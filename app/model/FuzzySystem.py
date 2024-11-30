from typing import List

from app.dto.coef import CoefDto
from app.dto.rule import RuleDto
from app.log.logs_work import LogsWork


class FuzzySystem:
    def __init__(self, rules: RuleDto):
        self.rules = rules

    def get_result_by_first(self, coefIn: List[float], agg_type='output', impl='mamdani') -> List[float] | None:
        LogsWork.add_impl_method(impl)
        LogsWork.add_agg_method(agg_type)
        LogsWork.add_rule_by_first(self.rules)
        LogsWork.add_input_data_by_first(coefIn)
        R = []
        for i in range(len(self.rules.coefs_b)):
            R.append(self.impl(self.rules.coefs_a[0][i].coefs, self.rules.coefs_b[i].coefs, impl))
        LogsWork.add_matrix_R(R)
        if agg_type == 'rules':
            B = []
            for r in R:
                B.append(self.maxmin([coefIn], r))
            LogsWork.add_B(B)
            result = [[round(i, 2) for i in self.aggMax(B)[0]]]
            LogsWork.add_result(result)
            return result
        else:
            aggR = self.aggMax(R)
            LogsWork.add_Ri(aggR)
            result = [[round(i, 2) for i in self.maxmin([coefIn], aggR)[0]]]
            LogsWork.add_result(result)
            return result

    def get_result_by_second(self, coefIn: List[List[float]]):
        LogsWork.add_rule(self.rules)
        LogsWork.add_input_data_by_second(coefIn)
        alphas = self.firing_level(coefIn)
        Bi = []
        for i in range(len(self.rules.coefs_b)):
            Bi.append([self.minAlphaB(alphas[i], self.rules.coefs_b[i].coefs)])
        LogsWork.add_Bi(Bi)
        result = self.aggMax(Bi)
        LogsWork.add_result(result)
        print(self.defuzzification(result[0]))
        return result

    def firing_level(self, coefIn: List[List[float]]):
        maxmins = []
        for coefsA in self.rules.coefs_a:
             maxmins.append([self.maxmin([coefIn[i]], self.transpose([coefsA[i].coefs]))[0][0] for i in range(len(coefsA))])
        result = []
        for item in maxmins:
            result.append(min([i if i is not None else 0 for i in item]))
        LogsWork.add_alpha(result)
        return result

    def impl(self, A: List[float], B: List[float], type_impl="mamdani") -> List[List[float]]:
        result = []
        if type_impl == "mamdani":
            for a in A:
                tmp = []
                for b in B:
                    if a < b:
                       tmp.append(a)
                    else:
                        tmp.append(b)
                result.append(tmp)
        else:
            for a in A:
                tmp = []
                for b in B:
                    tmp.append(a * b)
                result.append(tmp)
        return result

    def maxmin(self, A, R):
        if len(A[0]) != len(R):
            return None
        m = len(A)
        n = len(R[0])
        result = [[None for _ in range(len(R[0]))] for _ in range(len(A))]

        for i in range(m):
            for j in range(n):
                result[i][j] = max([min(A[i][k], R[k][j]) for k in range(len(A[i]))])
        return result

    def aggMax(self, v):
        if v is None:
            return None
        m = len(v[0])
        n = len(v[0][0])
        result = [[None for _ in range(len(v[0][0]))] for _ in range(len(v[0]))]
        for j in range(m):
            for k in range(n):
                result[j][k] = max([value[j][k] for value in v])
        return result

    def transpose(self, matrix):
        result = [[None for j in range(len(matrix))] for i in range(len(matrix[0]))]
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                result[i][j] = matrix[j][i]
        return result

    def minAlphaB(self, alpha, B):
        result = []
        for b in B:
            result.append(min(alpha, b))
        return result

    def defuzzification(self, result):
        return sum([result[i]*self.rules.values[-1].values[i] for i in range(len(result))])/sum(result)
