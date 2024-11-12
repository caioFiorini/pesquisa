import pandas as pd
import matplotlib.pyplot as plt

# Dados para a tabela
dados = {
    'Nome': ['Ana', 'Bruno', 'Carlos'],
    'Idade': [23, 35, 45],
    'Cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
}

# Criar DataFrame
tabela = pd.DataFrame(dados)

# Configurar o tamanho da figura
fig, ax = plt.subplots(figsize=(5, 2))  # Tamanho da imagem (largura, altura)

# Remover os eixos
ax.axis('off')

# Renderizar a tabela no gráfico
tabela_imagem = ax.table(cellText=tabela.values, colLabels=tabela.columns, cellLoc='center', loc='center')

# Ajustar o estilo da tabela
tabela_imagem.auto_set_font_size(False)
tabela_imagem.set_fontsize(12)
tabela_imagem.scale(1.2, 1.2)  # Escala da tabela

# Salvar como imagem
plt.savefig("tabela_imagem.png", bbox_inches='tight', dpi=300)

# Exibir a imagem
plt.show()
