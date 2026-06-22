import speech_recognition as sr
import pyttsx3
import requests
from playsound import playsound
from openai import OpenAI
import os
import re

# ===== CONFIGURAÇÃO DO OLLAMA =====
OLLAMA_URL = "http://localhost:11434/v1"
MODELO_LOCAL = "gemma2:2b"  # ou "phi3:mini"
client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

# ===== CONFIGURAÇÃO DA ELEVENLABS (OPCIONAL) =====
API_KEY_ELEVEN = "sk_4d3830ccdc604c94ec5272201fd7a05567e2c2706309334c"
VOICE_ID = "DSS5d6UduBjLpNdtDwY4"

# ===== PERSONALIDADE DA LUNA =====
personalidade = """Você é a Luna, uma assistente virtual nordestina, que dá as respostas com bastante sotaque
e sempre com o sorriso no rosto, mas sempre mantendo sua média de acerto de respostas e pedido em 100%, mas caso
não saiba de algo pode me indicar aonde pesquisar. Agora você também está integrada a um site tipo street view: 
o usuário vai pedir para ver determinado lugar, você consegue mostrar usando o comando: 
[COMANDO:mostrar_local:Nome do Lugar] e depois uma frase amigável. 
Obs: Você está criando diálogos sozinho simulando um "USUÁRIO" - NÃO FAÇA ISSO DE FORMA ALGUMA.
Quando o usuário pedir uma rota (ex: "quero ir de Brasília para São Paulo", "como chegar do Rio a Salvador",
"rota de Fortaleza a Recife"), responda com [COMANDO:rota:Origem|Destino] e depois uma frase amigável como 
"Claro! Vou calcular a melhor rota pra você"."""

historico = []

# ===== ENVIAR COMANDO PARA O GLOBO =====
def enviar_comando_globo(acao, dados=None):
    try:
        requests.post("http://localhost:5000/comando", json={"acao": acao, "dados": dados}, timeout=1)
        print(f"✅ Comando enviado ao globo: {acao} - {dados}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar comando: {e}")

# ===== PROCESSAR MENSAGEM =====
def enviar_mensagem(mensagem_usuario):
    """Envia mensagem + histórico + personalidade para o modelo local (Ollama)."""
    prompt = personalidade + "\n\nHistórico da conversa:\n"
    for interacao in historico[-6:]:
        prompt += f"Usuário: {interacao['usuario']}\n"
        prompt += f"Luna: {interacao['luna']}\n"
    prompt += f"\nUsuário: {mensagem_usuario}\n"
    prompt += "Luna:"

    resposta = client.chat.completions.create(
        model=MODELO_LOCAL,
        messages=[
            {"role": "system", "content": personalidade},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        top_p=0.7,
        max_tokens=500,
    )
    texto_resposta = resposta.choices[0].message.content.strip()

    # Detecta comandos especiais
    if "[COMANDO:" in texto_resposta:
        match = re.search(r'\[COMANDO:(\w+):([^\]]+)\]', texto_resposta)
        if match:
            acao = match.group(1)
            parametro = match.group(2)
            enviar_comando_globo(acao, {"param": parametro})
            texto_resposta = re.sub(r'\[COMANDO:[^\]]+\]', '', texto_resposta).strip()

    historico.append({"usuario": mensagem_usuario, "luna": texto_resposta})
    return texto_resposta

# ===== FUNÇÕES DE ÁUDIO =====
def ouvir():
    recognizer = sr.Recognizer()
    microfone = sr.Microphone()
    with microfone as source:
        print("\n🎤 Fale algo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("⏰ Nada detectado.")
            return None
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print(f"📝 Você disse: {texto}")
        return texto.lower()
    except:
        print("❌ Não entendi.")
        return None

def falar(texto):
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
        import time
        nome_arquivo = f"voz_{int(time.time())}.mp3"
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        playsound(nome_arquivo)
        time.sleep(1)
        os.remove(nome_arquivo)
    else:
        print("Erro:", response.text)

# ===== BLOCO PRINCIPAL (SÓ EXECUTA SE RODAR DIRETAMENTE) =====
if __name__ == "__main__":
    LunaPrimario = input("Aperte (1) para falar com a Luna por voz ou (2) para falar por texto: ").strip()
    if LunaPrimario == "1":
        print("Luna: Olá! Eu sou sua assistente. Diga 'sair' para encerrar.")
        falar("Olá! Eu sou a Luna, sua assistente.")
        while True:
            comando = ouvir()
            if comando is None:
                continue
            if comando in ["sair", "tchau", "exit"]:
                falar("Até logo!")
                print("Luna: Até logo!")
                break
            resposta = enviar_mensagem(comando)
            print(f"Luna: {resposta}")
            falar(resposta)
    elif LunaPrimario == "2":
        print("Luna: Olá! Digite 'sair' para encerrar.")
        while True:
            comando = input("Você: ")
            if comando.lower() in ["sair", "tchau", "exit"]:
                print("Luna: Até logo!")
                break
            resposta = enviar_mensagem(comando)
            print(f"Luna: {resposta}")
    else:
        print("Opção inválida. Encerrando.")
        exit()