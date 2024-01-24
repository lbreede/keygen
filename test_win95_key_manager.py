from model import Win95KeyManager

win95_key_manager = Win95KeyManager()


def test_validate_key() -> None:
    assert win95_key_manager.validate_key("111-1111111")
