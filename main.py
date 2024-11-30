from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from app.log.logs_work import LogsWork
from app.model.FuzzySystem import FuzzySystem
from app.model.parse import parse_rules

class RequestByFirst(BaseModel):
    values: List[float]
    impl_method: str | None = None
    agg_method: str | None = None
    punkt: int | None = None


class RequestBySecond(BaseModel):
    values: List[List[float]]

app = FastAPI()

@app.post('/byFirst')
def get_result_by_first(request: RequestByFirst):
    rules = parse_rules('rules1.txt')
    fuzzy = FuzzySystem(rules)
    result = fuzzy.get_result_by_first(request.values, impl=request.impl_method, agg_type=request.agg_method)
    LogsWork.write_in_file('results/result1.txt')
    LogsWork.log_text = ''
    return {
        'result': result[0],
    }

@app.post('/bySecond')
def get_result_by_second(request: RequestBySecond):
    rules = parse_rules('rules2.txt')
    print(request.values)
    fuzzy = FuzzySystem(rules)
    result = fuzzy.get_result_by_second(request.values)
    LogsWork.write_in_file('results/result2.txt')
    LogsWork.log_text = ''
    return {
        'result': result[0],
    }

@app.post('/defuz')
def defuz(request: RequestByFirst):
    rules = None
    if (request.punkt == 1):
        rules = parse_rules('rules1.txt')
    else:
        rules = parse_rules('rules2.txt')
    fuzzy = FuzzySystem(rules)
    return {
        "result": fuzzy.defuzzification(request.values),
    }

if __name__ == '__main__':
    # rules = parse_rules('rules2.txt')
    # print(rules)

    # fuzzy = FuzzySystem(rules)
    # print(fuzzy.get_result_by_second([[0.5, 0.8, 0.9, 0.5], [0.9, 0.5, 0.3, 0], [0.3, 0.5, 0.8, 0.4]]))
    # print(fuzzy.get_result_by_first([0.5, 0.8, 0.9, 0.5], agg_type='rules', impl='mamdani'))
    # LogsWork.write_in_file('result2.txt')
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)