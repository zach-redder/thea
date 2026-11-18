"""The single token check every service uses, so the comparison rules can't drift between them."""

import secrets


def token_matches(provided: str | None, expected: str | None) -> bool:
    """Constant-time comparison. Fails closed: no configured token means nothing matches.

    Compares bytes, not str: compare_digest raises TypeError on non-ASCII str,
    which would turn a bad token into a 500 instead of a 401.
    """
    if not provided or not expected:
        return False
    return secrets.compare_digest(
        provided.encode("utf-8", "surrogateescape"),
        expected.encode("utf-8", "surrogateescape"),
    )
