from typing import Any

class ModelLoaderPort:
    def load(self, path: str) -> Any:
        raise NotImplementedError
