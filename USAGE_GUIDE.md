# GitHub Integration Usage Guide

## Quick Start

Your GitHub integration is now set up! Here's how to use it:

### 1. Add Custom Instructions

Copy this block and add it to your Memex Custom Instructions:

```
<github_integration>
The user has GitHub integration configured:
- GitHub Username: noelmcmichael
- GitHub CLI available at: /opt/homebrew/bin/gh
- Global git config set with: noelmcmichael <ropak9@gmail.com>
- Authentication: Already logged in via GitHub CLI

Default GitHub behaviors:
- When creating new projects, offer to create GitHub repository
- Use GitHub CLI for all GitHub operations
- Default to public repositories unless specified otherwise
- Always push to GitHub after initial setup
- Create repositories with descriptive names and README files
- Use conventional commit messages

GitHub CLI commands to use:
- `gh repo create` - Create new repository
- `gh repo view` - View repository information  
- `gh repo list` - List user repositories
- `gh issue create` - Create issues
- `gh pr create` - Create pull requests
- `gh auth status` - Check authentication status

Helper functions are available in github_helpers.py for common operations.
</github_integration>
```

### 2. Using GitHub with New Projects

When you start a new Memex project, Memex will now automatically:
- Offer to create a GitHub repository
- Set up git with your identity
- Push your initial commit to GitHub
- Provide GitHub CLI commands for common operations

### 3. Manual GitHub Operations

You can also use GitHub CLI directly:

```bash
# Create a new repository
gh repo create my-project --description "My new project" --public

# View repository info
gh repo view

# List your repositories
gh repo list

# Create an issue
gh issue create --title "Bug report" --body "Description of the issue"

# Create a pull request
gh pr create --title "Feature: Add new functionality" --body "Description of changes"
```

### 4. Using Helper Functions

The `github_helpers.py` file provides Python functions for common operations:

```python
from github_helpers import *

# Get your GitHub username
username = get_github_username()

# Create a new repository
create_github_repo("my-new-project", "Project description", private=False)

# Initialize current directory with GitHub
init_repo_with_github("my-project", "My awesome project")

# Push to GitHub
push_to_github()

# List your repositories
repos = list_my_repos()
```

## Configuration Details

### Global Git Settings
- **Name**: noelmcmichael
- **Email**: ropak9@gmail.com
- **Applied to**: All repositories on your Mac

### GitHub CLI
- **Path**: `/opt/homebrew/bin/gh`
- **Version**: 2.74.2
- **Authentication**: Active (keyring)
- **Scopes**: gist, read:org, repo, workflow

### Memex Secrets
- **GITHUB_USERNAME**: noelmcmichael

## Benefits

1. **Seamless Workflow**: No need to configure git for each project
2. **Consistent Identity**: Same name/email across all projects
3. **Automated Setup**: Memex can create repositories automatically
4. **Helper Functions**: Common operations made simple
5. **CLI Integration**: Full GitHub CLI functionality available

## Troubleshooting

### Git Identity Issues
If you get "Please tell me who you are" errors:
```bash
git config --global user.name "noelmcmichael"
git config --global user.email "ropak9@gmail.com"
```

### GitHub CLI Authentication
Check authentication status:
```bash
gh auth status
```

Re-authenticate if needed:
```bash
gh auth login
```

### Helper Functions Not Working
Make sure you're in a directory with the helper functions:
```bash
cp /Users/noelmcmichael/Workspace/github_integration_memex/github_helpers.py .
```

## Next Steps

1. Add the custom instructions to Memex
2. Test with your next project
3. Use `gh` commands for daily GitHub operations
4. Leverage helper functions for automation

Your GitHub integration is ready to use! 🚀