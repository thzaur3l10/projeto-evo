import sqlite3

def init_db():
    conn = sqlite3.connect("clinica.db")
    cursor = conn.cursor()

    # Tabela Paciente
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Paciente (
        Data TEXT NOT NULL,
        Nome TEXT NOT NULL,
        CPF INTEGER NOT NULL PRIMARY KEY,
        DtNascimento TEXT NOT NULL,
        Email TEXT,
        Contato INTEGER,
        Responsavel TEXT,
        CPFResponsavel TEXT,
        HipoteseDiagnostica TEXT,
        EmailResponsavel TEXT,
        ContatoResponsavel INTEGER,
        Logradouro TEXT,
        Numero TEXT,
        Complemento TEXT,
        Bairro TEXT,
        CEP TEXT,
        UF TEXT,
        CP TEXT
    )
    """)

    # Tabela Convenio
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Convenio (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CPF INTEGER NOT NULL,
        Convenio TEXT,
        Plano TEXT,
        Carteirinha TEXT,
        Reembolso INTEGER,
        FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
    )
    """)

    # Tabela Clinico
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clinico (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CPF INTEGER NOT NULL,
        DtCadastro TEXT NOT NULL,
        Diagnostico TEXT NOT NULL,
        Indicacao TEXT,
        Avaliacao TEXT,
        Alta TEXT,
        DtAlta TEXT,
        FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
    )
    """)

    # Tabela Sessao
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sessao (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CPF INTEGER NOT NULL,
        Clinico INTEGER NOT NULL,
        QueixaSintoma TEXT,
        Consciencia TEXT,
        Nutricional TEXT,
        Mobilidade TEXT,
        Data TEXT NOT NULL,
        TerapiasAplicadas TEXT,
        Realizado TEXT NOT NULL,
        Evolucao TEXT,
        Observacao TEXT,
        NomeProfissional TEXT,
        Conselho TEXT,
        Assinatura TEXT,
        FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
    )
    """)

    # Tabela Evolucao
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Evolucao (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CPF INTEGER NOT NULL,
        Data TEXT NOT NULL,
        Observacao TEXT,
        Evolucao TEXT,
        FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
    )
    """)

    conn.commit()
    conn.close()
