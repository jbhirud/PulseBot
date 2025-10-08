# Security and Secrets

Recommendations for handling production credentials:

- Use GitHub Secrets for storing API keys and secrets used in CI and Actions.
- For runtime secrets in production, prefer a secrets manager such as HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault.
- Do NOT store API keys or secrets in the repository or in plain text config files.
- Rotate keys periodically and enforce least privilege for credentials.

CI usage

- Use repository secrets to populate environment variables in Actions workflows (Settings → Secrets).
- Avoid printing secrets in logs.
