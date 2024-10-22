from typing import Any, Dict, List, Optional, Union

from httpx import (
    AsyncClient,
    HTTPError,
    Response,
)

from weaviate.auth import AuthApiKey, AuthCredentials
from weaviate.collections.classes.config import DataType
from weaviate.config import Proxies
from weaviate.connect import ConnectionParams
from weaviate.connect.base import _ConnectionBase, _get_proxies
from weaviate.exceptions import AuthenticationFailedError, WeaviateConnectionError


class _GFLConnection(_ConnectionBase):
    """
    Connection class used to communicate with a GFL instance.
    """

    def __init__(
        self,
        connection_params: ConnectionParams,
        auth_client_secret: Optional[AuthCredentials] = None,
        proxies: Optional[Union[str, Proxies]] = None,
        trust_env: bool = True,
        additional_headers: Optional[Dict[str, Any]] = None,
    ):
        self.url = connection_params._http_url
        self._auth = auth_client_secret
        self._headers = {"Content-Type": "application/json"}

        if additional_headers:
            self._headers.update(additional_headers)

        # Handle authentication
        if auth_client_secret is not None:
            if isinstance(auth_client_secret, AuthApiKey):
                self._headers["Authorization"] = f"Bearer {auth_client_secret.api_key}"
            else:
                # Handle other types of authentication if needed
                raise AuthenticationFailedError(
                    "Unsupported authentication method for GFL connection"
                )

        self._proxies = _get_proxies(proxies, trust_env)
        self._trust_env = trust_env
        self._client = AsyncClient(
            headers=self._headers,
            proxies=self._proxies,
            trust_env=self._trust_env,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        error_msg: str = "",
    ) -> Response:
        url = self.url + path
        try:
            response = await self._client.get(url, params=params, headers=self._headers)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"{error_msg}: {e}") from e

    async def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        error_msg: str = "",
    ) -> Response:
        url = self.url + path
        try:
            response = await self._client.post(url, json=json, headers=self._headers)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"{error_msg}: {e}") from e

    async def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        error_msg: str = "",
    ) -> Response:
        url = self.url + path
        try:
            response = await self._client.put(url, json=json, headers=self._headers)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"{error_msg}: {e}") from e

    async def delete(
        self,
        path: str,
        error_msg: str = "",
    ) -> Response:
        url = self.url + path
        try:
            response = await self._client.delete(url, headers=self._headers)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"{error_msg}: {e}") from e


class _GFLBase:
    def __init__(self, connection: _GFLConnection, name: str):
        self._connection = connection
        self._name = name
        self._gfl_host = "http://localhost:8080"
        self._headers = {"Content-Type": "application/json"}


class _GFLAsync(_GFLBase):
    async def create(
        self, property_name: str, data_type: DataType, view_properties: List[str], instruction: str
    ) -> None:
        # Temporarily print connection details
        print(f"Connection URL: {self._connection.url}")
        print(f"Collection Name: {self._name}")
        print(f"GFL Host: {self._gfl_host}")
        print(f"Property Name: {property_name}")
        print(f"Data Type: {data_type}")
        print(f"View Properties: {view_properties}")
        print(f"Instruction: {instruction}")
        print(f"Headers: {self._headers}")
        # await self._connection.post(
        #     "/create",
        #     json={
        #         "property_name": property_name,
        #         "data_type": data_type,
        #         "view_properties": view_properties,
        #         "instruction": instruction,
        #     },
        # )

    async def update(self, name: str, view_properties: List[str], instruction: str) -> None:
        # Implementation for update
        pass

    async def delete_object(self, instruction: str, view_properties: List[str]) -> None:
        # Implementation for delete_object
        pass

    # Add other GFL-related methods as needed


class _GFLCreateOperationAsync:
    def __init__(self, gfl_collection: _GFLAsync):
        self._gfl_collection = gfl_collection

    async def with_hybrid_search(
        self, query: str, alpha: float, limit: int, properties: List[str]
    ) -> "_GFLCreateOperationAsync":
        # Implementation for with_hybrid_search
        return self

    async def with_filters(self, filters: dict) -> "_GFLCreateOperationAsync":
        # Implementation for with_filters
        return self
