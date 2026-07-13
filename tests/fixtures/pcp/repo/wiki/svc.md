# svc

The `svc` module authenticates callers. `authenticate` verifies the caller's JWT through
`verify_jwt` and enforces the `MAX_ATTEMPTS` ceiling before returning the decoded claims.

The signing secret is read from the environment, never hard-coded into the request path.

```isidore-claims
authenticate verifies the JWT by calling verify_jwt | svc/auth.py:14 | calls:authenticate;verify_jwt
the attempt ceiling MAX_ATTEMPTS is 5 | svc/auth.py:7 | value:MAX_ATTEMPTS;5
the auth module imports the tokens service | svc/auth.py:5 | imports:svc/auth.py;svc/tokens.py
authenticate reads the AUTH_SIGNING_KEY environment variable | svc/auth.py:13 | env:AUTH_SIGNING_KEY
the auth module defines authenticate | svc/auth.py:10 | defines:svc/auth.py;authenticate
authenticate returns None when the token is invalid | svc/auth.py:16 |
```
