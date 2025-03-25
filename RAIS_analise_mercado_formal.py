## Teste: Ministério do Planejamento em Brasília. Pesquisa sobre o mercado de trabalho brasileiro.
## Candidato: Maria Luiza Dias Campos
## Tarefa: limpeza final da base de dados extraída + análise descritiva.

## carregando bibliotecas
import pandas as pd ## manipulação de dataframes
import seaborn as sns ## execução de gráficos
import matplotlib.pyplot as plt ## execução de gráficos
import numpy as np ## manipulação de dataframes


# Carregar a base de dados
dados_finais = pd.read_csv("dados_rais_1991_a_2015.csv")

# Exibir as primeiras linhas
print(dados_finais.head())

## ANÁLISE TEMPORAL ##

# Agora, vou criar um dicionário de agrupamento para a coluna tipo_vinculo, assim a análise ficará mais fácil.
agrupamento_vinculos = {
    "CLT": [1, 10, 15, 20, 25, 60, 65, 70, 75],
    "ESTATUTÁRIO": [2, 30, 31, 35],
    "TEMPORÁRIO": [4, 50, 55, 90, 95],
    "AVULSO": [3, 40],
    "APRENDIZ": [55],
    "OUTROS": [5, 80, 96, 97],
    "NÃO CLASSIFICADO": [-1],
    "IGNORADO": [0]
}

# Criando uma função para categorizar os vínculos
def categorizar_vinculo(codigo):
    for categoria, codigos in agrupamento_vinculos.items():
        if codigo in codigos:
            return categoria
    return "OUTROS"  # Caso algum código não esteja no dicionário

# Substituindo os valores da coluna 'tipo_vinculo' pelas categorias resumidas
dados_finais["tipo_vinculo"] = dados_finais["tipo_vinculo"].apply(categorizar_vinculo)

# Exibir as primeiras linhas para verificar
print(dados_finais["tipo_vinculo"].head())

# Contando a frequência de cada categoria
print("\nDistribuição das categorias de vínculo:")
print(dados_finais["tipo_vinculo"].value_counts())

## CLT é a categoria mais frequente no conjunto temporal.

## Vamos plotar a ocorrência de contratos CLT no tempo a partir de um gráfico de dispersão.
vinculo_no_tempo = dados_finais.groupby(["ano", "tipo_vinculo"]).size().unstack(fill_value=0)
print(vinculo_no_tempo)

# Transformar a tabela "vinculo_no_tempo" em formato "long"
vinculo_no_tempo_long = vinculo_no_tempo.reset_index().melt(id_vars="ano", var_name="tipo_vinculo", value_name="contagem")

# vamos filtrar o novo dataset para apenas as observações CLT
clt_no_tempo = vinculo_no_tempo_long[vinculo_no_tempo_long["tipo_vinculo"] == "CLT"]
print(clt_no_tempo.head())
clt_no_tempo.to_csv("clt_no_tempo.csv", index=False)

## Agora vamos plotar o gráfico de dispersão.
# Configurar o estilo do Seaborn (sem linhas de grade)
sns.set(style="white")

# Criar o scatter plot
plt.figure(figsize=(14, 7))  # Aumentar o tamanho da figura
sns.scatterplot(data=clt_no_tempo, x="ano", y="contagem", color="black", s=50)  # Pontos pretos

# Adicionar uma linha de tendência
z = np.polyfit(clt_no_tempo["ano"], clt_no_tempo["contagem"], 1)  # Ajuste linear
p = np.poly1d(z)
plt.plot(clt_no_tempo["ano"], p(clt_no_tempo["ano"]), color="#655919", linestyle="--", linewidth=2)

# Adicionar título e labels
plt.title("Distribuição de Ocorrências de Contratos CLT ao Longo dos Anos", fontsize=16)
plt.xlabel("Ano", fontsize=14)
plt.ylabel("Número de Ocorrências", fontsize=14)

# Remover as linhas de grade
plt.grid(False)

# Ajustar o layout
plt.tight_layout()

# Salvar o gráfico com alta qualidade
plt.savefig("scatter_plot_clt.png", dpi=300, bbox_inches="tight")  # Aumentar o DPI para 300

# Exibir o gráfico
plt.show()

## Os dados da distribuição de ocorrências de CLT no tempo são bem dispersos, com uma leve tendência de queda.

