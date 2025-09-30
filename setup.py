#!/usr/bin/env python3
"""
ClaudeGuard Setup Script
Install ClaudeGuard globally with pip
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="claudeguard",
    version="1.0.0",
    author="ClaudeGuard Team",
    author_email="support@claudeguard.dev",
    description="Your AI Safety Net - Automatic backup and rollback for Claude Code operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claudeguard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claudeguard=cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "claudeguard": [
            "config.yaml",
            "README.md",
            "LICENSE",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/claudeguard/issues",
        "Source": "https://github.com/yourusername/claudeguard",
        "Documentation": "https://docs.claudeguard.dev",
    },
)