"""
A REALLY basic IGDB.com request wrapper that handles authentication.
"""

# Aiohttp imports
from aiohttp import ClientSession, ClientResponseError, ClientResponse
from aiohttp_client_cache import CachedSession, CacheBackend

# Utility imports
from datetime import datetime, timedelta
from typing import Literal, Any
import backoff
import asyncio

baseUrl = "https://api.igdb.com/v4"


# Create the client
class Client:
    def __init__(self, clientSecret: str, clientId: str) -> None:
        """A basic IGDB authentication wrapper

        Args:
            cache (CacheBackend): The cache to save requests to. <- THIS IS REQUIRED!
        """

        self.clientSecret = clientSecret
        self.clientId = clientId
        self.accessToken: str | None = None
        self.expiryDate: datetime = datetime.now() - timedelta(days=1)

    async def authenticate(self) -> None:
        """Generates a authentication token for IGDB.com

        Args:
            clientSecret (str): The client's secret
            clientId (str): The client's id
        """
        async with ClientSession(base_url="https://id.twitch.tv") as session:
            # Fetch the authentication token
            resp = await session.post(
                "/oauth2/token",
                params={
                    "client_id": self.clientId,
                    "client_secret": self.clientSecret,
                    "grant_type": "client_credentials",
                },
            )

            # Raise any errors
            resp.raise_for_status()

            # Get the request's data
            data: dict = await resp.json()

            # Store the expiry date and authentication token
            self.accessToken = data.get("access_token", None)
            self.expiryDate = datetime.now() + timedelta(
                seconds=int(data.get("expires_in", 1))
            )

    @backoff.on_exception(
        backoff.expo,
        ClientResponseError,
        max_tries=3,
        max_time=60,
    )
    async def request(
        self,
        route: str,
        method: Literal["get", "post", "put", "patch", "delete"],
        clientSession: ClientSession | CachedSession = None,
        params: dict = {},
        body: str = None,
    ) -> dict | list:
        """Makes a request to IGDB.com using the provided session. (Will create a session if not provided)"""
        if not clientSession:
            clientSession = ClientSession()

        async with clientSession as session:

            # Check if the token has expired or doesn't exist
            if not self.accessToken or (datetime.now() > self.expiryDate):
                await self.authenticate()

            # Fetch the data from IGDB.com
            resp: ClientResponse = await session.request(
                method,
                baseUrl + route,
                headers={
                    "Client-ID": self.clientId,
                    "Authorization": f"Bearer {self.accessToken}",
                },
                params=params,
                data=body,
            )

            # Raise any errors
            resp.raise_for_status()

            # Get the request's data
            data: dict = await resp.json()

            return data
