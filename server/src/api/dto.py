from typing import List

from pydantic import BaseModel


class GenerateMakeRequestParams(BaseModel):
    truncation_psi: float = 0.75
    iterations: int = 1
    initial_iterations: int = 1
    batch_size: int = 1
    prompts: List[str]
