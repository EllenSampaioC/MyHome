import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'dbname': 'quintoandar_db',
    'user': 'postgres',
    'password': '123postgres',  # Substitua pela sua senha real
    'host': 'localhost',
    'port': '5432'
}

try:
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    c = conn.cursor()
    c.execute('SELECT * FROM public.imoveis')
    imoveis = c.fetchall()
    print("Conexao OK! Dados encontrados:")
    for imovel in imoveis:
        print(imovel)
    conn.close()
except Exception as e:
    print(f"Erro: {e}")