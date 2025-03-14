import matplotlib.pyplot as plt
import numpy as np

# Simulando dados para o gráfico
generations = np.arange(1, 604)
f_measure_max = 0.78 + 0.08 * (1 - np.exp(-0.03 * generations))  # Crescimento simulado
f_measure_avg = 0.78 + 0.05 * (1 - np.exp(-0.03 * generations))  # Crescimento simulado
f_measure_min = 0.78 + 0.02 * (1 - np.exp(-0.03 * generations))  # Crescimento simulado
number_features = 150 - 0.5 * generations + 0.1 * np.sin(0.1 * generations)  # Decaimento simulado
diversity = 90 * np.exp(-0.02 * generations) + 10 * np.random.randn(len(generations))  # Decaimento simulado

# Criando a figura e o eixo
fig, ax1 = plt.subplots()

# Plotando as métricas de FMeasure no eixo primário
ax1.plot(generations, f_measure_max, 'g-', label='Maximum')
ax1.plot(generations, f_measure_avg, 'orange', label='Average')
ax1.plot(generations, f_measure_min, 'r-', label='Minimum')

# Definindo os rótulos e títulos
ax1.set_xlabel('Number of Generations')
ax1.set_ylabel('F Measure', color='black')
ax1.tick_params('y', colors='black')
ax1.legend(loc='upper left')

# Criando um segundo eixo Y para características como "Number Features" e "Diversity"
ax2 = ax1.twinx()
ax2.plot(generations, number_features, 'b--', label='Number Features')
ax2.plot(generations, diversity, 'm:', label='Diversity')

ax2.set_ylabel('Number Features / Diversity', color='black')
ax2.tick_params('y', colors='black')
ax2.legend(loc='upper right')

# Exibindo o gráfico
plt.tight_layout()
plt.show()
