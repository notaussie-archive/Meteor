# Import types
from beanie import Document
from pydantic import BaseModel, Field
from typing import Annotated


# Create config model
class Config(BaseModel):
    prefix: Annotated[
        str,
        Field(
            max_length=20,
            description="The server prefix",
        ),
    ] = "_bot-prefix_"


# Create server document
class Server(Document):

    config: Config = Config(prefix="test!")
