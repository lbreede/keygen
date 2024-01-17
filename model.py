import logging

logger = logging.getLogger(__name__)


class Model:
    KEY_LENGTH = 15
    assert KEY_LENGTH % 5 == 0

    def check_key(self, seed: str, key: str) -> bool:
        is_valid = key == self.generate_key(seed)
        if is_valid:
            logger.info("Key %r is valid", key)
        else:
            logger.warning("Key %r is invalid", key)
        return is_valid

    def keygen(self, seed: str) -> str:
        # TODO: Write better keygen
        pass

    def generate_key(self, seed: str) -> str:
        logger.debug("Generating key for seed %r", seed)
        key = seed.upper()
        logger.debug("Key to uppercase:       %r", key)

        key = "".join(key[c % len(key)] for c in range(self.KEY_LENGTH))
        logger.debug("Filled to length %02d:    %r", self.KEY_LENGTH, key)

        key = (
            key.replace("0", "A")
            .replace("1", "B")
            .replace("2", "C")
            .replace("3", "D")
            .replace("4", "E")
            .replace("5", "F")
            .replace("6", "G")
            .replace("7", "H")
            .replace("8", "I")
            .replace("9", "J")
        )
        logger.debug("Replaced digits:        %r", key)

        # TODO: Give additional rotation based on char index
        num = sum(ord(c) for c in key) % 26
        key = self.rot(key, num)
        logger.debug("Rotated by %02d:          %r", num, key)

        key = "".join(c if i % 2 == 0 else str(ord(c))[-1] for i, c in enumerate(key))
        logger.debug("Replaced odd chars:     %r", key)
        return key

    @staticmethod
    def rot(text: str, n: int) -> str:
        assert all(c.isupper() for c in text)
        return "".join(chr((ord(c) - ord("A") + n) % 26 + ord("A")) for c in text)

    @staticmethod
    def rot13(text: str) -> str:
        assert all(c.isupper() for c in text)
        return "".join(chr((ord(c) - ord("A") + 13) % 26 + ord("A")) for c in text)

    def add_dashes(self, text: str) -> str:
        magic_number = self.KEY_LENGTH // 5
        for i in range(4):
            n = (i + 1) * magic_number + i
            if len(text) > n:
                text = text[:n] + "-" + text[n:]
        return text

    def generate_key_with_dashes(self, seed: str) -> str:
        return self.add_dashes(self.generate_key(seed))
