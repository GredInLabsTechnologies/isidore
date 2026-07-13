"""Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by the graph)."""
import hmac


def verify_jwt(token, secret):
    """Return the decoded claims if the token's signature checks out, else None."""
    if not token or not secret:
        return None
    expected = hmac.new(secret.encode(), token.encode(), "sha256").hexdigest()
    if not hmac.compare_digest(expected, token.rsplit(".", 1)[-1]):
        return None
    return {"sub": token.split(".", 1)[0]}
