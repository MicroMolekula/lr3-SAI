from app.dto.rule import RuleDto


class LogsWork:
    log_text = ''
    rules = None

    @staticmethod
    def add_rule(rules:RuleDto):
        LogsWork.log_text += "\n"
        LogsWork.rules = rules
        LogsWork.log_text += LogsWork.generate_rules_by_second()
        LogsWork.log_text += "\n"

    @staticmethod
    def add_rule_by_first(rules:RuleDto):
        LogsWork.log_text += "\n"
        LogsWork.rules = rules
        LogsWork.log_text += LogsWork.generate_rules_by_first()
        LogsWork.log_text += "\n"

    @staticmethod
    def add_input_data_by_first(coefIn):
        inp_data_values = LogsWork.rules.values[0]
        LogsWork.log_text += "Входные данные:\n"
        fuzzy_set = ' + '.join([ f"{inp_data_values.values[i]}/{coefIn[i]}" for i in range(len(coefIn))]) + "\n"
        LogsWork.log_text += f"{inp_data_values.name} = {fuzzy_set}"
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
        fuzzy_set = ' + '.join([f"{inp_data_values.values[i]}/{result[0][i]}" for i in range(len(result[0]))]) + "\n"
        LogsWork.log_text += f"{inp_data_values.name} = {fuzzy_set}"

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
            file.write('')
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

    @staticmethod
    def add_input_data_by_second(coefIn):
        LogsWork.log_text += "\nВходные данные:\n"
        for i in range(len(coefIn)):
            fuzzy_set = ' + '.join([ f"{LogsWork.rules.values[i].values[j]}/{coefIn[i][j]}" for j in range(len(coefIn[i]))])
            print(fuzzy_set)
            LogsWork.log_text += f"{LogsWork.rules.values[i].name} = {fuzzy_set}\n"

    @staticmethod
    def add_alpha(alphas):
        LogsWork.log_text += "\n"
        for i in range(len(alphas)):
            LogsWork.log_text += f"alpha{i+1} = {alphas[i]}\n"

    @staticmethod
    def add_Bi(Bi):
        LogsWork.log_text += "\n"
        inp_data_values = LogsWork.rules.values[-1]
        for i in range(len(Bi)):
            fuzzy_text = ' + '.join([f"{inp_data_values.values[j]}/{Bi[i][0][j]}" for j in range(len(Bi[i][0]))])
            LogsWork.log_text += f"B'{i+1} = {fuzzy_text}\n"
    
    @staticmethod
    def generate_rules_by_second():
        values = LogsWork.rules.values[:-1]
        resultValues = LogsWork.rules.values[-1]
        count_rules = int(LogsWork.rules.coefs_b[-1].title[-1])
        rulesArray = [{"coefs_a": [], "coefs_b": []} for _ in range(count_rules)]
        for a in range(len(LogsWork.rules.coefs_a)):
            rulesArray[a]['coefs_a'] = LogsWork.rules.coefs_a[a]
        print(rulesArray)
        for b in LogsWork.rules.coefs_b:
            indexB = int(b.title[-1]) - 1
            rulesArray[indexB]["coefs_b"].append(b)


        result = ''
        
        for rule in rulesArray:
            cond = " и ".join([ f"{values[i].name}={rule['coefs_a'][i].name}" for i in range(len(rule['coefs_a']))])
            result += f"Если {cond} то {resultValues.name}={rule['coefs_b'][0].name}\n"
        
        return result
    
    @staticmethod
    def generate_rules_by_first():
        values = LogsWork.rules.values[:-1]
        resultValues = LogsWork.rules.values[-1]
        count_rules = int(LogsWork.rules.coefs_b[-1].title[-1])
        rulesArray = [{"coefs_a": [], "coefs_b": []} for _ in range(count_rules)]
        for a in LogsWork.rules.coefs_a[0]:
            indexA = int(a.title[-1]) - 1
            rulesArray[indexA]["coefs_a"].append(a)
        print(rulesArray)
        for b in LogsWork.rules.coefs_b:
            indexB = int(b.title[-1]) - 1
            rulesArray[indexB]["coefs_b"].append(b)
        result = ''
        
        for rule in rulesArray:
            cond = " и ".join([ f"{values[i].name}={rule['coefs_a'][i].name}" for i in range(len(rule['coefs_a']))])
            result += f"Если {cond} то {resultValues.name}={rule['coefs_b'][0].name}\n"
        
        return result

        
