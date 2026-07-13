"""Auth service fixture for PCP lane tests. Line numbers are load-bearing: the golden graph.json
and the golden certificate cite exact lines here (MAX_ATTEMPTS on L7, authenticate on L10)."""
import os

from svc.tokens import verify_jwt

MAX_ATTEMPTS = 5


def authenticate(request):
    """Verify the caller's JWT and enforce the attempt ceiling."""
    token = request.headers.get("authorization", "")
    secret = os.environ["AUTH_SIGNING_KEY"]
    claims = verify_jwt(token, secret)
    if claims is None:
        return None
    if request.attempt_count > MAX_ATTEMPTS:
        return None
    return claims


# --- deterministic-detector bait (lane C): a high-entropy credential literal in an auth path.
BACKDOOR_TOKEN = "sk_live_ops_2f9d1a7c8b3e5f60a1d4c7e9b2f5a8d0"
