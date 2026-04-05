from abc import ABC, abstractmethod

class LoaderStrategy(ABC):
    @abstractmethod
    def load(self, path: str):
        """ Standard method for all loader"""
        pass
