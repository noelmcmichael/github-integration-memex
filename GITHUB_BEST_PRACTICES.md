# GitHub Best Practices Guide

## Adding Custom Instructions to Memex

### Step-by-Step Instructions

1. **Open Memex Settings**
   - Click the gear icon (⚙️) in the Memex interface
   
2. **Navigate to Custom Instructions**
   - Look for the "Custom Instructions" section in settings
   
3. **Add the GitHub Integration Block**
   - Copy the following block from `custom_instructions.md`:

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

4. **Save Settings**
   - Apply the changes to activate GitHub integration for all future projects

---

## Individual Developer Best Practices

### Repository Management

#### 1. Repository Structure
```
project-name/
├── README.md              # Project overview and setup instructions
├── .gitignore            # Files to exclude from version control
├── .github/              # GitHub-specific configurations
│   ├── workflows/        # GitHub Actions CI/CD
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   └── pull_request_template.md
├── docs/                 # Documentation
├── src/                  # Source code
├── tests/                # Test files
└── scripts/              # Build/deployment scripts
```

#### 2. Essential Files

**README.md Template:**
```markdown
# Project Name

## Description
Brief description of what the project does.

## Installation
```bash
git clone https://github.com/noelmcmichael/project-name.git
cd project-name
npm install
```

## Usage
Basic usage examples

## Contributing
Guidelines for contributing

## License
License information
```

**`.gitignore` Essentials:**
```
# Dependencies
node_modules/
*.log

# Environment variables
.env
.env.local

# Build outputs
dist/
build/

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

### Commit Best Practices

#### 1. Commit Message Format
Use the **Conventional Commits** standard:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic changes)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(auth): add OAuth2 login functionality

fix(api): resolve timeout issue in user search

docs: update installation instructions

style: format code according to style guide

refactor(database): optimize query performance

test: add unit tests for user service

chore: update dependencies
```

#### 2. Commit Frequency
- **Commit often**: Small, logical changes
- **Atomic commits**: One feature/fix per commit
- **Complete state**: Each commit should leave the code in a working state

#### 3. Writing Quality Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- Keep subject line under 50 characters
- Separate subject from body with blank line
- Explain *what* and *why*, not *how*
- Reference issues: "Fixes #123" or "Closes #456"

### Branching Strategy for Individual Work

#### 1. GitHub Flow (Recommended for Individual Projects)
```
main branch (always deployable)
├── feature/user-authentication
├── fix/login-bug
└── docs/api-documentation
```

**Workflow:**
1. Create feature branch from `main`
2. Work on feature
3. Push branch to GitHub
4. Create Pull Request
5. Review and merge
6. Delete feature branch

#### 2. Branch Naming Conventions
```
feature/feature-name
fix/bug-description
hotfix/critical-issue
docs/documentation-update
refactor/component-name
chore/dependency-update
```

### Security Best Practices

#### 1. Never Commit Secrets
- API keys, passwords, tokens
- Use environment variables
- Add sensitive files to `.gitignore`
- Use GitHub's secret detection

#### 2. Code Scanning
- Enable Dependabot alerts
- Use GitHub's security advisories
- Run security scans on dependencies
- Keep dependencies updated

#### 3. Repository Settings
- Enable vulnerability alerts
- Set up security policies
- Use signed commits for sensitive projects

---

## Team Collaboration Best Practices

### Repository Setup

#### 1. Branch Protection Rules
Navigate to Settings → Branches in your repository:

**Main Branch Protection:**
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ✅ Restrict pushes that create new commits
- ✅ Do not allow bypassing the above settings

#### 2. Repository Templates
Create organization-wide templates with:
- Standard file structure
- Default `.gitignore`
- Issue/PR templates
- Contributing guidelines
- Code of conduct

### Team Workflow Strategies

#### 1. Git Flow (For Release-Based Projects)
```
main          (production releases)
├── develop   (integration branch)
├── feature/  (new features)
├── release/  (release preparation)
└── hotfix/   (critical fixes)
```

**Best for:**
- Projects with scheduled releases
- Multiple versions in production
- Larger teams with formal processes

#### 2. GitHub Flow (For Continuous Deployment)
```
main          (always deployable)
├── feature/  (all work branches)
```

**Best for:**
- Web applications
- Continuous deployment
- Small to medium teams

#### 3. Trunk-Based Development (For High-Velocity Teams)
```
main          (trunk - everyone commits here)
├── short-lived feature branches (< 1 day)
```

**Best for:**
- Teams with strong CI/CD
- Feature flags implementation
- Experienced teams

### Pull Request Best Practices

#### 1. PR Creation Guidelines

