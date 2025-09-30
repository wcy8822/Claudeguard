#!/usr/bin/env python3
"""
ClaudeGuard Core - Automatic Backup Engine
Captures snapshots before AI operations for instant rollback
"""

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ClaudeGuard:
    """Core backup and rollback engine for Claude Code operations"""

    RISK_LEVELS = {
        'LOW': ['Read', 'Glob', 'Grep', 'WebSearch', 'WebFetch'],
        'MEDIUM': ['Write', 'Edit', 'NotebookEdit'],
        'HIGH': ['Bash', 'Task'],
        'CRITICAL': ['rm -rf', 'DROP', 'DELETE', 'TRUNCATE']
    }

    def __init__(self, project_root: str = None, config: Dict = None):
        """
        Initialize ClaudeGuard

        Args:
            project_root: Project directory (defaults to current directory)
            config: Configuration dictionary (defaults to load from config.yaml)
        """
        self.project_root = Path(project_root or Path.cwd())
        self.backup_root = self.project_root / ".claudeguard" / "backups"
        self.log_dir = self.project_root / ".claudeguard" / "logs"
        self.operation_log = self.log_dir / "operation_history.jsonl"

        # Create directories
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Load or use provided config
        self.config = config or self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from config.yaml"""
        config_path = self.project_root / ".claudeguard" / "config.yaml"
        if config_path.exists():
            import yaml
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self._default_config()

    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'backup': {
                'enabled': True,
                'max_backups': 100,
                'retention_days': 30,
                'auto_cleanup': True
            },
            'risk_detection': {
                'enabled': True,
                'warn_on_high_risk': True
            },
            'verification': {
                'auto_verify': False,
                'compliance_threshold': 100
            },
            'storage': {
                'compression': False,
                'encryption': False
            }
        }

    def _get_risk_level(self, operation: str) -> str:
        """Classify operation risk level"""
        operation_upper = operation.upper()

        # Check CRITICAL first
        for pattern in self.RISK_LEVELS['CRITICAL']:
            if pattern in operation_upper:
                return 'CRITICAL'

        # Check operation type
        for level, patterns in self.RISK_LEVELS.items():
            for pattern in patterns:
                if operation.startswith(pattern):
                    return level

        return 'MEDIUM'  # Default to MEDIUM for unknown operations

    def _get_git_snapshot(self) -> Optional[str]:
        """Capture current Git commit hash"""
        if not (self.project_root / ".git").exists():
            return None

        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    def create_backup(
        self,
        operation_type: str,
        operation_details: Dict,
        affected_files: List[str] = None
    ) -> str:
        """
        Create backup snapshot before operation

        Args:
            operation_type: Type of operation (Write, Edit, Bash, etc.)
            operation_details: Details about the operation
            affected_files: List of files that will be modified

        Returns:
            backup_id: Unique identifier for this backup
        """
        if not self.config['backup']['enabled']:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_id = f"backup_{timestamp}"
        backup_dir = self.backup_root / backup_id
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Get risk level
        risk_level = self._get_risk_level(operation_type)

        # Backup affected files
        backed_up_files = []
        if affected_files:
            for file_path in affected_files:
                file_path = Path(file_path)
                if file_path.exists() and file_path.is_file():
                    try:
                        # Preserve directory structure
                        rel_path = file_path.relative_to(self.project_root)
                        backup_file = backup_dir / rel_path
                        backup_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, backup_file)
                        backed_up_files.append(str(rel_path))
                    except Exception as e:
                        print(f"Warning: Could not backup {file_path}: {e}")

        # Create metadata
        metadata = {
            'backup_id': backup_id,
            'timestamp': timestamp,
            'operation_type': operation_type,
            'operation_details': operation_details,
            'risk_level': risk_level,
            'affected_files': backed_up_files,
            'git_commit': self._get_git_snapshot(),
            'project_root': str(self.project_root)
        }

        # Save metadata
        with open(backup_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        # Log operation
        with open(self.operation_log, 'a') as f:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'backup_id': backup_id,
                'operation_type': operation_type,
                'risk_level': risk_level,
                'files_count': len(backed_up_files)
            }
            f.write(json.dumps(log_entry) + '\n')

        return backup_id

    def rollback(self, backup_id: str = None) -> Tuple[bool, str]:
        """
        Rollback to a previous backup

        Args:
            backup_id: Specific backup to restore (defaults to most recent)

        Returns:
            (success, message): Success status and message
        """
        # Find backup
        if backup_id is None:
            backups = sorted(self.backup_root.glob("backup_*"))
            if not backups:
                return False, "No backups found"
            backup_dir = backups[-1]
            backup_id = backup_dir.name
        else:
            backup_dir = self.backup_root / backup_id
            if not backup_dir.exists():
                return False, f"Backup {backup_id} not found"

        # Load metadata
        metadata_file = backup_dir / "metadata.json"
        if not metadata_file.exists():
            return False, f"Backup metadata not found for {backup_id}"

        with open(metadata_file) as f:
            metadata = json.load(f)

        # Restore files
        restored_count = 0
        for rel_path in metadata['affected_files']:
            backup_file = backup_dir / rel_path
            target_file = self.project_root / rel_path

            if backup_file.exists():
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target_file)
                    restored_count += 1
                except Exception as e:
                    return False, f"Error restoring {rel_path}: {e}"

        message = f"Restored {restored_count} files from {backup_id}"
        return True, message

    def list_backups(self, limit: int = 10) -> List[Dict]:
        """
        List recent backups

        Args:
            limit: Maximum number of backups to return

        Returns:
            List of backup metadata dictionaries
        """
        backups = sorted(self.backup_root.glob("backup_*"), reverse=True)[:limit]

        result = []
        for backup_dir in backups:
            metadata_file = backup_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                result.append(metadata)

        return result

    def get_status(self) -> Dict:
        """Get ClaudeGuard system status"""
        backups = list(self.backup_root.glob("backup_*"))

        # Calculate total storage
        total_size = sum(
            f.stat().st_size
            for backup in backups
            for f in backup.rglob("*")
            if f.is_file()
        )

        # Count operations from log
        operation_count = 0
        if self.operation_log.exists():
            with open(self.operation_log) as f:
                operation_count = sum(1 for _ in f)

        return {
            'enabled': self.config['backup']['enabled'],
            'total_backups': len(backups),
            'total_operations': operation_count,
            'storage_mb': total_size / (1024 * 1024),
            'backup_root': str(self.backup_root),
            'log_file': str(self.operation_log)
        }

    def cleanup(self, max_backups: int = None, max_age_days: int = None):
        """
        Clean up old backups

        Args:
            max_backups: Maximum number of backups to keep
            max_age_days: Maximum age in days
        """
        max_backups = max_backups or self.config['backup']['max_backups']
        max_age_days = max_age_days or self.config['backup']['retention_days']

        backups = sorted(self.backup_root.glob("backup_*"), reverse=True)

        # Remove by count
        if len(backups) > max_backups:
            for backup in backups[max_backups:]:
                shutil.rmtree(backup)

        # Remove by age
        cutoff_time = datetime.now().timestamp() - (max_age_days * 86400)
        for backup in backups:
            if backup.stat().st_mtime < cutoff_time:
                shutil.rmtree(backup)