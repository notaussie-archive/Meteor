# Import types
from pydantic import BaseModel
from beanie import Document


class Starboard(BaseModel):

    channelId: str | None = None

    enabled: bool = False

    minimumStars: int = 5


class Config(BaseModel):

    starboard: Starboard = Starboard()


# Create server document
class Server(Document):
    serverId: str

    config: Config = Config()