## Agora, vamos fazer o mesmo para as ocorrências de contrato tipo estatuário
estatutario_no_tempo = vinculo_no_tempo_long[vinculo_no_tempo_long["tipo_vinculo"] == "ESTATUTÁRIO"]
print(estatutario_no_tempo.head())
estatutario_no_tempo.to_csv("estatutario_no_tempo.csv", index=False)

## Agora, vamos plotar o gráfico.
# Configurar o estilo do Seaborn (sem linhas de grade)
sns.set(style="white")

# Criar o scatter plot
plt.figure(figsize=(14, 7))  # Aumentar o tamanho da figura
sns.scatterplot(data=estatutario_no_tempo, x="ano", y="contagem", color="black", s=50)  # Pontos pretos

# Adicionar uma linha de tendência
z = np.polyfit(estatutario_no_tempo["ano"], estatutario_no_tempo["contagem"], 1)  # Ajuste linear
p = np.poly1d(z)
plt.plot(estatutario_no_tempo["ano"], p(estatutario_no_tempo["ano"]), color="#5e8194", linestyle="--", linewidth=2)

# Adicionar título e labels
plt.title("Distribuição de Ocorrências de Contratos Estatutários ao Longo dos Anos", fontsize=16)
plt.xlabel("Ano", fontsize=14)
plt.ylabel("Número de Ocorrências", fontsize=14)

# Remover as linhas de grade
plt.grid(False)

# Ajustar o layout
plt.tight_layout()

# Salvar o gráfico com alta qualidade
plt.savefig("scatter_plot_estatutario.png", dpi=300, bbox_inches="tight")  # Aumentar o DPI para 300

# Exibir o gráfico
plt.show()

## Os contratos do tipo estatutário são igualmente dispersos e apresentam uma tendência de subida ao longo dos anos.

## ANÁLISE GEOGRÁFICA ##

## Decidi fazer uma análise por macrorregião para garantir visualizações mais limpas.

# Dicionário de agrupamento para macrorregiões
agrupamento_macrorregioes = {
    "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"]
}

# Função para categorizar os Estados em macrorregiões
def categorizar_macrorregiao(sigla_uf):
    for macrorregiao, estados in agrupamento_macrorregioes.items():
        if sigla_uf in estados:
            return macrorregiao
    return "NÃO CLASSIFICADO"  # Caso algum Estado não esteja no dicionário

# Aplicar a função à coluna 'sigla_uf' para criar a coluna 'macrorregiao'
dados_finais["macrorregiao"] = dados_finais["sigla_uf"].apply(categorizar_macrorregiao)

# Verificar o resultado
print(dados_finais[["sigla_uf", "macrorregiao", "tipo_vinculo"]].head())

## ok, vamos filtrar novamente "dados_finais" para criar um dataset próprio para a análise geográfica

# Filtrar os contratos CLT e estatutários
contratos_clt = dados_finais[dados_finais["tipo_vinculo"] == "CLT"]
contratos_estatutario = dados_finais[dados_finais["tipo_vinculo"] == "ESTATUTÁRIO"]

# Agrupar por ano e macrorregião para contar os contratos CLT
df_clt = contratos_clt.groupby(['ano', 'macrorregiao']).size().reset_index(name='total_clt')

# Agrupar por ano e macrorregião para contar os contratos estatutários
df_estatutario = contratos_estatutario.groupby(['ano', 'macrorregiao']).size().reset_index(name='total_estatutario')

# Juntar os dois dataframes em um único dataframe final
data_regional = pd.merge(df_clt, df_estatutario, on=['ano', 'macrorregiao'], how='outer')

# Preencher valores NaN com 0 (caso não haja contratos de algum tipo em alguma combinação de ano/macrorregiao)
data_regional = data_regional.fillna(0)

# Filtrar o dataframe para remover as observações onde macrorregiao == "NÃO CLASSIFICADO"
data_regional = data_regional[data_regional["macrorregiao"] != "NÃO CLASSIFICADO"]

# Exibir o dataframe filtrado
print(data_regional.head())

# salvando...
data_regional.to_csv("data_regional.csv", index=False)

# Exibir o dataframe final
print(data_regional.head())

## Gráficos de tendência por macrorregião (contratos clt)

# Ordenar as macrorregiões pela soma total de contratos CLT (do maior para o menor)
macros_ordenadas_clt = (
    data_regional.groupby('macrorregiao')['total_clt']
    .sum()
    .sort_values(ascending=False)
    .index
    .tolist()
)

