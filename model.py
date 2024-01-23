import base64
import hashlib
import logging

logger = logging.getLogger(__name__)


class Model:
    def __init__(self):
        self.key_length = 25
        assert self.key_length % 5 == 0

    def check_key(self, input_data: str, key: str) -> bool:
        if len(key) < self.key_length:
            logger.warning("Key %r is too short", self.add_dashes(key))
            return False

        if len(key) > self.key_length:
            # This should never happen
            logger.warning("Key %r is too long", self.add_dashes(key))
            return False

        if key != self.generate_key(input_data):
            logger.warning("Key %r is invalid", self.add_dashes(key))
            return False

        logger.info("Key %r is valid", self.add_dashes(key))
        return True

    def generate_key(self, input_data: str, add_dashes: bool = False) -> str:
        logger.debug("Generating key for seed %r", input_data)
        sha256_hash = hashlib.sha256(input_data.encode()).digest()
        key = base64.urlsafe_b64encode(sha256_hash).decode("utf-8")
        key = "".join(char for char in key if char.isalnum())
        # Highly unlikely that the key is less than 25 characters at this point.
        # However, if it is, we'll pad it with X's.
        key = key.ljust(self.key_length, "X")
        key = key[: self.key_length]
        key = key.upper()
        if add_dashes:
            key = self.add_dashes(key)
        return key

    def add_dashes(self, text: str) -> str:
        magic_number = self.key_length // 5
        for i in range(4):
            n = (i + 1) * magic_number + i
            if len(text) > n:
                text = text[:n] + "-" + text[n:]
        return text
