from constants import Constants


class MOGATerminalLogger:
    @staticmethod
    def print_generation_results(generation_count: int, population_size: int, record):
        print("\n\n")
        log = (
            "Número da geração: "
            + generation_count.__str__()
            + "\n"
            + "Tamanho da população: "
            + population_size.__str__()
            + "\n"
            + "Total de filhos repetidos: "
            + record["Filhos"][Constants.Stats.REPEATED_INDIVIDUALS].__str__()
            + "\n"
            + "(Filhos abaixo da média, Filhos acima da média) = "
            + record["Filhos"][Constants.Stats.WORST_BEST].__str__()
            + "\n"
            + "1) Media  "
            + record["Fitness"][Constants.Stats.AVERAGE][0].__str__()
            + "\n"
            + "1) Media  "
            + record["Fitness"][Constants.Stats.AVERAGE][1].__str__()
            + "\n"
            + "2) Desvio Padrao "
            + record["Fitness"][Constants.Stats.STANDARD_DEVIATION][0].__str__()
            + "\n"
            + "2) Desvio Padrao "
            + record["Fitness"][Constants.Stats.STANDARD_DEVIATION][1].__str__()
            + "\n"
            + "3) Minimo "
            + record["Fitness"][Constants.Stats.MINIMUM][0].__str__()
            + "\n"
            + "3) Minimo "
            + record["Fitness"][Constants.Stats.MINIMUM][1].__str__()
            + "\n"
            + "4) Maximo "
            + record["Fitness"][Constants.Stats.MAXIMUM][0].__str__()
            + "\n"
            + "4) Maximo "
            + record["Fitness"][Constants.Stats.MAXIMUM][1].__str__()
        )

        print(log)
