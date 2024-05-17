from typing import TypedDict
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration values for servers"""

    loggingChannel: str | None


@dataclass
class Server:
    serverId: str

    config: Config


Server("test", Config("testing"))
