#!/usr/bin/env python3
"""
Development setup script for Neo4j MCP Server using nv for environment management.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_nv_installed():
    """Check if nv is installed and available."""
    try:
        result = subprocess.run(["nv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ nv detected: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def create_env_file():
    """Create .env file from example if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from example...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✓ .env file created from example")
        print("⚠️  Please update .env with your actual Neo4j credentials")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("⚠️  No env.example file found, please create .env manually")


def main():
    """Main setup function."""
    print("Setting up Neo4j MCP Server development environment with nv...")
    print("=" * 60)
    
    # Check if nv is installed
    if not check_nv_installed():
        print("✗ nv is not installed or not available in PATH")
        print("Please install nv first: https://github.com/jcouture/nv")
        sys.exit(1)
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 9):
        print(f"✗ Python 3.9+ required, found {python_version.major}.{python_version.minor}")
        sys.exit(1)
    else:
        print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Create or activate nv environment
    project_name = "neo4j-mcp-server"
    print(f"Setting up nv environment: {project_name}")
    
    # Check if environment already exists
    try:
        result = subprocess.run(["nv", "list"], capture_output=True, text=True)
        if project_name in result.stdout:
            print(f"✓ nv environment '{project_name}' already exists")
            if not run_command(f"nv use {project_name}", f"Activating existing environment '{project_name}'"):
                sys.exit(1)
        else:
            print(f"Creating new nv environment: {project_name}")
            if not run_command(f"nv create {project_name}", f"Creating nv environment '{project_name}'"):
                sys.exit(1)
            if not run_command(f"nv use {project_name}", f"Activating nv environment '{project_name}'"):
                sys.exit(1)
    except Exception as e:
        print(f"✗ Failed to manage nv environment: {e}")
        sys.exit(1)
    
    # Install dependencies using nv
    print("Installing dependencies...")
    if not run_command("nv pip install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    if not run_command("nv pip install -r requirements.txt", "Installing requirements"):
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Run tests
    print("Running tests...")
    if not run_command("nv pip install pytest pytest-cov", "Installing test dependencies"):
        print("⚠️  Test dependencies installation failed, continuing...")
    
    if run_command("nv run pytest tests/ -v", "Running tests"):
        print("✓ All tests passed")
    else:
        print("⚠️  Some tests failed, but setup completed")
    
    print("\n" + "=" * 60)
    print("🎉 Development environment setup completed with nv!")
    print("\nNext steps:")
    print("1. Activate the environment: nv use neo4j-mcp-server")
    print("2. Update .env file with your Neo4j credentials")
    print("3. Start Neo4j database")
    print("4. Run the server: nv run python run_server.py")
    print("5. Run tests: nv run pytest tests/ -v")
    print("\nFor more information, see README.md and TRD_Neo4j_MCP_Server.md")


if __name__ == "__main__":
    main()
