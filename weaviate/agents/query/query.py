from typing import List, Optional, Union

import httpx
from pydantic import BaseModel

from weaviate.agents.query.models import (
    AggregationResult,
    CollectionDescription,
    QueryResult,
    Usage,
)
from weaviate.client import WeaviateAsyncClient, WeaviateClient


class AggregationResultWithCollection(AggregationResult):
    collection: str


class QueryResultWithCollection(QueryResult):
    collection: str


class QueryAgentResponse(BaseModel):
    original_query: str
    collection_names: list[str]
    searches: list[list[QueryResultWithCollection]]
    aggregations: list[list[AggregationResultWithCollection]]
    usage: Usage
    total_time: float
    search_answer: str | None
    aggregation_answer: str | None
    has_aggregation_answer: bool
    has_search_answer: bool
    is_partial_answer: bool
    missing_information: list[str]
    final_answer: str


class QueryAgentError(Exception):
    """Error raised by the QueryAgent."""


class QueryAgent:
    """Agent class for performing agentic queries against Weaviate collections."""

    def __init__(
        self,
        client: Union[WeaviateClient, WeaviateAsyncClient],
        collections: List[Union[str, CollectionDescription]],
        agents_host: Union[str, None] = None,
    ):
        """Initialize a QueryAgent.

        Args:
            client: A Weaviate client instance (sync or async)
            collections: List of collection names or CollectionDescription objects the agent has access to
        """
        self._client = client
        self._connection = client._connection
        self._agents_host = agents_host or "https://api.agents.weaviate.io"
        self._collections = collections

        # check if all collections have the same URL
        self.base_url = self._client._connection.url

        self._headers = {
            "Authorization": self._connection.get_current_bearer_token().replace("Bearer ", ""),
            "X-Weaviate-Cluster-Url": self._client._connection.url.replace(":443", ""),
        }
        self._timeout = 60
        self._query_agent_url = f"{self._agents_host}/agent/query"

    def run(
        self,
        query: str,
        view_properties: Optional[List[str]] = None,
        context: Optional[QueryAgentResponse] = None,
    ) -> QueryAgentResponse:
        """Execute a agentic query against the specified collections.

        Args:
            query: The natural language query string
            view_properties: Optional list of property names which the agent has the ability to view
            context: Optional context of type QueryAgentResponse
        Returns:
            A QueryAgentResponse object containing search results and analysis
        """
        request_body = {
            "query": query,
            "collection_names": [
                c.name if isinstance(c, CollectionDescription) else c for c in self._collections
            ],
            "headers": self._connection.additional_headers,
            "collection_view_properties": view_properties,
            "limit": 20,
            "tenant": None,
            "previous_response": context.model_dump() if context else None,
        }

        response = httpx.post(
            self._query_agent_url,
            headers=self._headers,
            json=request_body,
            timeout=self._timeout,
        )

        if response.status_code != 200:
            raise QueryAgentError(
                f"Query agent returned status code {response.status_code} with response {response.text}"
            )

        return QueryAgentResponse(**response.json())
