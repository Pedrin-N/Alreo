import sqlite3

# Cria o arquivo empresa.db compatível com o Alreo
import os
conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'empresa.db'))
cursor = conn.cursor()

# 1. Tabela DEPARTAMENTO
cursor.execute('''
CREATE TABLE DEPARTAMENTO (
    Dnome VARCHAR(15) NOT NULL,
    Dnumero INT NOT NULL PRIMARY KEY,
    Cpf_gerente CHAR(11),
    Data_inicio_gerente DATE
);
''')

# 2. Tabela FUNCIONARIO
cursor.execute('''
CREATE TABLE FUNCIONARIO (
    Pnome VARCHAR(15) NOT NULL,
    Minicial CHAR(1),
    Unome VARCHAR(15) NOT NULL,
    Cpf CHAR(11) NOT NULL PRIMARY KEY,
    Datanasc DATE,
    Endereco VARCHAR(50),
    Sexo CHAR(1),
    Salario DECIMAL(10,2),
    Cpf_supervisor CHAR(11),
    Dnr INT NOT NULL,
    FOREIGN KEY (Dnr) REFERENCES DEPARTAMENTO(Dnumero)
);
''')

# Inserção de dados de DEPARTAMENTO
cursor.executemany('''
INSERT INTO DEPARTAMENTO VALUES (?, ?, ?, ?)
''', [
    ('Matriz', 1, '88866555576', '1981-06-19'),
    ('Administracao', 4, '98765432168', '1995-01-01'),
    ('Pesquisa', 5, '33344555587', '1988-05-22')
])

# Inserção de dados de FUNCIONARIO (Tuplas clássicas de Elmasri & Navathe)
cursor.executemany('''
INSERT INTO FUNCIONARIO VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [
    ('Joao', 'B', 'Silva', '12345678966', '1965-01-09', 'Rua das Flores, 751, SP', 'M', 30000.0, '33344555587', 5),
    ('Fernando', 'T', 'Wong', '33344555587', '1955-12-08', 'Rua da Lapa, 34, SP', 'M', 40000.0, '88866555576', 5),
    ('Alice', 'J', 'Zelaya', '99988777767', '1968-01-19', 'Rua Souza Lima, 35, Curitiba', 'F', 25000.0, '98765432168', 4),
    ('Jennifer', 'S', 'Souza', '98765432168', '1941-06-20', 'Av. Arthur de Lima, 54, SA', 'F', 43000.0, '88866555576', 4),
    ('Ronaldo', 'K', 'Lima', '66688444476', '1962-09-15', 'Rua Reboucas, 65, Piracicaba', 'M', 38000.0, '33344555587', 5),
    ('Joyce', 'A', 'Leite', '45345345376', '1972-07-31', 'Av. Lucas Obes, 74, SP', 'F', 25000.0, '33344555587', 5),
    ('Andre', 'V', 'Pereira', '98798798733', '1969-03-29', 'Rua Timbira, 35, SP', 'M', 25000.0, '98765432168', 4),
    ('Jorge', 'E', 'Brito', '88866555576', '1937-11-10', 'Rua do Horto, 35, SP', 'M', 55000.0, None, 1)
])

conn.commit()
conn.close()
print("Banco 'empresa.db' gerado com sucesso!")