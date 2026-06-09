from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from openrouteservice import Client
import numpy as np
import requests

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True) 

ORS_API_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImYzMmIyM2M5OTdjMjQ5ZGM4NjU4NjZiYjZhZWQzMWU0IiwiaCI6Im11cm11cjY0In0='
ors_client = Client(key=ORS_API_KEY)


def geocode(lugar):
    # Adiciona "Brasil" para garantir que o lugar está no país correto
    query = f"{lugar}, Brasil"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1&accept-language=pt-BR"
    response = requests.get(url, headers={'User-Agent': 'Luna-Assistant/1.0'})
    if response.status_code == 200 and response.json():
        lat = float(response.json()[0]['lat'])
        lon = float(response.json()[0]['lon'])
        return (lat, lon)
    return None

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

    try:
        route = ors_client.directions(
            coordinates=[(coords_origem[1], coords_origem[0]), (coords_destino[1], coords_destino[0])],
            profile='driving-car',
            format='geojson'
        )
    except Exception as e:
        print(f"Erro ao calcular a rota: {e}")
        return jsonify({"erro": "Não foi possível calcular a rota."}), 500

    distancia_km = route['features'][0]['properties']['summary']['distance'] / 1000
    duracao_min = route['features'][0]['properties']['summary']['duration'] / 60
    route_coords = route['features'][0]['geometry']['coordinates']

    route_points_3d = []
    radius = 5
    for lon, lat in route_coords:
        x = radius * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
        y = radius * np.sin(np.radians(lat))
        z = radius * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
        route_points_3d.append([x, y, z])

    return jsonify({
        "rota": route_points_3d,
        "distancia": round(distancia_km, 2),
        "duracao": round(duracao_min, 2)
    })


# Armazena o último comando (simples)
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
    # Retorna e depois limpa (para não repetir)
    cmd = comando_atual.copy()
    comando_atual["acao"] = None
    return jsonify(cmd)

if __name__ == '__main__':
    app.run(port=5000, debug=False)