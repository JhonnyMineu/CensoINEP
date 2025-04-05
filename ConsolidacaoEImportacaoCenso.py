import pandas as pd
import glob
import os
from sqlalchemy import create_engine, Integer, String, Float
from sqlalchemy import text


# Caminho do drive onde os arquivos estão
caminho_pasta_censo = r"C:\Users\jhow_\OneDrive\Documentos\Microdados_Censo_2019_a_2023\Dados_Censo"
caminho_pasta_ies = r"C:\Users\jhow_\OneDrive\Documentos\Microdados_Censo_2019_a_2023\Dados_IES"



# Criando função que coleta, concatena os dfs e seleciona as colunas
def carregar_arquivos_csv(caminho_pasta, colunas):
    # Adiciona barra invertida ao final se não tiver
    if not caminho_pasta.endswith("\\"):
        caminho_pasta += "\\"

    # Buscar arquivos com extensão .CSV
    arquivos_csv = glob.glob(caminho_pasta + "*.CSV")
    no_arquivo = str(arquivos_csv).replace(r'C:\\Users\\jhow_\\OneDrive\\Documentos\\Microdados_Censo_2019_a_2023\\','')

    print("Arquivos encontrados:", no_arquivo)

    # Criar lista de dataframes se houver arquivos
    dfs = [pd.read_csv(arquivo, sep=";", encoding="latin-1") for arquivo in arquivos_csv]

    # Concatenar
    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final = df_final[colunas]
        return df_final
    else:
        print("Nenhum arquivo encontrado.")

# Selecionando as colunas que quero trazer de todos os censos
colunas_censo = ['NU_ANO_CENSO','CO_UF','NO_UF','SG_UF','TP_REDE','CO_IES','NO_CURSO',
                 'CO_CURSO','NO_CINE_ROTULO','NO_CINE_AREA_GERAL','NO_CINE_AREA_ESPECIFICA',
                 'NO_CINE_AREA_DETALHADA','TP_MODALIDADE_ENSINO','QT_ING','QT_MAT','QT_CONC']

# Utilizando a função criada anteriormente para juntar os censos e o cadastro das IES
df_censo = carregar_arquivos_csv(caminho_pasta_censo,colunas_censo)

# Selecionando as colunas que quero trazer do cadastro de IES
colunas_ies = ['CO_IES','NU_ANO_CENSO','NO_IES','TP_ORGANIZACAO_ACADEMICA','TP_REDE']

df_ies = carregar_arquivos_csv(caminho_pasta_ies,colunas_ies)


# Criar dimensão de Instituições
df_ies_sorted = df_ies.sort_values(by=['CO_IES', 'NU_ANO_CENSO'], ascending=[True, False])
dim_instituicao = df_ies_sorted.drop_duplicates(subset='CO_IES', keep='first').copy()
dim_instituicao['NO_ORGANIZACAO_ACADEMICA'] = dim_instituicao['TP_ORGANIZACAO_ACADEMICA'].map({1: 'Universidade',
                                                  2: 'Centro Universitário',
                                                  3: 'Faculdade',
                                                  4:'Instituto Federal de Educação, Ciência e Tecnologia',
                                                  5:'Centro Federal de Educação Tecnológica'})
dim_instituicao['NO_TP_REDE'] = dim_instituicao['TP_REDE'].map({1:'Pública',2:'Privada'})
dim_instituicao.drop(columns='NU_ANO_CENSO',inplace=True)

# Criar dimensão de Cursos
df_censo_sorted = df_censo.sort_values(by=['CO_CURSO', 'NU_ANO_CENSO'], ascending=[True, False])
dim_curso = df_censo_sorted.drop_duplicates(subset='CO_CURSO', keep='first').copy()
dim_curso = dim_curso[['CO_CURSO','NO_CURSO',
                       'NO_CINE_ROTULO','NO_CINE_AREA_GERAL',
                       'NO_CINE_AREA_ESPECIFICA','NO_CINE_AREA_DETALHADA']]
#dim_curso.drop(columns='index',inplace=True)

# Criar dimensão de Modalidade
dim_modalidade = df_censo['TP_MODALIDADE_ENSINO'].dropna().drop_duplicates().reset_index()
dim_modalidade["NO_MODALIDADE"] = dim_modalidade['TP_MODALIDADE_ENSINO'].map({1: 'Presencial', 2: 'A Distância'})
dim_modalidade.drop(columns='index',inplace=True)

# Criar dimensão de Tempo
dim_tempo = df_censo["NU_ANO_CENSO"].drop_duplicates().reset_index()
dim_tempo.drop(columns='index',inplace=True)

# Criar Tabela Fato
fato_censo = df_censo.drop(columns=['NO_CURSO','NO_UF','SG_UF',
           'NO_CINE_ROTULO','NO_CINE_AREA_GERAL','NO_CINE_AREA_ESPECIFICA',
           'NO_CINE_AREA_DETALHADA'])

