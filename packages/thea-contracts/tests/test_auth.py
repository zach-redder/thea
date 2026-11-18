from thea_contracts.auth import token_matches


def test_matching_token() -> None:
    assert token_matches("s3cret", "s3cret")


def test_fails_closed_without_a_configured_token() -> None:
    assert not token_matches("anything", None)
    assert not token_matches("", "")


def test_non_ascii_input_is_a_mismatch_not_a_crash() -> None:
    assert not token_matches("tökén", "token")
