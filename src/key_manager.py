import logging
import random
import re
import time
from string import digits
from typing import Protocol

from tqdm import trange

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
        pattern = re.compile(r"^(\d{3})-(\d{7})$")
        if (match := pattern.match(key)) is None:
            logger.debug(
                "INVALID: %s - The key must be in the format of XXX-XXXXXXX.",
                key,
            )
            return False
        prefix, suffix = match.groups()

        if prefix in self.BAD_PREFIXES:
            logger.debug(
                "INVALID: %s - The first 3 characters must not equal to 333, "
                "444, 555, 666, 777, 888 or 999.",
                key,
            )
            return False

        if "9" in suffix:
            logger.debug(
                "INVALID: %s - The last 7 characters must all be numbers from " "0-8.",
                key,
            )
            return False

        if sum(int(x) for x in suffix) % 7:
            logger.debug(
                "INVALID: %s - The sum of the last 7 numbers must be "
                "divisible by 7 with no remainder.",
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
