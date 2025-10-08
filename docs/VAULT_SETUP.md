# Vault (HashiCorp) setup for Exchange API keys

This document shows a minimal example for storing exchange credentials in HashiCorp Vault (KV v2) and how to make them available to the `APIKeyManager` used by PulseBot.

## Example secret layout (KV v2)

Store secrets under `secret/data/exchanges/<exchange_name>`.
Example for Binance (KV v2):

Path: `secret/data/exchanges/binance`

Data (JSON payload for KV v2):

```
{ "data": { "api_key": "<your-key>", "api_secret": "<your-secret>" } }
```

`APIKeyManager` will attempt to read KV v2 using `secrets.kv.v2.read_secret_version(path=...)` and expects fields named `api_key`/`api_secret` (or `key`/`secret`). Adjust your Vault policies and paths to match.

## CI / GitHub Actions

- Add `VAULT_ADDR` and `VAULT_TOKEN` as repository secrets in GitHub (or configure an AppRole and export the role's credentials during CI). The `APIKeyManager` constructor reads `VAULT_ADDR` and `VAULT_TOKEN` from env vars by default.
- If your CI cannot access Vault, consider injecting per-environment keys using GitHub Secrets (e.g., `BINANCE_API_KEY`, `BINANCE_SECRET`) only for protected branches.
- The release workflow contains an optional PyPI publish step that runs only when `secrets.PYPI_API_TOKEN` is set. To enable automated PyPI publishing, add a `PYPI_API_TOKEN` secret.

## Minimal Vault policy example

This is an example Vault policy granting read access to the exchange secrets path (tweak as needed):

```
path "secret/data/exchanges/*" {
  capabilities = ["read"]
}
```

## Notes

- Prefer least-privilege secrets and short-lived credentials (rotate keys and Vault tokens regularly).
- For production, prefer AppRole or Vault agents instead of raw tokens in CI.
