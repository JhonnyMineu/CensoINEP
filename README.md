# 🎓 Painel Analítico - Censo da Educação Superior (2019 a 2023)

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de **Assistente de Dados**, com o objetivo de construir painéis analíticos baseados nos microdados do Censo da Educação Superior, fornecidos pelo INEP.

---

## 🧠 Objetivo

Criar uma solução de ponta a ponta que envolva:
- Extração e transformação dos microdados do Censo (2019 a 2023);
- Estruturação de modelo dimensional (estrela) no SQL Server;
- Criação de dashboards analíticos no Power BI;
- Análise geral do Ensino Superior EAD e análise específica do Centro Universitário Senac.

---

## ⚙️ Estrutura do Projeto

```bash

├── scripts/
│   └── etl_inep.py            # Script Python para leitura, tratamento e inserção no banco
├── sql/
│   └── modelo_estrela.sql     # Script para criação das tabelas no SQL Server
├── powerbi/
│   └── painel_censo.pbix      # Arquivo Power BI com os dashboards
├── imagens/
│   └── preview_dashboard.png  # Captura de tela dos dashboards
├── requirements.txt           # Pacotes Python utilizados
└── README.md

🛠️ Tecnologias Utilizadas
-Python 3.10
-pandas, sqlalchemy, pyodbc
-SQL Server 2022
-Power BI
-GitHub

🧾 Descrição Técnica
📥 ETL (Python)
-O script percorre a pasta data/, carrega os arquivos CSV de cada ano, seleciona colunas relevantes e aplica filtros.
-Os dados são organizados em tabelas do tipo dimensão e fato, que são carregadas diretamente no banco SQL Server.

🧱 Modelo Estrela
Construído com base nos princípios de modelagem dimensional.

Principais tabelas:

-dim_curso
-dim_ano
-dim_modalidade
-dim_ies
-fato_matricula

📊 Dashboards (Power BI)
Painel Geral
-Evolução de ingressantes, matriculados e concluintes (EAD x Presencial)
-Top cursos por indicador e ano
-Taxas de crescimento ano a ano

Painel Senac
-Evolução dos indicadores no Senac (total e por curso)
-Comparação com outras IES
-Taxas de crescimento do Senac

📬 Contato
Se quiser conversar sobre o projeto ou tiver dúvidas:

Nome: Jhonny S. Mineu

Email: jhonny.mineu@gmail.com

LinkedIn: https://www.linkedin.com/in/jhonnymineu/

📝 Observações Finais
Todas as fontes de dados são públicas e podem ser acessadas em:
-Censo da Educação Superior - INEP
-Este projeto foi desenvolvido para fins de demonstração técnica em processo seletivo.