**Template Example:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
```

#### 2. PR Size and Scope
- **Small PRs**: Easier to review (< 400 lines changed)
- **Single purpose**: One feature/fix per PR
- **Complete**: Include tests and documentation
- **Self-contained**: Can be merged independently

#### 3. PR Description Best Practices
- Clear title summarizing changes
- Detailed description of what and why
- Link to related issues
- Include screenshots for UI changes
- Add testing instructions
- Mention breaking changes

### Code Review Process

#### 1. Review Checklist

**For Reviewers:**
- [ ] Code is readable and well-documented
- [ ] Logic is correct and efficient
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities
- [ ] Follows coding standards
- [ ] No unnecessary complexity
- [ ] Error handling is appropriate

**Review Types:**
- **Approve**: Ready to merge
- **Request Changes**: Issues that must be fixed
- **Comment**: Suggestions or questions

#### 2. Review Etiquette

**For Authors:**
- Respond to all feedback
- Ask for clarification if unclear
- Be open to suggestions
- Test suggested changes
- Update PR description if scope changes

**For Reviewers:**
- Be constructive and respectful
- Explain the "why" behind feedback
- Suggest solutions, not just problems
- Acknowledge good code
- Focus on the code, not the person

#### 3. Review Process Flow
```
1. Author creates PR
2. Automated checks run (CI/CD)
3. Team members review
4. Author addresses feedback
5. Re-review if needed
6. Approved PR gets merged
7. Feature branch deleted
```

### Team Communication

#### 1. Issue Management
```markdown
# Bug Report Template
**Bug Description:** Clear description

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:** OS, browser, version

**Screenshots:** If applicable
```

#### 2. Project Management
- Use GitHub Projects for task tracking
- Label issues consistently
- Assign issues to team members
- Set milestones for releases
- Link PRs to issues

#### 3. Communication Channels
- Use discussions for architecture decisions
- Comment on PRs for code-specific feedback
- Use issues for bug reports and feature requests
- Document decisions in repository wiki

### CI/CD Integration

#### 1. GitHub Actions Workflow
```yaml
name: CI/CD

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Run linting
        run: npm run lint
      - name: Check types
        run: npm run type-check
```

#### 2. Quality Gates
- All tests must pass
- Code coverage thresholds met
- Security scans pass
- Code style checks pass
- No merge conflicts

### Advanced Team Practices

#### 1. Semantic Versioning
```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1 (patch: bug fixes)
1.0.1 → 1.1.0 (minor: new features)
1.1.0 → 2.0.0 (major: breaking changes)
```

#### 2. Release Management
- Use GitHub Releases for version tracking
- Maintain CHANGELOG.md
- Tag releases with semantic versions
- Include release notes
- Automate release creation

#### 3. Documentation Strategy
- Keep README updated
- Document API changes
- Maintain architecture decision records (ADRs)
- Update getting started guides
- Create troubleshooting guides

---

## Automation and Tools

### GitHub CLI Commands

**Repository Management:**
```bash
# Create repository
gh repo create project-name --public

# Clone repository
gh repo clone noelmcmichael/project-name

# View repository info
gh repo view

# List repositories
gh repo list noelmcmichael
```

**Issue Management:**
```bash
# Create issue
gh issue create --title "Bug: Login fails" --body "Description"

# List issues
gh issue list

# View issue
gh issue view 123

# Close issue
gh issue close 123
```

**Pull Request Management:**
```bash
# Create PR
gh pr create --title "Add new feature" --body "Description"

# List PRs
gh pr list

# Review PR
gh pr review 456 --approve

# Merge PR
gh pr merge 456 --squash
```

### Integration Tools

#### 1. Development Tools
- **IDEs**: VS Code with GitHub extension
- **Git GUI**: GitKraken, Sourcetree
- **Code quality**: SonarQube, CodeClimate
- **Security**: Snyk, GitHub Security

#### 2. Communication
- **Slack/Discord**: GitHub integration for notifications
- **Email**: GitHub notifications
- **Project management**: Jira, Linear integration

---

## Troubleshooting Common Issues

### Merge Conflicts
```bash
# Update your branch with latest main
git checkout main
git pull
git checkout feature-branch
git merge main

# Resolve conflicts in files
# Then commit
git add .
git commit -m "Resolve merge conflicts"
```

### Accidental Commits
```bash
# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Undo last commit (discards changes)
git reset --hard HEAD~1

# Amend last commit message
git commit --amend -m "New message"
```

### Force Push Safety
```bash
# Safer force push
git push --force-with-lease origin feature-branch

# Instead of
git push --force origin feature-branch
```

---

## Consistency Guidelines

### Team Standards Document
Create a `CONTRIBUTING.md` file with:
- Development setup instructions
- Coding style guidelines
- Testing requirements
- Review process
- Release procedures

### Code Style
- Use consistent formatting (Prettier, ESLint)
- Follow language-specific conventions
- Document complex logic
- Use meaningful variable names
- Keep functions small and focused

### Regular Team Practices
- Weekly code review retrospectives
- Monthly security audits
- Quarterly workflow improvements
- Annual tooling evaluations

---

This comprehensive guide ensures consistent, secure, and efficient GitHub usage for both individual projects and team collaboration. Adapt these practices based on your specific project needs and team size.