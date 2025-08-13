#!/usr/bin/env python3
"""
Git setup script for Neo4j MCP Server project.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True, result.stdout.strip()
        else:
            print(f"✗ {description} failed")
            print(f"Error output: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False, str(e)


def check_git_installed():
    """Check if Git is installed and available."""
    success, output = run_command("git --version", "Checking Git installation", check=False)
    if success:
        print(f"✓ Git detected: {output}")
        return True
    else:
        print("✗ Git is not installed or not available in PATH")
        print("Please install Git first: https://git-scm.com/downloads")
        return False


def initialize_git_repo():
    """Initialize Git repository."""
    if os.path.exists(".git"):
        print("✓ Git repository already exists")
        return True
    
    success, _ = run_command("git init", "Initializing Git repository")
    return success


def configure_git_user():
    """Configure Git user settings."""
    # Check if user is already configured
    success, email = run_command("git config user.email", "Checking Git user email", check=False)
    if success and email:
        print(f"✓ Git user email already configured: {email}")
        return True
    
    print("\nGit user configuration:")
    print("Please enter your Git user information:")
    
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    
    if not name or not email:
        print("✗ Name and email are required")
        return False
    
    success1, _ = run_command(f'git config user.name "{name}"', "Setting Git user name")
    success2, _ = run_command(f'git config user.email "{email}"', "Setting Git user email")
    
    return success1 and success2


def create_initial_commit():
    """Create initial commit with project files."""
    # Add all files
    success1, _ = run_command("git add .", "Adding files to Git")
    if not success1:
        return False
    
    # Check if there are files to commit
    success2, output = run_command("git status --porcelain", "Checking Git status", check=False)
    if not success2 or not output.strip():
        print("✓ No files to commit (all files may be ignored)")
        return True
    
    # Create initial commit
    success3, _ = run_command(
        'git commit -m "Initial commit: Neo4j MCP Server foundation"',
        "Creating initial commit"
    )
    return success3


def setup_git_hooks():
    """Setup basic Git hooks for code quality."""
    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        print("⚠️  Git hooks directory not found")
        return True
    
    # Create pre-commit hook for basic checks
    pre_commit_hook = hooks_dir / "pre-commit"
    if not pre_commit_hook.exists():
        hook_content = """#!/bin/sh
# Pre-commit hook for Neo4j MCP Server

echo "Running pre-commit checks..."

# Check for Python syntax errors
python -m py_compile neo4j_mcp_server/__init__.py 2>/dev/null || {
    echo "✗ Python syntax errors found"
    exit 1
}

# Run basic tests if pytest is available
if command -v pytest >/dev/null 2>&1; then
    echo "Running basic tests..."
    pytest tests/test_config.py tests/test_core.py -q || {
        echo "✗ Basic tests failed"
        exit 1
    }
fi

echo "✓ Pre-commit checks passed"
"""
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # Make hook executable
            os.chmod(pre_commit_hook, 0o755)
            print("✓ Pre-commit hook created")
        except Exception as e:
            print(f"⚠️  Failed to create pre-commit hook: {e}")
    
    return True


def create_git_attributes():
    """Create .gitattributes file for consistent line endings."""
    gitattributes_content = """# Auto detect text files and perform LF normalization
* text=auto

# Python files
*.py text diff=python

# Documentation
*.md text diff=markdown
*.txt text
*.rst text

# Configuration files
*.yml text
*.yaml text
*.json text
*.toml text
*.ini text
*.cfg text
*.conf text

# Scripts
*.sh text eol=lf
*.bat text eol=crlf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.tar.gz binary
*.db binary
"""
    
    gitattributes_file = Path(".gitattributes")
    if not gitattributes_file.exists():
        try:
            with open(gitattributes_file, 'w') as f:
                f.write(gitattributes_content)
            print("✓ .gitattributes file created")
        except Exception as e:
            print(f"⚠️  Failed to create .gitattributes: {e}")
    
    return True


def setup_remote_repository():
    """Setup remote repository if URL is provided."""
    print("\nRemote repository setup:")
    print("If you have a remote repository URL (GitHub, GitLab, etc.), enter it below.")
    print("Leave empty to skip remote setup.")
    
    remote_url = input("Remote repository URL: ").strip()
    
    if not remote_url:
        print("✓ Skipping remote repository setup")
        return True
    
    # Add remote origin
    success1, _ = run_command(f'git remote add origin "{remote_url}"', "Adding remote origin")
    if not success1:
        return False
    
    # Set upstream branch
    success2, _ = run_command("git branch -M main", "Setting main branch")
    if not success2:
        return False
    
    print("\nRemote repository configured successfully!")
    print("To push your code, run: git push -u origin main")
    
    return True


def main():
    """Main Git setup function."""
    print("Setting up Git for Neo4j MCP Server project...")
    print("=" * 60)
    
    # Check if Git is installed
    if not check_git_installed():
        sys.exit(1)
    
    # Initialize Git repository
    if not initialize_git_repo():
        sys.exit(1)
    
    # Configure Git user
    if not configure_git_user():
        sys.exit(1)
    
    # Setup Git hooks
    setup_git_hooks()
    
    # Create .gitattributes
    create_git_attributes()
    
    # Create initial commit
    if not create_initial_commit():
        print("⚠️  Initial commit failed, but repository is initialized")
    
    # Setup remote repository
    setup_remote_repository()
    
    print("\n" + "=" * 60)
    print("🎉 Git setup completed!")
    print("\nNext steps:")
    print("1. Review your changes: git status")
    print("2. View commit history: git log --oneline")
    print("3. Add remote repository: git remote add origin <your-repo-url>")
    print("4. Push to remote: git push -u origin main")
    print("\nFor more information, see README.md and TRD_Neo4j_MCP_Server.md")


if __name__ == "__main__":
    main()
