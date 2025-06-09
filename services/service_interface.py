from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    def register_user(self, username: str, email: str, password: str):
        pass

    @abstractmethod
    def login_user(self, username: str, password: str):
        pass
