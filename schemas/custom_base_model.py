from pydantic import BaseModel, validate_model
from pydantic.error_wrappers import ErrorWrapper

class CustomBaseModel(BaseModel):
    def validate(self):
        errors = validate_model(self)
        error_messages = []
        for error in errors:
            if isinstance(error, ErrorWrapper):
                error_messages.append(f"{error['loc'][0]}: {error['msg']}")
        return error_messages