# Paleta de tons de verde inspirados no #655919 (mais escuro para o mais claro)
paleta_verde_customizada = [
    '#655919',  # mais escuro
    '#7a6c26',
    '#8f8033',
    '#a59f5c',
    '#bcc688'   # mais claro
]

# Criar dicionário de mapeamento macrorregião -> cor (com base na ordem de frequência)
paleta_verde_mapeada = {
    macro: cor for macro, cor in zip(macros_ordenadas_clt, paleta_verde_customizada)
}

# Estilo do gráfico
sns.set_style("white")

# Criar o gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data_regional,
    x='ano',
    y='total_clt',
    hue='macrorregiao',
    hue_order=macros_ordenadas_clt,
    marker='o',
    palette=paleta_verde_mapeada,
    linewidth=2.5
)

# Títulos e eixos
plt.title("Evolução dos Contratos CLT por Macrorregião ao Longo do Tempo", fontsize=16, pad=20)
plt.xlabel("Ano", fontsize=14, labelpad=10)
plt.ylabel("Total de Contratos CLT", fontsize=14, labelpad=10)

# Legenda
plt.legend(title='Macrorregião', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

# Layout e exibição
plt.grid(False)
plt.tight_layout()
plt.savefig("evolucao_contratos_clt.png", dpi=300, bbox_inches='tight')
plt.show()

## Gráficos de tendência por macrorregião (contratos estatutários)

# Ordenar as macrorregiões pela frequência total de contratos estatutários
macro_ordenadas_estatutario = (
    data_regional.groupby('macrorregiao')['total_estatutario']
    .sum()
    .sort_values(ascending=False)
    .index
)

# Paleta de tons azul acinzentado (baseada em #5e8194, do mais escuro ao mais claro)
paleta_azulacinzentado = [
    '#5e8194',  # mais escuro
    '#7494a4',
    '#8ba7b4',
    '#a2bac4',
    '#b9cdd4'   # mais claro
]

# Mapear cores para macrorregiões com base na ordem de frequência
paleta_mapeada = {
    macro: cor for macro, cor in zip(macro_ordenadas_estatutario, paleta_azulacinzentado)
}

# Estilo sem linhas de grade
sns.set_style("white")

# Criar o gráfico de linhas
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data_regional,
    x='ano',
    y='total_estatutario',
    hue='macrorregiao',
    hue_order=macro_ordenadas_estatutario,
    marker='o',
    palette=paleta_mapeada,
    linewidth=2.5
)

# Título e eixos
plt.title("Evolução dos Contratos Estatutários por Macrorregião ao Longo do Tempo", fontsize=16, pad=20)
plt.xlabel("Ano", fontsize=14, labelpad=10)
plt.ylabel("Total de Contratos Estatutários", fontsize=14, labelpad=10)

