from flask import Flask, request

app = Flask(__name__)

# Rota para receber os dados do sensor
@app.route('/dados', methods=['GET'])
def receber_dados():
    valor = request.args.get('valor')  # pega o valor enviado pela D1 Mini
    if valor:
        print(f"Valor recebido do sensor: {valor}")
        return "OK", 200
    else:
        return "Nenhum valor recebido", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
