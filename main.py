import requests

class IncapsulaGen():
    def __init__(self, session: requests.Session, script: str, user_data: dict[str, Any]) -> None:
        self._session: requests.Session = requests.Session()
        self.script: str = script
    
    def create_data(self) -> None:
        return None