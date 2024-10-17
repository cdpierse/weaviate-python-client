from typing import List, Optional

from weaviate.collections.classes.config import DataType
from weaviate.collections.gfl.gfl import _GFLBase

class _GFL(_GFLBase):
    def create(
        self, property_name: str, data_type: DataType, view_properties: List[str], instruction: str
    ) -> None: ...
    def update(self, name: str, view_properties: List[str], instruction: str) -> None: ...
    def delete_object(self, instruction: str, view_properties: List[str]) -> None: ...
