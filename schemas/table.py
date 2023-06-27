from enum import Enum
from typing import Optional
from pydantic import BaseModel
from typing import Dict, Any, List

class SortOption(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'



class TableParams(BaseModel):
    page: int = 0
    size: int = 10
    sort: SortOption = SortOption.ASC
    sortby: Optional[str]

class TableResponse(TableParams):
    total_elements: int
    content: List[Any]
        
    
class AllParams(BaseModel):
    params_model: Optional[Dict[str, Any]]
    params_table: Optional[TableParams]
    
        