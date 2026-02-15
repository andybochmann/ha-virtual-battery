# Contributing to Virtual Battery for Home Assistant

Thank you for your interest in contributing to Virtual Battery! This document provides guidelines and information to help you contribute effectively.

## 🤝 How to Contribute

We welcome contributions of all kinds:

- 🐛 Bug reports and fixes
- ✨ Feature requests and implementations
- 📝 Documentation improvements
- 🧪 Test coverage enhancements
- 🎨 UI/UX improvements
- 🌍 Translations

## 📋 Development Workflow

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/ha-virtual-battery.git
   cd ha-virtual-battery
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/andybochmann/ha-virtual-battery.git
   ```

### 2. Create a Branch

Create a feature branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or improvements

### 3. Make Your Changes

- Follow the existing code style and patterns
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Test your changes thoroughly in a local Home Assistant instance

### 4. Test Your Changes

Before submitting, ensure your changes work correctly:

1. **Set up a local Home Assistant development environment**:
   - Install Home Assistant Core in development mode
   - Copy your modified integration to the `custom_components` folder
   - Restart Home Assistant

2. **Test the integration**:
   - Add/configure the Virtual Battery integration
   - Test all affected functionality
   - Verify existing features still work
   - Test edge cases and error handling

3. **Code quality checks**:
   - Ensure Python code follows PEP 8 style guidelines
   - Remove any debugging code (print statements, commented code)
   - Validate YAML files if modified

### 5. Submit a Pull Request

1. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** on GitHub:
   - Provide a clear title describing the change
   - Fill out the pull request template (if available)
   - Reference any related issues (e.g., "Fixes #123")
   - Describe what changed and why
   - Include screenshots for UI changes
   - List any breaking changes

3. **Wait for review** (see Code Review Process below)

## 👤 Code Review Process

This repository uses a **CODEOWNERS file** and **mandatory code reviews** to maintain code quality and security.

### What is CODEOWNERS?

The `.github/CODEOWNERS` file defines who is responsible for reviewing code in different parts of the repository. For this project:

- **All files** require review from [@andybochmann](https://github.com/andybochmann)
- **Security-sensitive areas** have explicit ownership rules:
  - GitHub workflows (`.github/workflows/`)
  - Core component code (`custom_components/virtual_battery/`)
  - Configuration flow (`config_flow.py`)
  - Services configuration (`services.yaml`)
  - Component initialization (`__init__.py`)

### How CODEOWNERS Affects Your Pull Request

When you submit a pull request:

1. **Automatic review request**: GitHub automatically requests review from the code owner(s) based on which files you modified

2. **Blocking review**: Your PR cannot be merged until:
   - The code owner approves your changes
   - All automated checks pass (if configured)
   - All review conversations are resolved

3. **Re-review on changes**: If you push new commits after approval:
   - Previous approvals may be dismissed (if branch protection is configured this way)
   - The code owner will need to review the changes again

### Review Timeline

- **Initial review**: Typically within 3-7 days
- **Follow-up reviews**: Usually faster after initial feedback
- **Urgent fixes**: Security issues are prioritized

### What Reviewers Look For

Code reviews focus on:

✅ **Functionality**: Does the code work as intended?
✅ **Security**: Are there any security vulnerabilities? (See [SECURITY.md](SECURITY.md))
✅ **Code quality**: Is the code clean, maintainable, and well-documented?
✅ **Home Assistant standards**: Does it follow Home Assistant integration guidelines?
✅ **Testing**: Has the code been tested thoroughly?
✅ **Breaking changes**: Are breaking changes documented and justified?
✅ **Performance**: Are there any performance concerns?

## 🔒 Security Considerations

Security is a top priority for this integration. Please review our [Security Policy](SECURITY.md) for:

- How to report security vulnerabilities
- Branch protection policies
- Security best practices for contributors

### Security Guidelines

When contributing:

- ❌ **Never commit sensitive data**: API keys, passwords, tokens, or personal information
- ✅ **Validate user input**: Always sanitize and validate data from configuration flows and services
- ✅ **Follow Home Assistant security guidelines**: Adhere to [Home Assistant's security best practices](https://developers.home-assistant.io/docs/security/)
- ✅ **Test security implications**: Consider how your changes might affect security
- ✅ **Use secrets properly**: Use Home Assistant's secrets management for sensitive configuration

## 📝 Code Style Guidelines

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Use type hints where appropriate

Example:
```python
async def reset_battery_level(self) -> None:
    """Reset the battery level to 100% and update the last reset time."""
    self._attr_native_value = 100
    self._last_reset = dt_util.utcnow()
    self.async_write_ha_state()
