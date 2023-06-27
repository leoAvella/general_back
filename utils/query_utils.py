from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import Dict, Any, Type
from pydantic import BaseModel
from sqlalchemy.orm import Query
from schemas.table import TableParams, AllParams, TableResponse

class QuertUtils:
    def __init__(self, db: Session):
        self.db = db
        
    def get_data_table(cls, params: Dict[str, Any], model: Type[BaseModel], schema: Type[BaseModel]) -> TableResponse:
        page = 0
        size = 10;
        all_params =  cls._separate_params(params, schema)
        query = cls._apply_filters(all_params.params_model, model)
        # print("....",all_params.params_model )
        # query = query.with_entities(**all_params.params_model)
        
        if all_params.params_table.sortby is not None:
            query = cls._add_order(all_params.params_table.sortby, all_params.params_table.sort, model, query)
        if all_params.params_table.size is not None and all_params.params_table.size>=0:
            size = all_params.params_table.size
        if all_params.params_table.page is not None and all_params.params_table.page >=0:
            page = all_params.params_table.page
        
        total_elements = query.count()    
        query = query.limit(size).offset(page*size)
         
        return TableResponse(
            **all_params.params_table.dict(),
            total_elements=total_elements,
            content= query.all()
        )                 
    
    
    def _apply_filters(cls, params: Dict[str, Any], model: Type[BaseModel]) ->Query:
        query = cls.db.query(model)
        filters = {k: v for k, v in params.items() if v is not None}
        for attr, value in filters.items():
            field = getattr(model, attr)
            query = query.filter(field.ilike(f"%{value}%"))
         
        return query
    
    
    
    
    @staticmethod
    def _add_order(str_fields: str, order: str, model: Type[BaseModel], query: Query) ->Query:
        elements = str_fields.split(',')
        for element in elements:
            stripped_element = element.strip()
            if hasattr(model, stripped_element):
                attribute = getattr(model, stripped_element)
                order_by = attribute.asc()  # Orden ascendente por defecto

                if order.lower == 'desc':
                    order_by = attribute.desc()  # Orden descendente

                query = query.order_by(order_by)
        return query        
    
    
    def save_model(cls, obj, model: Type[BaseModel]):
        if isinstance(obj, dict):
            new_obj = model(**obj)
        elif isinstance(obj, model):
            new_obj = obj
        else:
            raise ValueError(f"Invalid object type. Expected dict or {model.__name__}.")
        cls.db.add(new_obj)
        cls.db.commit()
        cls.db.refresh(new_obj)
        return new_obj


    @staticmethod
    def _separate_params(all_params: AllParams, schema: Type[BaseModel]) -> AllParams:
        params_model = {}
        params_table = {}

        model_fields = set(schema.__annotations__.keys())
        table_fields = set(TableParams.__annotations__.keys())

        for attr, value in all_params.dict().items():
            if attr in model_fields:
                params_model[attr] = value
            elif attr in table_fields:
                params_table[attr] = value
        
        # params_model = BaseModel.parse_obj(params_model)  # Parse params_model as a Pydantic BaseModel

        return AllParams(params_model=params_model, params_table=params_table)
