from typing import Dict, List

from app.dto.rule import RuleDto
from app.dto.value import ValueDto
from app.dto.coef import CoefDto

flags = [
    'values',
    'coefs'
]

def parse_rules(filename: str):
    flag=''
    values = []
    coefsA = []
    coefsB = []
    flagAs = False
    with open(filename, "r") as f:
        for line in f:
            tmp_flag = check_flag(line)
            if tmp_flag != '':
                flag = tmp_flag
                continue
            match flag:
                case 'values':
                    values.append(parse_values(line))
                case 'coefs':
                    coef = parse_coef(line)
                    if 'A' in coef.title:
                        if len(coef.title) > 2:
                            flagAs = True
                        coefsA.append(coef)
                    elif 'B' in coef.title:
                        coefsB.append(coef)
    if flagAs:
        coefExA = coefsA[-1].title[1]
        tmpCoefsA = [[] for _ in range(int(coefExA))]
        for coefA in coefsA:
            index = int(coefA.title[1])-1
            coefA.title = coefA.title[-1]
            tmpCoefsA[index].append(coefA)
        return RuleDto(values, tmpCoefsA, coefsB)
    return RuleDto(values, [coefsA], coefsB)


def parse_values(line: str) -> ValueDto:
    title, name = line.split(":")[0].split('-')
    values = [int(i) for i in line.split(":")[1].split(' ')]
    return ValueDto(title, name, values)

def parse_coef(line: str) -> CoefDto:
    title, name = line.split(":")[0].split('-')
    values = [float(i) for i in line.split(":")[1].split(' ')]
    return CoefDto(title, name, values)

def check_flag(line: str) -> str:
    if line.strip() in flags:
        return line.strip()
    return ''