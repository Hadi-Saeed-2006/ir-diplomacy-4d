# Security Policy

## Scope

DIPLOMATIQ 4D is a portfolio project and currently does not store user credentials or require secrets for its bundled demo dataset.

## Reporting a security issue

Please do not publish sensitive credentials, tokens, private URLs, or personal data in a public issue. Report security concerns privately through GitHub's available private reporting mechanisms where enabled.

## Secret handling

- Never commit API keys or access tokens.
- Use environment variables or GitHub Secrets for future integrations.
- Keep `.env` and local secret files out of version control.

## Data integrity

External news and public datasets must be treated according to their source terms and documented with provenance before being presented as analytical inputs.