# Legenda fora do gráfico
plt.legend(title='Macrorregião', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

# Layout e salvamento
plt.grid(False)
plt.tight_layout()
plt.savefig("evolucao_contratos_estatutarios.png", dpi=300, bbox_inches='tight')
plt.show()

## ANÁLISE DE GÊNERO ##

# Vamos seguir a análise fazendo o dicionário de gênero
agrupamento_genero = {
    "Feminino": [2],
    "Masculino": [1],
    "Ignorado": [-1]
}

# Função para categorizar os gêneros
def categorizar_genero(sexo):
    for genero, codigos in agrupamento_genero.items():
        if sexo in codigos:
            return genero
    return "Desconhecido"  # Caso o valor não esteja no dicionário

# Aplicar a função de categorização
contratos_clt['sexo'] = contratos_clt['sexo'].apply(categorizar_genero)
contratos_estatutario['sexo'] = contratos_estatutario['sexo'].apply(categorizar_genero)

# Agrupar por ano e sexo para contar os contratos CLT
df_clt = contratos_clt.groupby(['ano', 'sexo']).size().reset_index(name='total_clt')
df_estatutario = contratos_estatutario.groupby(['ano', 'sexo']).size().reset_index(name='total_estatutario')

# Juntar os dois dataframes em um único dataframe final
data_genero = pd.merge(df_clt, df_estatutario, on=['ano', 'sexo'], how='outer')

# Preencher valores NaN com 0 (caso não haja contratos de algum tipo em alguma combinação de ano/gênero)
data_genero = data_genero.fillna(0)

# Exibir o dataframe filtrado
print(data_genero.head())

# Salvar o dataset
data_genero.to_csv("data_genero.csv", index=False)

## Análise gráfica: CLT

#Preparar os dados (pivotar por ano e gênero)
clt_por_ano_genero = data_genero.pivot(index='ano', columns='sexo', values='total_clt')

# Ordenar as colunas (Feminino primeiro para empilhar na base)
clt_por_ano_genero = clt_por_ano_genero[['Feminino', 'Masculino']]  # ajuste conforme seus dados

# Criar o gráfico de linhas (sem bordas e sem grade)
plt.figure(figsize=(12, 6), facecolor='none')

# Linha para Feminino (Rosa pastel)
plt.plot(
    clt_por_ano_genero.index,
    clt_por_ano_genero['Feminino'],
    color='#b9377a',  # Rosa
    marker='o',       # Marcadores circulares
    linestyle='-',
    linewidth=2,
    label='Feminino (CLT)'
)

# Linha para Masculino (Azul pastel)
plt.plot(
    clt_por_ano_genero.index,
    clt_por_ano_genero['Masculino'],
    color='#4b6080',  # Azul
    marker='s',       # Marcadores quadrados
    linestyle='-',
    linewidth=2,
    label='Masculino (CLT)'
)

# Personalização do gráfico
plt.title('Evolução de Contratos CLT por Gênero (1991-2015)', fontsize=14, pad=20)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Contratos CLT', fontsize=12)
plt.xticks(clt_por_ano_genero.index[::2], rotation=45, ha='right')  # Anos de 2 em 2

# Remover TODAS as bordas e grades
plt.gca().spines[['top', 'right']].set_visible(False)  # Remove todas as bordas
plt.grid(False)  # Desativa grades

# Legenda (flutuante à direita)
plt.legend(
    title='Gênero',
    frameon=False,  # Remove borda da legenda
    loc='center left',
    bbox_to_anchor=(1, 0.5)  # Posiciona fora do gráfico
)

# Ajustar layout e salvar
plt.tight_layout()
plt.savefig('evolucao_clt_genero.png', dpi=300, bbox_inches='tight')

# Exibir o gráfico
plt.show()

## Análise gráfica: Estatutário

#Preparar os dados (pivotar por ano e gênero)
estatutario_por_ano_genero = data_genero.pivot(index='ano', columns='sexo', values='total_estatutario')

# Ordenar as colunas (Feminino primeiro para empilhar na base)
estatutario_por_ano_genero = estatutario_por_ano_genero[['Feminino', 'Masculino']]

# Criar o gráfico de linhas (sem bordas e sem grade)
plt.figure(figsize=(12, 6), facecolor='none')

# Linha para Feminino (Rosa pastel)
plt.plot(
    estatutario_por_ano_genero.index,
    estatutario_por_ano_genero['Feminino'],
    color='#b9377a',  # Rosa
    marker='o',       # Marcadores circulares
    linestyle='-',
    linewidth=2,
    label='Feminino (CLT)'
)

# Linha para Masculino (Azul pastel)
plt.plot(
    estatutario_por_ano_genero.index,
    estatutario_por_ano_genero['Masculino'],
    color='#4b6080',  # Azul
    marker='s',       # Marcadores quadrados
    linestyle='-',
    linewidth=2,
    label='Masculino (CLT)'
)

# Personalização do gráfico
plt.title('Evolução de Contratos Estatutários por Gênero (1991-2015)', fontsize=14, pad=20)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Contratos Estatutários', fontsize=12)
plt.xticks(clt_por_ano_genero.index[::2], rotation=45, ha='right')  # Anos de 2 em 2

# Remover TODAS as bordas e grades
plt.gca().spines[['top', 'right']].set_visible(False)  # Remove todas as bordas
plt.grid(False)  # Desativa grades

# Legenda (flutuante à direita)
plt.legend(
    title='Gênero',
    frameon=False,  # Remove borda da legenda
    loc='center left',
    bbox_to_anchor=(1, 0.5)  # Posiciona fora do gráfico
)

# Ajustar layout e salvar
plt.tight_layout()
plt.savefig('evolucao_estatutario_genero.png', dpi=300, bbox_inches='tight')

# Exibir o gráfico
plt.show()









