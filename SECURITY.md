# Security Policy

## Overview

This document outlines the security policies and procedures for the Virtual Battery for Home Assistant integration, including how to report vulnerabilities and the recommended branch protection settings for repository administrators.

## Reporting Security Vulnerabilities

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in this integration, please report it by emailing the maintainer directly or by using GitHub's private security advisory feature:

1. Navigate to the repository on GitHub
2. Go to the **Security** tab
3. Click **Report a vulnerability**
4. Provide detailed information about the vulnerability

We take all security reports seriously and will respond as quickly as possible.

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact and severity
- Any suggested fixes or mitigations (if available)

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| Older   | :x:                |

We recommend always using the latest version of the integration to ensure you have the most recent security patches.

## Branch Protection Policies

This repository uses a CODEOWNERS file to enforce code review requirements. Repository administrators should configure the following branch protection rules for the `main` branch to ensure secure development practices.

### Recommended Branch Protection Rules for `main`

#### 1. Require Pull Request Reviews Before Merging

- **Enable**: Require pull request reviews before merging
- **Required approving reviews**: At least 1
- **Dismiss stale pull request approvals when new commits are pushed**: ✅ Enabled
- **Require review from Code Owners**: ✅ Enabled (enforces CODEOWNERS file)
- **Restrict who can dismiss pull request reviews**: Optional, but recommended for larger teams

**Rationale**: Ensures all code changes are reviewed by the designated code owner (@andybochmann) before being merged, preventing unreviewed or malicious code from reaching production.

#### 2. Require Status Checks to Pass

- **Enable**: Require status checks to pass before merging
- **Require branches to be up to date before merging**: ✅ Enabled
- **Required status checks**: Configure based on your CI/CD pipeline
  - HACS validation (if configured)
  - Automated tests (if configured)
  - Linting/code quality checks (if configured)

**Rationale**: Ensures all automated tests and quality checks pass before code is merged, catching potential issues early.

#### 3. Require Conversation Resolution

- **Enable**: Require conversation resolution before merging ✅

**Rationale**: Ensures all review comments and discussions are addressed before merging, promoting thorough code review.

#### 4. Require Linear History

- **Enable**: Require linear history (Optional, but recommended)

**Rationale**: Maintains a clean, easy-to-audit commit history by preventing merge commits.

#### 5. Require Signed Commits

- **Enable**: Require signed commits (Recommended for enhanced security)

**Rationale**: Ensures commit authenticity by requiring GPG or SSH signatures, preventing commit spoofing.

#### 6. Include Administrators

- **Enable**: Do not include administrators in these restrictions (Default)
- **Alternative**: Include administrators for maximum security

**Rationale**: Consider enabling this for maximum security, but note that it may slow down critical hotfixes. Use your judgment based on team size and workflow.

#### 7. Restrict Pushes

- **Enable**: Restrict who can push to matching branches
- **Allowed to push**: Limit to specific users or teams (Optional)

**Rationale**: Prevents accidental direct pushes to the main branch, ensuring all changes go through the pull request process.

#### 8. Allow Force Pushes

- **Disable**: Do not allow force pushes ✅

**Rationale**: Force pushes can rewrite history and potentially remove security fixes or introduce vulnerabilities.

#### 9. Allow Deletions

- **Disable**: Do not allow deletions ✅

**Rationale**: Prevents accidental or malicious deletion of the main branch.

### How to Configure Branch Protection

Repository administrators can configure these settings via:

1. **GitHub Web UI**:
   - Navigate to **Settings** → **Branches**
   - Under "Branch protection rules", click **Add rule**
   - Enter `main` as the branch name pattern
   - Configure the settings as outlined above
   - Click **Create** or **Save changes**

2. **GitHub CLI**:
   ```bash
   gh api repos/:owner/:repo/branches/main/protection \
     --method PUT \
     --field required_pull_request_reviews[require_code_owner_reviews]=true \
     --field required_pull_request_reviews[required_approving_review_count]=1 \
     --field required_pull_request_reviews[dismiss_stale_reviews]=true \
     --field enforce_admins=false \
     --field required_conversation_resolution[enabled]=true \
     --field allow_force_pushes[enabled]=false \
     --field allow_deletions[enabled]=false
   ```

3. **GitHub API**: See [GitHub Branch Protection API documentation](https://docs.github.com/en/rest/branches/branch-protection)

## Code Review Requirements

The repository includes a `.github/CODEOWNERS` file that defines code ownership. Key points:

- **All files** require review from @andybochmann
- **Security-sensitive areas** are explicitly marked:
  - GitHub workflows (`.github/workflows/`)
  - Core component code (`custom_components/virtual_battery/`)
  - Configuration flow (`config_flow.py`)
  - Services configuration (`services.yaml`)
  - Component initialization (`__init__.py`)

Contributors should:
1. Create a pull request for all changes
2. Wait for automated checks to pass (if configured)
3. Address review comments from the code owner
4. Obtain approval before merging

## Security Best Practices for Contributors

1. **Never commit sensitive data**: API keys, passwords, tokens, or personal information
2. **Keep dependencies updated**: Regularly update Home Assistant and integration dependencies
3. **Validate user input**: Always sanitize and validate data from configuration flows and services
4. **Follow Home Assistant security guidelines**: Adhere to [Home Assistant's security best practices](https://developers.home-assistant.io/docs/security/)
5. **Test thoroughly**: Test changes in a local Home Assistant instance before submitting
6. **Use secrets properly**: Use Home Assistant's secrets management for sensitive configuration

## Security Considerations for Users

When using this integration:

1. **Install from trusted sources**: Only install from the official repository or HACS
2. **Review permissions**: Understand what data the integration accesses
3. **Keep updated**: Install updates promptly to receive security patches
4. **Report issues**: Report any suspicious behavior or security concerns

## Dependency Security

This integration depends on Home Assistant core. Security updates for dependencies are handled through:

1. **Home Assistant updates**: Keep Home Assistant updated to the latest stable version
2. **Integration updates**: Update the integration when new versions are released
3. **Monitoring**: The maintainer monitors for security advisories affecting dependencies

## License

This security policy is part of the Virtual Battery for Home Assistant integration, licensed under the MIT License.

## Contact

For security-related questions or concerns:
- Repository: [andybochmann/ha-virtual-battery](https://github.com/andybochmann/ha-virtual-battery)
- Maintainer: [@andybochmann](https://github.com/andybochmann)

---

*Last updated: 2026-01-09*
