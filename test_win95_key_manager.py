from model import Win95KeyManager

win95_key_manager = Win95KeyManager()


def test_validate_key() -> None:
    assert win95_key_manager.validate_key("111-1111111")


def test_generate_key() -> None:
    assert win95_key_manager.generate_key()


def test_format_key() -> None:
    assert win95_key_manager.format_key("111-1111111") == "111-1111111"
    assert win95_key_manager.format_key("1111111111") == "111-1111111"
    assert win95_key_manager.format_key("ABC-1234567890") == "123-4567890"
    assert win95_key_manager.format_key("ABC") == ""
