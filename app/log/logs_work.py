from numpy.f2py import rules

from app.dto.rule import RuleDto


class LogsWork:
    log_text = ''
    rules = None

    @staticmethod
    def add_rule(rules:RuleDto):
        LogsWork.log_text += "\n"
        LogsWork.rules = rules
        for coefsA in rules.coefs_a:
            for coefA in coefsA:
                LogsWork.log_text += coefA.text(rules.values[0]) + "\n"

        for coefsB in rules.coefs_b:
            LogsWork.log_text += coefsB.text(rules.values[1]) + "\n"

        LogsWork.log_text += "\n"

    @staticmethod
    def add_input_data_by_first(coefIn):
        inp_data_values = LogsWork.rules.values[0]
        LogsWork.log_text += "Входные данные:\n"
        LogsWork.log_text += (f"{inp_data_values.name} = {' + '.join([ f"{inp_data_values.values[i]}/{coefIn[i]}" for i in range(len(coefIn))])}" + "\n")
        LogsWork.log_text += "\n"


    @staticmethod
    def add_matrix_R(R):
        for i in range(len(R)):
            LogsWork.log_text += LogsWork.print_matrix(f"R{i+1}", R[i])
            LogsWork.log_text += "\n"

    @staticmethod
    def add_B(B):
        for i in range(len(B)):
            LogsWork.log_text += LogsWork.print_matrix(f"B{i+1}", B[i])
            LogsWork.log_text += "\n"

    @staticmethod
    def add_Ri(Ri):
        LogsWork.log_text += LogsWork.print_matrix(f"R'", Ri)
        LogsWork.log_text += "\n"

    @staticmethod
    def add_result(result):
        inp_data_values = LogsWork.rules.values[-1]
        LogsWork.log_text += "\nРезультат:\n"
        LogsWork.log_text += (f"{inp_data_values.name} = {' + '.join([f"{inp_data_values.values[i]}/{result[0][i]}" for i in range(len(result[0]))])}" + "\n")

    @staticmethod
    def print_matrix(value, array):
        result = f"{value}:\n"
        for i in range(len(array)):
            for j in range(len(array[i])):
                number = str(round(array[i][j], 4))
                spaces = 8 - len(number)
                result += f"{round(array[i][j], 4)} {' '*spaces}"
            result += "\n"
        return result

    @staticmethod
    def write_in_file(filename):
        with open(filename, "w") as file:
            file.write(LogsWork.log_text)

    @staticmethod
    def add_impl_method(method='mamdani'):
        if method == 'mamdani':
            LogsWork.log_text += "Метод импликации - Мамдани\n"
        else:
            LogsWork.log_text += "Метод импликации - Ларсена\n"

    @staticmethod
    def add_agg_method(method='output'):
        if method == 'output':
            LogsWork.log_text += "Метод агрегации выходов\n"
        else:
            LogsWork.log_text += "Метод агрегации правил\n"