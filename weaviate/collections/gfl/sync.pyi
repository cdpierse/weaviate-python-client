from typing import Dict, List, Optional

from weaviate.collections.classes.config import DataType
from weaviate.collections.gfl.gfl import _GFLBase

class _GFL(_GFLBase):
    def create(
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
    ) -> None: ...
    def update(
        self,
        instruction: str,
        view_properties: List[str],
        on_properties: List[str],
        uuids: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        tenant: Optional[str] = None,
        model: str = "weaviate",
        api_key_for_model: Optional[str] = None,
    ) -> None: ...
    def delete_object(self, instruction: str, view_properties: List[str]) -> None: ...