```

### Home Assistant Integration Patterns

- Use `async` for all API calls
- Follow the Home Assistant [integration quality scale](https://developers.home-assistant.io/docs/integration_quality_scale_index/)
- Use `_LOGGER` for logging (not `print()`)
- Implement proper error handling
- Use Home Assistant's utility functions (e.g., `dt_util` for datetime operations)

### YAML Files

- Use 2 spaces for indentation
- Keep files organized and well-commented
- Validate YAML syntax before committing

## 🧪 Testing Guidelines

While automated tests are not currently configured, manual testing is essential:

### Manual Testing Checklist

- [ ] Fresh installation works correctly
- [ ] Configuration flow completes successfully
- [ ] All services work as expected
- [ ] Battery discharge calculates correctly
- [ ] Entities appear in Home Assistant UI
- [ ] State persists across Home Assistant restarts
- [ ] Error handling works for invalid inputs
- [ ] Existing configurations continue to work (no breaking changes)
- [ ] Device attachment works correctly (if modified)

### Test Scenarios to Consider

1. **New installation**: Clean setup from scratch
2. **Existing installation**: Upgrade from previous version
3. **Edge cases**: Invalid inputs, missing data, boundary conditions
4. **Multiple instances**: Multiple virtual batteries configured
5. **Device attachment**: Attaching to existing devices

## 📖 Documentation

Good documentation helps users and future contributors:

- Update the README.md if you add new features
- Add code comments for complex logic
- Include docstrings for public functions
- Update CHANGELOG.md with your changes (if applicable)
- Provide examples for new features

## 🐛 Reporting Bugs

Found a bug? Please help us fix it!

### Before Reporting

1. Check if the issue already exists
2. Test on the latest version
3. Verify it's not a Home Assistant core issue

### Bug Report Should Include

- Virtual Battery version
- Home Assistant version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Relevant logs (with sensitive data removed)
- Screenshots (if applicable)

### Where to Report

- **Security vulnerabilities**: Follow the [Security Policy](SECURITY.md) - do NOT open a public issue
- **Bugs and features**: Open a GitHub issue

## ✨ Feature Requests

Have an idea for a new feature?

1. **Check existing issues**: Your idea might already be proposed
2. **Open a discussion**: Describe your use case and proposed solution
3. **Wait for feedback**: The maintainer will provide guidance
4. **Submit a PR**: If approved, you're welcome to implement it

## 💬 Communication

- **GitHub Issues**: For bugs, features, and questions
- **Pull Requests**: For code contributions
- **Discussions**: For general questions and ideas

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors are valued and recognized:

- Contributors are listed in the GitHub contributors page
- Significant contributions may be highlighted in release notes
- Your GitHub profile will be linked in merged pull requests

## ❓ Questions?

If you have questions about contributing:

1. Check this guide and the [README.md](README.md)
2. Review the [Security Policy](SECURITY.md)
3. Look at existing pull requests for examples
4. Open a GitHub issue if you need clarification

## 📚 Helpful Resources

- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Home Assistant Integration Development](https://developers.home-assistant.io/docs/creating_component_index)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [GitHub Pull Request Documentation](https://docs.github.com/en/pull-requests)

---

Thank you for contributing to Virtual Battery for Home Assistant! Your efforts help make this integration better for everyone. 🚀
