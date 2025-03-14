import csv

with open("Base Teste Hipertensão.csv", "r", newline='') as file:
    reader = csv.reader(file)
    with open("Base Treino Hipertensão.csv", "a", newline='') as file2:
        writer = csv.writer(file2)

        # pulo a primeira linha do file 1
        next(reader)
        for i in reader:
            writer.writerow(i)