print(fato_censo.columns)
print(fato_censo.head())
# Configurar conexão com SQL Server
usuario = "sa"
senha = "090319"
servidor = r"Nitro_Jhonny\MSSQLSERVERPROJ2"
banco = "BDCensoINEP"

engine = create_engine(f"mssql+pyodbc://{usuario}:{senha}@{servidor}/{banco}?driver=ODBC+Driver+17+for+SQL+Server")



with engine.connect() as conn:
    conn.execute(text("""
    IF OBJECT_ID('dim_instituicao', 'U') IS NULL
    CREATE TABLE dim_instituicao (
        idRegistro INT IDENTITY(1,1) PRIMARY KEY,
        CO_IES INT UNIQUE,
        NO_IES VARCHAR(255),
        TP_ORGANIZACAO_ACADEMICA INT,
        NO_ORGANIZACAO_ACADEMICA VARCHAR(255)
    )
    """))

    conn.execute(text("""
    IF OBJECT_ID('dim_curso', 'U') IS NULL
    CREATE TABLE dim_curso (
        idRegistro INT IDENTITY(1,1) PRIMARY KEY,
        CO_CURSO INT UNIQUE,
        NO_CURSO VARCHAR(255),
        NO_CINE_ROTULO VARCHAR(255),
        NO_CINE_AREA_GERAL VARCHAR(255),
        NO_CINE_AREA_ESPECIFICA VARCHAR(255),
        NO_CINE_AREA_DETALHADA VARCHAR(255)
    )
    """))

    conn.execute(text("""
    IF OBJECT_ID('dim_modalidade', 'U') IS NULL
    CREATE TABLE dim_modalidade (
        idRegistro INT IDENTITY(1,1) PRIMARY KEY,
        TP_MODALIDADE_ENSINO INT UNIQUE,
        NO_MODALIDADE VARCHAR(50)
    )
    """))

    conn.execute(text("""
    IF OBJECT_ID('dim_tempo', 'U') IS NULL
    CREATE TABLE dim_tempo (
        Ano INT PRIMARY KEY
    )
    """))

    conn.execute(text("""
    IF OBJECT_ID('fato_educacao', 'U') IS NULL
    CREATE TABLE fato_educacao (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Ano INT,
        CO_IES INT,
        CO_CURSO INT,
        TP_MODALIDADE_ENSINO INT,
        Qtd_Ingressantes INT,
        Qtd_Matriculados INT,
        Qtd_Concluintes INT,
        FOREIGN KEY (CO_IES) REFERENCES dim_instituicao(CO_IES),
        FOREIGN KEY (CO_CURSO) REFERENCES dim_curso(CO_CURSO),
        FOREIGN KEY (TP_MODALIDADE_ENSINO) REFERENCES dim_modalidade(TP_MODALIDADE_ENSINO),
        FOREIGN KEY (Ano) REFERENCES dim_tempo(Ano)
    )
    """))




# Inserir dados no banco por tabela dimensão e fato
dim_instituicao.to_sql("dim_instituicao", con=engine, if_exists="append", index=False, dtype={
    "idRegistro":Integer, "CO_IES": Integer, "NO_IES": String(255),
    "TP_ORGANIZACAO_ACADEMICA": String(100), "NO_ORGANIZACAO_ACADEMICA": String(10)
})

dim_curso.to_sql("dim_curso", con=engine, if_exists="append", index=False, dtype={
    "idRegistro":Integer,"CO_CURSO": Integer, "NO_CURSO": String(255), "NO_CINE_ROTULO": String(255),
    "NO_CINE_AREA_GERAL": String(255),"NO_CINE_AREA_ESPECIFICA": String(255), "NO_CINE_AREA_DETALHADA": String(255)
})

dim_modalidade.to_sql("dim_modalidade", con=engine, if_exists="append", index=False, dtype={
    "idRegistro":Integer,"TP_MODALIDADE_ENSINO": Integer, "NO_MODALIDADE": String(50)
})

dim_tempo.to_sql("dim_tempo", con=engine, if_exists="append", index=False, dtype={
    "idRegistro":Integer,"NU_ANO_CENSO": Integer
})

fato_censo.to_sql("fato_educacao", con=engine, if_exists="append", index=False, dtype={
    "idRegistro":Integer,"NU_ANO_CENSO": Integer, "CO_UF": Integer , "TP_REDE": Integer, "CO_IES": Integer, 
     "TP_MODALIDADE_ENSINO": Integer, "CO_CURSO": Integer, "QT_ING": Integer, "QT_MAT": Integer, "QT_CONC": Integer
})

print("Dados inseridos com sucesso!")

