from typing import List

from app.dto.coef import CoefDto
from app.dto.value import ValueDto



class RuleDto:
    def __init__(self, values: List[ValueDto], coefs_a: List[List[CoefDto]], coefs_b: List[CoefDto]):
        self.values: List[ValueDto] = values
        self.coefs_a: List[List[CoefDto]] = coefs_a if type(coefs_a[0]) is list else [coefs_a]
        self.coefs_b: List[CoefDto] = coefs_b



