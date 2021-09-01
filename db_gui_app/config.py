from pathlib import Path
import toml

MAIN_FOLDER = Path(__file__).parent.parent

class Config:
    def __init__(self) -> None:
        self.data = toml.load(MAIN_FOLDER / "config.toml")

    @property
    def url_schema(self):
        return self.data["database"]["url_schema"]

    @property
    def connection(self):
        return self.data["database"]["connection"]

    @property
    def relative(self):
        return self.data["database"]["relative"]

    @property
    def windowtitle(self):
        return self.data["window"]["title"]

config = Config()
