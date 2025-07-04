#!/usr/bin/env python3
"""
GitHub Helper Functions for Memex Projects
Provides easy-to-use functions for common GitHub operations
"""

import subprocess
import json
import keyring
from pathlib import Path

def get_github_username():
    """Get GitHub username from Memex secrets"""
    try:
        return keyring.get_password("memex", "GITHUB_USERNAME")
    except Exception:
        return "noelmcmichael"  # fallback

def run_gh_command(command_args):
    """Run a GitHub CLI command and return the result"""
    try:
        cmd = ["/opt/homebrew/bin/gh"] + command_args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"GitHub CLI error: {e.stderr}")
        return None

def create_github_repo(repo_name, description="", private=False):
    """Create a new GitHub repository"""
    cmd_args = ["repo", "create", repo_name, "--description", description]
    if private:
        cmd_args.append("--private")
    else:
        cmd_args.append("--public")
    
    result = run_gh_command(cmd_args)
    if result:
        print(f"✅ Repository '{repo_name}' created successfully")
        return True
    return False

def init_repo_with_github(repo_name, description="Memex project", private=False):
    """Initialize current directory as git repo and create GitHub repo"""
    # Initialize git repo
    subprocess.run(["git", "init"], check=True)
    
    # Create GitHub repo
    if create_github_repo(repo_name, description, private):
        # Add remote origin
        username = get_github_username()
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        print(f"✅ Remote origin added: {remote_url}")
        return True
    return False

def push_to_github(branch="main"):
    """Push current branch to GitHub"""
    try:
        subprocess.run(["git", "push", "-u", "origin", branch], check=True)
        print(f"✅ Pushed to GitHub branch: {branch}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to push: {e}")
        return False

def get_repo_info():
    """Get information about current repository"""
    result = run_gh_command(["repo", "view", "--json", "name,description,url,isPrivate"])
    if result:
        return json.loads(result)
    return None

def list_my_repos():
    """List all repositories for the authenticated user"""
    result = run_gh_command(["repo", "list", "--json", "name,description,isPrivate,url"])
    if result:
        return json.loads(result)
    return []

if __name__ == "__main__":
    # Test the functions
    print("GitHub Helper Functions Test")
    print(f"GitHub Username: {get_github_username()}")
    
    # List repositories
    repos = list_my_repos()
    print(f"Number of repositories: {len(repos)}")
    
    # Show current repo info if in a repo
    repo_info = get_repo_info()
    if repo_info:
        print(f"Current repo: {repo_info['name']}")