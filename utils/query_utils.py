from typing import Any, Dict, Type

from pydantic import BaseModel
from sqlalchemy import inspect, text
from sqlalchemy.orm import Query, Session

from schemas.table import AllParams, TableParams, TableResponse
from typing import Optional, Type

class QuertUtils:
    def __init__(self, db: Session):
        self.db = db

    def get_model_by_id(self, id: int, model: Type[BaseModel]) -> Optional[BaseModel]:
        result: Optional[BaseModel] = self.db.query(model).get(id)
        return result

    def save_model(self, obj: Any, model: Type[BaseModel]) -> BaseModel:
        if isinstance(obj, dict):
            new_obj = model(**obj)
        elif isinstance(obj, model):
            new_obj = obj
        else:
            raise ValueError(f"Tipo de objeto no válido. Se esperaba un dict o {model.__name__}.")
        self.db.add(new_obj)
        self.db.commit()
        self.db.refresh(new_obj)
        return new_obj

    def update_model(self, id: int, obj: Any, model: Type[BaseModel]) -> BaseModel:
        row = self.get_model_by_id(id, model)
        if row:
            for key, value in obj.items():
                setattr(row, key, value)
            self.db.commit()
        return row

    def get_data_table(cls, params: Dict[str, Any], model: Type[BaseModel], schema: Type[BaseModel]) -> TableResponse:
        all_params = cls._separate_params(params, schema)
        query = cls._apply_filters(all_params.params_model, model, schema)

        if all_params.params_table.sortby is not None:
            query = cls._add_order(all_params.params_table.sortby, all_params.params_table.sort, model, query)
        if all_params.params_table.size is None or all_params.params_table.size <= 0:
            all_params.params_table.size = 10
        if all_params.params_table.page is None or all_params.params_table.page < 0:
            all_params.params_table.page = 0

        total_elements = query.count()
        page = all_params.params_table.page -1 if int(all_params.params_table.page) >=1 else 0
        query = query.limit(all_params.params_table.size).offset(page * all_params.params_table.size)
        d = total_elements / all_params.params_table.size
        tp = d if d == 0 else d+1
        return TableResponse(**all_params.params_table.dict(), total_elements=total_elements, total_pages=tp, content=query.all())

    def _apply_filters(cls, params: Dict[str, Any], model: Type[BaseModel], schema: Type[BaseModel]) -> Query:
        query = cls.db.query(*[getattr(model, attr) for attr in schema.__annotations__.keys()])
        filters = {k: v for k, v in params.items() if v is not None}
        for attr, value in filters.items():
            field = getattr(model, attr)
            query = query.filter(field.ilike(f"%{value}%"))

        return query

    @staticmethod
    def _add_order(str_fields: str, order: str, model: Type[BaseModel], query: Query) -> Query:
        elements = str_fields.split(",")
        for element in elements:
            stripped_element = element.strip()
            if hasattr(model, stripped_element):
                attribute = getattr(model, stripped_element)
                order_by = attribute.asc()  # Orden ascendente por defecto

                if order.lower == "desc":
                    order_by = attribute.desc()  # Orden descendente

                query = query.order_by(order_by)
        return query

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

        return AllParams(params_model=params_model, params_table=params_table)
