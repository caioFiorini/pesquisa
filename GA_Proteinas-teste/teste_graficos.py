import matplotlib.pyplot as plt

# Suponha que você tem os dados:
qtd_atributos = [1, 2, 3, 4, 5]  # pode ir até 40
f1_scores = [0.55, 0.60, 0.65, 0.68, 0.70]  # alguma métrica
atributos_por_barra = [
    ["idade"],
    ["idade", "sexo"],
    ["idade", "sexo", "altura"],
    ["idade", "sexo", "altura", "peso"],
    ["idade", "sexo", "altura", "peso", "IMC"]
]

# Criar o gráfico
plt.figure(figsize=(12, 6))
bars = plt.bar(qtd_atributos, f1_scores, color='skyblue')

# Adiciona os nomes dos atributos dentro de cada barra
for bar, atributos in zip(bars, atributos_por_barra):
    texto = "\n".join(atributos)  # Quebra linha pra caber
    plt.text(bar.get_x() + bar.get_width()/2.0,
             bar.get_height()/2,
             texto,
             ha='center', va='center', fontsize=8, rotation=90)

plt.xlabel("Quantidade de Atributos")
plt.ylabel("F1 Score")
plt.title("Desempenho vs Quantidade de Atributos")
plt.tight_layout()
plt.show()
