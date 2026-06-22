from flask import Flask, request, jsonify
from flask_cors import CORS
<<<<<<< HEAD
from openrouteservice import Client
import numpy as np
import requests
from Assistente import enviar_mensagem  # Importa a função do assistente.py
import base64
import time
import os

API_KEY_ELEVEN = "sk_4d3830ccdc604c94ec5272201fd7a05567e2c2706309334c"
VOICE_ID = "DSS5d6UduBjLpNdtDwY4"

def gerar_audio_elevenlabs(texto):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY_ELEVEN,
        "Content-Type": "application/json"
    }
    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        # Converte o áudio para base64 para enviar via JSON
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        return audio_base64
    else:
        print(f"Erro ElevenLabs: {response.text}")
        return None

app = Flask(__name__)

=======
import json
from openrouteservice import Client
import numpy as np
import requests

app = Flask(__name__)
>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
<<<<<<< HEAD
     supports_credentials=True)

# ===== CONFIGURAÇÃO DA OPENROUTESERVICE =====
ORS_API_KEY = 'eyJ0cml0I1YjNlZTM1OTc4NTExMTIwMDI5ZjYyNDgiLCJpZCI6ImYzMmMyM2M5OTdjMjQ5ZGM4NjU4NjZiYjZhZWQzM0U0IiwiaCI6Im1c1cm1c1cjY0Ino='
ors_client = Client(key=ORS_API_KEY)

# ===== GEOCODE =====
def geocode(lugar):
    query = f"{lugar}, Brasil"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1&accept-language=pt-BR"
    response = requests.get(url, headers={"User-Agent": "Luna-Assistant/1.0"})
=======
     supports_credentials=True) 

ORS_API_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImYzMmIyM2M5OTdjMjQ5ZGM4NjU4NjZiYjZhZWQzMWU0IiwiaCI6Im11cm11cjY0In0='
ors_client = Client(key=ORS_API_KEY)


def geocode(lugar):
    # Adiciona "Brasil" para garantir que o lugar está no país correto
    query = f"{lugar}, Brasil"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1&accept-language=pt-BR"
    response = requests.get(url, headers={'User-Agent': 'Luna-Assistant/1.0'})
>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
    if response.status_code == 200 and response.json():
        lat = float(response.json()[0]['lat'])
        lon = float(response.json()[0]['lon'])
        return (lat, lon)
    return None

<<<<<<< HEAD
# ===== ROTA PARA CALCULAR ROTA =====
@app.route('/calcular_rota', methods=['POST', 'OPTIONS'])
def calcular_rota():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    origem = data.get('origem')
    destino = data.get('destino')
    coords_origem = geocode(origem)
    coords_destino = geocode(destino)
    if not coords_origem or not coords_destino:
        return jsonify({"erro": "Não encontrei um dos lugares"}), 400
=======
# ========== ROTA PARA CALCULAR ROTA ==========
@app.route('/calcular_rota', methods=['POST', 'OPTIONS'])
def calcular_rota():
    if request.method == 'OPTIONS':
        return '', 200  # resposta para preflight CORS
    data = request.get_json()
    origem = data.get('origem')
    destino = data.get('destino')

    coords_origem = geocode(origem)
    coords_destino = geocode(destino)

    if not coords_origem or not coords_destino:
        return jsonify({"erro": "Não consegui encontrar um dos lugares."}), 400

>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
    try:
        route = ors_client.directions(
            coordinates=[(coords_origem[1], coords_origem[0]), (coords_destino[1], coords_destino[0])],
            profile='driving-car',
            format='geojson'
        )
    except Exception as e:
<<<<<<< HEAD
        print(f"Erro ORS: {e}")
        return jsonify({"erro": "Falha ao calcular rota"}), 500
    distancia_km = route['features'][0]['properties']['summary']['distance'] / 1000
    duracao_min = route['features'][0]['properties']['summary']['duration'] / 60
    route_coords = route['features'][0]['geometry']['coordinates']
=======
        print(f"Erro ao calcular a rota: {e}")
        return jsonify({"erro": "Não foi possível calcular a rota."}), 500

    distancia_km = route['features'][0]['properties']['summary']['distance'] / 1000
    duracao_min = route['features'][0]['properties']['summary']['duration'] / 60
    route_coords = route['features'][0]['geometry']['coordinates']

>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
    route_points_3d = []
    radius = 5
    for lon, lat in route_coords:
        x = radius * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
        y = radius * np.sin(np.radians(lat))
        z = radius * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
        route_points_3d.append([x, y, z])
<<<<<<< HEAD
=======

>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
    return jsonify({
        "rota": route_points_3d,
        "distancia": round(distancia_km, 2),
        "duracao": round(duracao_min, 2)
    })

<<<<<<< HEAD
# ===== COMANDOS DO GLOBO =====
=======

# Armazena o último comando (simples)
>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
comando_atual = {"acao": None, "dados": None}

@app.route('/comando', methods=['POST'])
def receber_comando():
    data = request.json
    comando_atual["acao"] = data.get("acao")
    comando_atual["dados"] = data.get("dados")
    print(f"📡 Comando recebido: {comando_atual}")
    return jsonify({"status": "ok"})

@app.route('/comando', methods=['GET'])
def pegar_comando():
<<<<<<< HEAD
=======
    # Retorna e depois limpa (para não repetir)
>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
    cmd = comando_atual.copy()
    comando_atual["acao"] = None
    return jsonify(cmd)

<<<<<<< HEAD
# ===== CHAT =====
@app.route('/chat', methods=['POST'])
def chat():
    print("🔵 Rota /chat chamada")  # debug
    data = request.get_json()
    mensagem = data.get('mensagem', '').strip()
    print(f"📩 Mensagem recebida: {mensagem}")
    if not mensagem:
        return jsonify({"erro": "Mensagem vazia"}), 400
    resposta_texto = enviar_mensagem(mensagem)
    print(f"💬 Resposta: {resposta_texto[:50]}...")  # mostra início
    audio_base64 = gerar_audio_elevenlabs(resposta_texto)
    return jsonify({
        "resposta": resposta_texto,
        "audio": audio_base64
    })

if __name__ == '__main__':
    app.run(port=5000, debug=False)

=======
if __name__ == '__main__':
    app.run(port=5000, debug=False)
>>>>>>> fc2c36a5dfba086a3373c4f265361db945609c83
