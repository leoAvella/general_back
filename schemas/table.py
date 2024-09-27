from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SortOption(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'

class SizeOption(str, Enum):
    TEN = 10
    TWENTY = 20
    FIFTY = 50


class TableParams(BaseModel):
    page: int = 0
    #size: SizeOption = SizeOption.TEN
    size: int = 10
    sort: SortOption = SortOption.ASC
    sortby: Optional[str]

class TableResponse(TableParams):
    total_elements: int
    total_pages: int
    content: List[Any]
        
    
class AllParams(BaseModel):
    params_model: Optional[Dict[str, Any]]
    params_table: Optional[TableParams]
    
        