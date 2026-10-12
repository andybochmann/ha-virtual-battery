# Contributing

Bug reports, fixes and translations are welcome.

## Reporting a bug

Open an issue with the integration version, the Home Assistant version, the steps to reproduce, and the relevant log lines (logger `custom_components.virtual_battery`). For security problems, see [SECURITY.md](SECURITY.md).

## Making a change

1. Fork the repository and create a branch, for example `fix/...`, `feat/...` or `docs/...`.
2. Keep the change focused and follow the existing code style.
3. Write commit messages in [Conventional Commits](https://www.conventionalcommits.org/) style, for example `fix: ...` or `feat: ...`.
4. When you change text in the UI, update all three files in `custom_components/virtual_battery/translations/` (en, de, fr).
5. Add a line under `[Unreleased]` in `CHANGELOG.md` for changes users will notice.
6. Open a pull request that says what changed and why, and link the issue (`Closes #123`).

Pull requests run hassfest and HACS validation.

## Testing

There are no automated tests yet, so test in a real Home Assistant. Docker is the quickest way, with your copy of the integration mounted:

```bash
docker run -d --name ha-dev -p 8123:8123 \
  -v "$PWD/ha-config:/config" \
  -v "$PWD/custom_components:/config/custom_components" \
  ghcr.io/home-assistant/home-assistant:stable
```

Open http://localhost:8123, add a Virtual Battery, and check:

- setup and the options flow
- the services and the reset button
- the battery level and time sensors across a Home Assistant restart
- that a battery created with the previous release still works after updating
- attaching to an existing device, if your change touches it
