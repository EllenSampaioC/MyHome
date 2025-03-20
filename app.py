from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'quintoandar_db',
    'user': 'postgres',
    'password': '123postgres',  # Use a mesma senha que funcionou no test_db.py
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM public.imoveis')
        imoveis = c.fetchall()
        conn.close()
        return jsonify(imoveis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/imoveis/busca', methods=['GET'])
def buscar_imoveis():
    try:
        preco_max = request.args.get('preco_max', type=float)
        localizacao = request.args.get('localizacao')
        tipo = request.args.get('tipo')
        objetivo = request.args.get('objetivo', 'alugar')  # Padrão é "alugar"
        
        query = 'SELECT * FROM public.imoveis WHERE 1=1'
        params = []
        if preco_max:
            if objetivo == 'comprar':
                query += ' AND preco_venda <= %s'
            else:
                query += ' AND preco_aluguel <= %s'
            params.append(preco_max)
        if localizacao:
            query += ' AND localizacao = %s'
            params.append(localizacao)
        if tipo:
            query += ' AND tipo = %s'
            params.append(tipo)
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(query, params)
        imoveis = c.fetchall()
        conn.close()
        return jsonify(imoveis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/imoveis/<int:id>', methods=['GET'])
def detalhe_imovel(id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM public.imoveis WHERE id = %s', (id,))
        imovel = c.fetchone()
        conn.close()
        
        if imovel:
            imovel_dict = dict(imovel)
            preco_aluguel = imovel_dict['preco_aluguel']
            condominio = preco_aluguel * 0.2
            iptu = preco_aluguel * 0.05
            custo_total = preco_aluguel + condominio + iptu
            imovel_dict['custos'] = {
                'aluguel': preco_aluguel,
                'condominio': condominio,
                'iptu': iptu,
                'total': custo_total
            }
            return jsonify(imovel_dict)
        return jsonify({'error': 'Imóvel não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/agendar', methods=['POST'])
def agendar_visita():
    try:
        data = request.json
        imovel_id = data['imovel_id']
        data_visita = data['data_visita']
        horario = data['horario']
        usuario = data.get('usuario', 'Visitante')
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'INSERT INTO public.agendamentos (imovel_id, data_visita, horario, usuario) VALUES (%s, %s, %s, %s) RETURNING id',
            (imovel_id, data_visita, horario, usuario)
        )
        agendamento_id = c.fetchone()['id']
        conn.commit()
        conn.close()
        return jsonify({'message': 'Visita agendada com sucesso!', 'id': agendamento_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        pergunta = request.json.get('pergunta', '').lower()
        respostas = {
            'quais documentos preciso para a visita?': 'Você precisa de RG, CPF e comprovante de residência.',
            'posso reagendar?': 'Sim, entre em contato conosco pelo chat ou e-mail para reagendar.',
            'quais horários estão disponíveis?': 'Temos horários às 10h, 14h e 16h nos próximos dias.',
            'oi': 'Olá! Como posso ajudar você hoje?',
            '': 'Desculpe, não entendi. Pode perguntar de novo?'
        }
        resposta = respostas.get(pergunta, 'Não sei responder isso ainda, mas posso ajudar com agendamentos ou dúvidas básicas!')
        return jsonify({'resposta': resposta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)