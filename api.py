from flask import Flask, jsonify, request
import oracledb
from flask_cors import CORS
import os



app = Flask(__name__)
CORS(app)

# Definir o caminho para o Oracle Instant Client


# Dados de conexão ao Oracle
dsn_tns = oracledb.makedsn('oracle.fiap.com.br', '1521', service_name='orcl')
username = 'rm76153'
password = '150598'

# Função para verificar se o usuário e senha existem na tabela mobile_logins
def check_credentials(email, senha):
    try:
        # Conectar ao banco de dados Oracle
        conn = oracledb.connect(user=username, password=password, dsn=dsn_tns)
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute("SELECT COUNT(*) FROM mobile_login WHERE email = :email AND senha = :senha", {'email': email, 'senha': senha})

        # Recuperar o resultado
        count = cursor.fetchone()[0]

        # Fechar o cursor e conexão
        cursor.close()
        conn.close()

        return count > 0

    except oracledb.DatabaseError as e:
        error, = e.args
        return {"error": error.message}

# Função para recuperar a senha com base no email
def get_password_by_email(email):
    try:
        # Conectar ao banco de dados Oracle
        conn = oracledb.connect(user=username, password=password, dsn=dsn_tns)
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute("SELECT senha FROM mobile_login WHERE email = :email", {'email': email})

        # Recuperar o resultado
        row = cursor.fetchone()

        # Fechar o cursor e conexão
        cursor.close()
        conn.close()

        if row:
            return row[0]
        else:
            return None

    except oracledb.DatabaseError as e:
        error, = e.args
        return {"error": error.message}
    

def consultar_comentarios():
        try:
            # Conectar ao banco de dados Oracle
            conn = oracledb.connect(user=username, password=password, dsn=dsn_tns)
            cursor = conn.cursor()

            # Executar a consulta SQL
            cursor.execute("SELECT * FROM ComentariosRedesSociais")

            # Recuperar todos os resultados
            resultados = cursor.fetchall()

            # Converter os resultados em um formato adequado para jsonify
            dados = []
            for resultado in resultados:
                dados.append({
                    'id_comentario': resultado[0],
                    'texto_comentario': resultado[1],
                    'sentimento': resultado[2],
                    'rede_social': resultado[3]
                })

            # Fechar o cursor e a conexão
            cursor.close()
            conn.close()

            return jsonify(dados)

        except oracledb.DatabaseError as e:
            error, = e.args
            return {"error": error.message}
    
def get_user_info_by_email(email):
    try:
        # Conectar ao banco de dados Oracle
        conn = oracledb.connect(user=username, password=password, dsn=dsn_tns)
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute("SELECT NOME_USUARIO, senha FROM mobile_login WHERE email = :email", {'email': email})

        # Recuperar o resultado
        row = cursor.fetchone()

        # Fechar o cursor e conexão
        cursor.close()
        conn.close()

        if row:
            return {'nome': row[0], 'senha': row[1]}
        else:
            return None

    except oracledb.DatabaseError as e:
        error, = e.args
        return {"error": error.message}
    






@app.route('/user-info/<email>', methods=['GET'])
def get_user_info(email):
    user_info = get_user_info_by_email(email)
    
    if user_info:
        return jsonify(user_info), 200
    else:
        return jsonify({"message": "Email não encontrado."}), 404


@app.route('/comentarios', methods=['GET'])
def get_comentarios():
    return consultar_comentarios()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if email is None or senha is None:
        return jsonify({"error": "Email e senha são obrigatórios."}), 400

    if check_credentials(email, senha):
        return jsonify({"message": "Credenciais válidas."}), 200
    else:
        return jsonify({"message": "Credenciais inválidas."}), 401

@app.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    data = request.get_json()
    email = data.get('email')

    if email is None:
        return jsonify({"error": "Email é obrigatório."}), 400

    senha = get_password_by_email(email)
    
    if senha:
        return jsonify({"message": "Senha encontrada.", "senha": senha}), 200
    else:
        return jsonify({"message": "Email não encontrado."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
