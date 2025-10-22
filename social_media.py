import base64
import hashlib
import time
import secrets
import string
import requests
import json
from urllib.parse import urlencode

class SocialMedia:
    AUTH_URL = "https://twitter.com/i/oauth2/authorize"
    TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
    API_BASE  = "https://api.twitter.com/2"

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 scopes: str = "tweet.read tweet.write users.read offline.access",
                 token_store_path: str = ""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.token_store_path = token_store_path  # ✅ ADD THIS LINE

        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self._code_verifier = None
        self._state = None

    # ---------- PKCE helpers ----------
    @staticmethod
    def _random_string(n=64):
        alphabet = string.ascii_letters + string.digits + "-._~"
        return "".join(secrets.choice(alphabet) for _ in range(n))

    @staticmethod
    def _sha256_b64url(data: str) -> str:
        digest = hashlib.sha256(data.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    def new_auth_flow(self) -> str:
        """Start a new auth flow; returns the authorization URL to visit."""
        self._code_verifier = self._random_string(64)
        code_challenge = self._sha256_b64url(self._code_verifier)
        self._state = self._random_string(24)

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "state": self._state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str, state: str) -> bool:
        """Exchange the `code` for access + refresh tokens."""
        if not self._code_verifier:
            raise RuntimeError("No PKCE verifier in memory. Call new_auth_flow() first.")
        if state != self._state:
            raise ValueError("State mismatch; possible CSRF.")

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "code_verifier": self._code_verifier,
        }

        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret) if self.client_secret else None
        resp = requests.post(self.TOKEN_URL, data=data, auth=auth, timeout=30)
        if resp.status_code != 200:
            print(f"❌ Token exchange failed: {resp.status_code} {resp.text}")
            return False
        self._store_tokens(resp.json())
        return True

    def refresh_access_token(self) -> bool:
        if not self.refresh_token:
            print("No refresh_token available.")
            return False

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret) if self.client_secret else None
        resp = requests.post(self.TOKEN_URL, data=data, auth=auth, timeout=30)
        if resp.status_code != 200:
            print(f"❌ Refresh failed: {resp.status_code} {resp.text}")
            return False
        self._store_tokens(resp.json())
        return True

    def _store_tokens(self, payload: dict):
        # ✅ First store tokens in memory
        self.access_token = payload.get("access_token")
        self.refresh_token = payload.get("refresh_token") or self.refresh_token
        expires_in = payload.get("expires_in")
        self.expires_at = int(time.time()) + int(expires_in) if expires_in else None

        # ✅ Then persist them to disk (if path is provided)
        if getattr(self, "token_store_path", None):
            with open(self.token_store_path, "w", encoding="utf-8") as f:
                json.dump({
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "expires_at": self.expires_at,
                }, f, indent=2)

    def _ensure_token(self) -> bool:
        if self.access_token and (self.expires_at is None or time.time() < self.expires_at - 60):
            return True
        if self.refresh_token:
            return self.refresh_access_token()
        print("❌ Not authorized. Start the flow at /start.")
        return False

    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}

    # ---------- Public API ----------
    def login(self) -> bool:
        if not self._ensure_token():
            return False
        r = requests.get(f"{self.API_BASE}/users/me", headers=self._auth_headers(), timeout=30)
        if r.status_code == 200:
            user = r.json().get("data", {})
            print(f"✅ Logged in as @{user.get('username')} (id={user.get('id')})")
            return True
        print(f"❌ Login check failed: {r.status_code} {r.text}")
        return False

    def create_post(self, text: str) -> dict | None:
        if not self._ensure_token():
            return None
        r = requests.post(f"{self.API_BASE}/tweets", json={"text": text}, headers=self._auth_headers(), timeout=30)
        if r.status_code in (200, 201):
            return r.json()
        print(f"❌ Post failed: {r.status_code} {r.text}")
        return None

    def logout(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
