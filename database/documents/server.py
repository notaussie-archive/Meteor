# Import types
from beanie import Document
from pydantic import BaseModel, Field
from typing import Annotated


# Create server document
class Server(Document):
    serverId: str
