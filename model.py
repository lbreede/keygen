import base64
import hashlib
import logging
from typing import Protocol
from string import digits
import random
import time
from tqdm import trange
import re

logger = logging.getLogger(__name__)


class KeyManager(Protocol):
    def validate_key(self, key: str) -> bool:
        ...

    def generate_key(self) -> str:
        ...

    def format_key(self, key: str) -> str:
        ...


class Win95KeyManager:
    BAD_PREFIXES = {"333", "444", "555", "666", "777", "888", "999"}

    def validate_key(self, key: str) -> bool:
        pattern = re.compile(r"^(\d{3})-(\d{7}$)")
        if (match := pattern.match(key)) is None:
            logger.debug(
                "INVALID: %s - The key must be in the format of XXX-XXXXXXX.", key
            )
            return False
        prefix, suffix = match.groups()

        if prefix in self.BAD_PREFIXES:
            logger.debug(
                "INVALID: %s - The first 3 characters must not equal to 333, 444, 555, "
                "666, 777, 888 or 999.",
                key,
            )
            return False

        if "9" in suffix:
            logger.debug(
                "INVALID: %s - The last 7 characters must all be numbers from 0-8.", key
            )
            return False

        if sum(int(x) for x in suffix) % 7:
            logger.debug(
                "INVALID: %s - The sum of the last 7 numbers must be divisible by 7 "
                "with no remainder.",
                key,
            )
            return False

        logger.debug("  VALID: %s - All checks passed. ✨", key)
        return True

    def generate_key(self) -> str:
        prefix = suffix = None
        while prefix is None or prefix in self.BAD_PREFIXES:
            prefix = "".join(random.choice(digits) for _ in range(3))
        while suffix is None or sum(int(x) for x in suffix) % 7:
            suffix = "".join(random.choice("012345678") for _ in range(7))
        return f"{prefix}-{suffix}"

    def format_key(self, key: str) -> str:
        key = "".join(x for x in key if x.isdigit())
        if len(key) >= 3:
            key = key[:3] + "-" + key[3:]
        key = key[:11]
        return key

    def speed_test(self, iterations: int = 1_000_000) -> None:
        start = time.time()
        for _ in trange(iterations):
            assert self.validate_key(self.generate_key())
        duration = time.time() - start
        print(f"Validated {iterations:,} keys in {duration:.2f} seconds.")


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


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    print(Win95KeyManager().format_key("11aaaaaaa2362457724574511111"))


if __name__ == "__main__":
    main()
