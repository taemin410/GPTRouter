from pydantic import BaseModel

class ResponseCompletion(BaseModel):
    completion: str