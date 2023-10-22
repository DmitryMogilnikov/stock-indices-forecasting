from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def check_connection(self):
        """Check connection to DB."""

    @abstractmethod
    def get_all_keys(self) -> set[str]:
        """Extract all keys from DB."""

    @abstractmethod
    def check_existing_key(self, key: str) -> bool:
        """Check is key exists in DB"""

    @abstractmethod
    def delete_key(self, key: str) -> None:
        """Delete key from DB."""
