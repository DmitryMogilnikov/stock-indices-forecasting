from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    
    @abstractmethod
    def delete_key():
        pass
