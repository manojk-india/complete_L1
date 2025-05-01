# Here is where we declare our models 
from typing import Literal
from pydantic import BaseModel
class info(BaseModel):
    board: str
    name: str
    sprint: Literal['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5', 'Sprint 6', 'Sprint 7', 'Sprint 8', 'Sprint 9', 'Sprint 10', 'Sprint 11']		
