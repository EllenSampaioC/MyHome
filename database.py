import psycopg2

# Configurações do banco (ajuste com suas credenciais)
DB_CONFIG = {
    'dbname': 'quintoandar_db',
    'user': 'postgres',        # Substitua pelo seu usuário
    'password': '123postgres',   # Substitua pela sua senha
    'host': 'localhost',
    'port': '5432'             # Porta padrão do PostgreSQL
}

def criar_banco():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True  # Para criar a tabela sem transação explícita
        c = conn.cursor()
        
        # Criar tabela
        c.execute('''CREATE TABLE IF NOT EXISTS imoveis (
                     id SERIAL PRIMARY KEY,
                     localizacao TEXT NOT NULL,
                     preco_aluguel REAL NOT NULL,
                     tipo TEXT NOT NULL,
                     quartos INTEGER NOT NULL)''')
        
        # Inserir dados fictícios
        c.execute("INSERT INTO imoveis (localizacao, preco_aluguel, tipo, quartos) VALUES ('São Paulo', 1500.00, 'Apartamento', 2) ON CONFLICT DO NOTHING")
        c.execute("INSERT INTO imoveis (localizacao, preco_aluguel, tipo, quartos) VALUES ('Rio de Janeiro', 2000.00, 'Casa', 3) ON CONFLICT DO NOTHING")
        c.execute("INSERT INTO imoveis (localizacao, preco_aluguel, tipo, quartos) VALUES ('Belo Horizonte', 1200.00, 'Apartamento', 1) ON CONFLICT DO NOTHING")
        
        conn.close()
        print("Banco de dados configurado com sucesso!")
    except Exception as e:
        print(f"Erro ao configurar o banco: {e}")

if __name__ == '__main__':
    criar_banco()