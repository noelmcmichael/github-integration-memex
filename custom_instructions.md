# GitHub Integration Custom Instructions

Add this to your Memex Custom Instructions for automatic GitHub integration:

## GitHub Integration Block

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

## Usage Instructions

1. Copy the GitHub Integration Block above
2. Add it to your Custom Instructions in Memex
3. All new projects will automatically have GitHub integration available
4. Memex will offer to create GitHub repositories for new projects
5. Git operations will use the configured identity automatically

## Benefits

- No need to configure git/GitHub for each project
- Consistent identity across all projects
- Automatic GitHub repository creation
- Helper functions for common operations
- Standardized workflow across all Memex projects