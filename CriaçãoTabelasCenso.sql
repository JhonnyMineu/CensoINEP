CREATE TABLE dim_instituicao (
        idRegistro INT IDENTITY(1,1),
        CO_IES INT PRIMARY KEY,
        NO_IES VARCHAR(255),
        TP_ORGANIZACAO_ACADEMICA INT,
        NO_ORGANIZACAO_ACADEMICA VARCHAR(255)
);


CREATE TABLE dim_curso (
        idRegistro INT IDENTITY(1,1),
        CO_CURSO INT PRIMARY KEY,
        NO_CURSO VARCHAR(255),
        NO_CINE_ROTULO VARCHAR(255),
        NO_CINE_AREA_GERAL VARCHAR(255),
        NO_CINE_AREA_ESPECIFICA VARCHAR(255),
        NO_CINE_AREA_DETALHADA VARCHAR(255)
);

CREATE TABLE dim_modalidade (
        idRegistro INT IDENTITY(1,1),
        TP_MODALIDADE_ENSINO INT PRIMARY KEY,
        NO_MODALIDADE VARCHAR(50)
);

CREATE TABLE dim_tempo (
        ID_Ano INT PRIMARY KEY,
        Ano INT
);

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
        FOREIGN KEY (Ano) REFERENCES dim_tempo(ID_Ano)
);