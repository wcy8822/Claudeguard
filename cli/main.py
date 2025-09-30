#!/usr/bin/env python3
"""
ClaudeGuard CLI - Command Line Interface
Your AI Safety Net
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.guard import ClaudeGuard


def print_header():
    """Print ClaudeGuard header"""
    print("\n" + "="*70)
    print("🤖 ClaudeGuard - Your AI Safety Net".center(70))
    print("="*70 + "\n")


def cmd_status(args):
    """Show ClaudeGuard status"""
    guard = ClaudeGuard()
    status = guard.get_status()

    print_header()
    print("📊 System Status")
    print("-" * 70)
    print(f"Status: {'✅ Enabled' if status['enabled'] else '❌ Disabled'}")
    print(f"Total Backups: {status['total_backups']}")
    print(f"Total Operations: {status['total_operations']}")
    print(f"Storage Used: {status['storage_mb']:.2f} MB")
    print(f"Backup Directory: {status['backup_root']}")
    print(f"Operation Log: {status['log_file']}")
    print()


def cmd_list(args):
    """List recent backups"""
    guard = ClaudeGuard()
    limit = int(args[0]) if args else 10
    backups = guard.list_backups(limit=limit)

    print_header()
    print(f"📋 Recent Backups (showing {len(backups)} of {limit})")
    print("-" * 70)

    if not backups:
        print("No backups found.")
        return

    for i, backup in enumerate(backups, 1):
        timestamp = backup['timestamp']
        operation = backup['operation_type']
        risk = backup['risk_level']
        files = len(backup['affected_files'])
        backup_id = backup['backup_id']

        # Risk level emoji
        risk_emoji = {
            'LOW': '🟢',
            'MEDIUM': '🟡',
            'HIGH': '🟠',
            'CRITICAL': '🔴'
        }.get(risk, '⚪')

        print(f"{i:2}. {risk_emoji} {operation:15} | {files:2} files | {timestamp}")
        print(f"    ID: {backup_id}")
        if backup.get('git_commit'):
            print(f"    Git: {backup['git_commit'][:8]}")
        print()


def cmd_rollback(args):
    """Rollback to a previous backup"""
    guard = ClaudeGuard()

    if args:
        backup_id = args[0]
    else:
        # Use most recent backup
        backups = guard.list_backups(limit=1)
        if not backups:
            print("❌ No backups found to rollback")
            return
        backup_id = backups[0]['backup_id']

    print_header()
    print(f"🔄 Rolling back to: {backup_id}")
    print("-" * 70)

    success, message = guard.rollback(backup_id)

    if success:
        print(f"✅ {message}")
        print("\n🎉 Rollback complete!")
    else:
        print(f"❌ Rollback failed: {message}")
    print()


def cmd_verify(args):
    """Verify backup compliance"""
    guard = ClaudeGuard()

    print_header()
    print("🔍 Verifying Backup Compliance")
    print("-" * 70)

    # Count operations and backups
    operation_count = 0
    if guard.operation_log.exists():
        with open(guard.operation_log) as f:
            operation_count = sum(1 for _ in f)

    backups = list(guard.backup_root.glob("backup_*"))
    backup_count = len(backups)

    # Calculate compliance
    if operation_count > 0:
        compliance = (backup_count / operation_count) * 100
    else:
        compliance = 100.0

    print(f"Total Operations: {operation_count}")
    print(f"Total Backups: {backup_count}")
    print(f"Compliance Rate: {compliance:.1f}%")

    if compliance >= 100:
        print("\n✅ Fully Compliant - All operations are backed up!")
    elif compliance >= 90:
        print("\n⚠️  Mostly Compliant - Some operations may be missing backups")
    else:
        print("\n❌ Low Compliance - Many operations are not backed up")

    # Export report if requested
    if '--export' in args:
        export_idx = args.index('--export')
        if export_idx + 1 < len(args):
            export_file = args[export_idx + 1]
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_operations': operation_count,
                'total_backups': backup_count,
                'compliance_rate': compliance,
                'status': 'compliant' if compliance >= 100 else 'non_compliant'
            }
            with open(export_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Report exported to: {export_file}")

    print()


def cmd_cleanup(args):
    """Clean up old backups"""
    guard = ClaudeGuard()

    max_backups = int(args[0]) if args else guard.config['backup']['max_backups']

    print_header()
    print(f"🧹 Cleaning up backups (keeping {max_backups} most recent)")
    print("-" * 70)

    before = len(list(guard.backup_root.glob("backup_*")))
    guard.cleanup(max_backups=max_backups)
    after = len(list(guard.backup_root.glob("backup_*")))

    removed = before - after
    print(f"Removed {removed} old backups")
    print(f"Remaining: {after} backups")
    print("\n✅ Cleanup complete!")
    print()


def cmd_cost(args):
    """Show cost analysis"""
    guard = ClaudeGuard()
    status = guard.get_status()

    print_header()
    print("💰 Cost Analysis")
    print("-" * 70)
    print(f"Current Storage: {status['storage_mb']:.2f} MB")

    # Estimate future growth
    if status['total_operations'] > 0:
        avg_size = status['storage_mb'] / status['total_operations']
        # Assume 100 operations per month
        monthly_growth = avg_size * 100
        yearly_growth = monthly_growth * 12

        print(f"Average Backup Size: {avg_size:.4f} MB")
        print(f"Predicted Monthly Growth: {monthly_growth:.2f} MB")
        print(f"Predicted Yearly Growth: {yearly_growth:.2f} MB")

    print(f"\nEstimated Cost: $0.00/year")
    print("💡 ClaudeGuard uses local storage only - 100% free!")
    print("\n✅ Minimal impact, maximum protection")
    print()


def cmd_help(args):
    """Show help message"""
    print_header()
    print("📚 ClaudeGuard Commands")
    print("-" * 70)
    print("status              Show system status and statistics")
    print("list [N]            List N most recent backups (default: 10)")
    print("rollback [ID]       Rollback to backup ID (default: most recent)")
    print("verify              Verify backup compliance")
    print("verify --export F   Verify and export report to file F")
    print("cleanup [N]         Keep only N most recent backups")
    print("cost                Show storage cost analysis")
    print("help                Show this help message")
    print()
    print("Examples:")
    print("  claudeguard status")
    print("  claudeguard list 20")
    print("  claudeguard rollback backup_20250930_160000")
    print("  claudeguard verify --export report.json")
    print()


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        cmd_help([])
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        'status': cmd_status,
        'list': cmd_list,
        'rollback': cmd_rollback,
        'verify': cmd_verify,
        'cleanup': cmd_cleanup,
        'cost': cmd_cost,
        'help': cmd_help
    }

    if command in commands:
        try:
            commands[command](args)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            sys.exit(1)
    else:
        print(f"\n❌ Unknown command: {command}\n")
        cmd_help([])
        sys.exit(1)


if __name__ == "__main__":
    main()