from typing import Any, Dict, List, Optional

from httpx import AsyncClient, HTTPError, Response

from weaviate.collections.classes.config import DataType
from weaviate.connect import ConnectionV4
from weaviate.exceptions import WeaviateConnectionError


class _GFLBase:
    def __init__(self, connection: ConnectionV4, name: str):
        self._connection = connection
        self._name = name
        self._gfl_host = "https://gfl.labs.weaviate.io"
        self._headers = {"Content-Type": "application/json"}

        # Store token for use in request body instead of headers
        self._token = self._connection.get_current_bearer_token().replace("Bearer ", "")

        # Create a new AsyncClient for the GFL host
        self._client = AsyncClient(
            base_url=self._gfl_host,
            headers=self._headers,
        )

    async def close(self) -> None:
        await self._client.aclose()

    # Implement the request methods
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Response:
        try:
            response = await self._client.get(path, params=params)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"GET request failed: {e}") from e

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Response:
        try:
            response = await self._client.post(path, json=json)
            if response.status_code == 422:
                print(f"Response content: {response.text}")  # Add this debug line
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"POST request failed: {e}") from e

    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Response:
        try:
            response = await self._client.put(path, json=json)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"PUT request failed: {e}") from e

    async def delete(self, path: str) -> Response:
        try:
            response = await self._client.delete(path)
            response.raise_for_status()
            return response
        except HTTPError as e:
            raise WeaviateConnectionError(f"DELETE request failed: {e}") from e


class _GFLAsync(_GFLBase):
    async def create(
        self,
        property_name: str,
        data_type: DataType,
        view_properties: List[str],
        instruction: str,
        uuids: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        tenant: Optional[str] = None,
        model: str = "weaviate",
        api_key_for_model: Optional[str] = None,
    ) -> None:
        await self.post(
            "/gfls/create",
            json={
                "uuids": uuids,
                "collection": self._name,
                "instruction": instruction,
                "on_properties": [
                    {
                        "name": property_name,
                        "data_type": data_type.value,
                    }
                ],
                "view_properties": view_properties,
                "weaviate": {
                    "url": self._connection.url,
                    "key": self._token,
                },
                "headers": headers,
                "tenant": tenant,
                "model": model,
                "api_key_for_model": api_key_for_model,
            },
        )

    async def update(
        self,
        instruction: str,
        view_properties: List[str],
        on_properties: List[str],
        uuids: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        tenant: Optional[str] = None,
        model: str = "weaviate",
        api_key_for_model: Optional[str] = None,
    ) -> None:
        await self.post(
            "/gfls/update",
            json={
                "uuids": uuids,
                "collection": self._name,
                "instruction": instruction,
                "on_properties": on_properties,
                "view_properties": view_properties,
                "weaviate": {
                    "url": self._connection.url,
                    "key": self._token,
                },
                "headers": headers,
                "tenant": tenant,
                "model": model,
                "api_key_for_model": api_key_for_model,
            },
        )

    async def delete_object(self, instruction: str, view_properties: List[str]) -> None:
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
