import os
from typing import Optional, Dict
import importlib


class APIKeyManager:
    """Small abstraction for retrieving API keys.

    - In production, it will fetch secrets from HashiCorp Vault (via hvac).
    - In development, it falls back to environment variables.

    Example usage:
        mgr = APIKeyManager(vault_addr=os.environ.get('VAULT_ADDR'))
        keys = mgr.get_keys('binance')
    """

    def __init__(self, vault_addr: Optional[str] = None, token: Optional[str] = None):
        self.vault_addr = vault_addr or os.environ.get('VAULT_ADDR')
        self.token = token or os.environ.get('VAULT_TOKEN')
        self._client = None
        # Import hvac lazily so tests can inject a fake hvac module into sys.modules
        try:
            hvac = importlib.import_module('hvac')
        except Exception:
            hvac = None

        if self.vault_addr and hvac is not None:
            try:
                self._client = hvac.Client(url=self.vault_addr, token=self.token)
            except Exception:
                # If hvac fails to initialize, keep client as None and fall back
                self._client = None

    def _from_env(self, service: str) -> Optional[Dict[str, str]]:
        api_key = os.environ.get(f"{service.upper()}_API_KEY")
        api_secret = os.environ.get(f"{service.upper()}_API_SECRET")
        if api_key and api_secret:
            return {"key": api_key, "secret": api_secret}
        return None

    def _from_vault(self, path: str) -> Optional[Dict[str, str]]:
        if not self._client:
            return None
        try:
            # Expect secrets at secret/data/<path> (KV v2) or secret/<path>
            # Try KV v2 first
            read_path = f"secret/data/{path}"
            resp = self._client.secrets.kv.v2.read_secret_version(path=path)
            data = resp.get('data', {}).get('data', {})
            key = data.get('api_key') or data.get('key')
            secret = data.get('api_secret') or data.get('secret')
            if key and secret:
                return {"key": key, "secret": secret}
        except Exception:
            try:
                # Fallback to older kv
                resp = self._client.secrets.kv.read_secret(path=path)
                data = resp.get('data', {})
                key = data.get('api_key') or data.get('key')
                secret = data.get('api_secret') or data.get('secret')
                if key and secret:
                    return {"key": key, "secret": secret}
            except Exception:
                return None
        return None

    def get_keys(self, service: str) -> Optional[Dict[str, str]]:
        """Get API keys for a service. Tries environment first, then Vault.

        Returns dict with 'key' and 'secret' or None if not found.
        """
        env = self._from_env(service)
        if env:
            return env

        # Try vault
        vault_path = f"{service}"
        vault = self._from_vault(vault_path)
        if vault:
            return vault

        return None
