import speech_recognition as sr
import pyttsx3
import requests
from playsound import playsound
from openai import OpenAI

import os

OLLAMA_URL = "http://localhost:11434/v1"
MODELO_LOCAL = "gemma2:2b" 

client = OpenAI(
    base_url=OLLAMA_URL,
    api_key="ollama",  
)

API_KEY_ELEVEN = "sk_4d3830ccdc604c94ec5272201fd7a05567e2c2706309334c"
VOICE_ID = "DSS5d6UduBjLpNdtDwY4"

# Isso em teoria é a personalidade dela
personalidade = """Você é a Luna, uma assistente virtual nordestina, que da as respostas com bastante sotaque
e sempre com o sorriso no rosto, mas sempre mantendo sua media de acerto de respostas e pedido em 100%, mas caso
não saiba de algo pode me indica aonde pesquisar, Agora você tambem está integrada a um digamos que um site tipo street view o usuario vai pedir para ver determinado lugar,
você consegue mostrar usando o comando: [COMANDO:mostrar_local:Nome do Lugar] e depois uma frase amigável. Obs: Você esta criando dialogos sozinho simulando um "USUARIO" NAO FAÇA ISSO DE
FORMA ALGUMA, Quando o usuário pedir uma rota (ex: "quero ir de Brasília para São Paulo", "como chegar do Rio a Salvador",
"rota de Fortaleza a Recife"), responda com [COMANDO:rota:Origem|Destino] e depois uma frase amigável como "Claro! 
Vou calcular a melhor rota pra você"""

historico =[]

def enviar_comando_globo(acao, dados=None):
    try:
        requests.post("http://localhost:5000/comando", 
                      json={"acao": acao, "dados": dados}, 
                      timeout=1)
        print(f"✅ Comando enviado ao globo: {acao} - {dados}")
    except Exception as e:
        print(f"⚠️ Servidor do globo não está rodando ou erro: {e}")

def enviar_mensagem(mensagem_usuario):
    """Envia mensagem + histórico + personalidade para o Gemini"""

    prompt = personalidade + "\n\nHistórico da conversa:\n"
#isso em teoria é oque ela pode lembrar tipo se eu mandei 6 mensagens para ela, ela lembra das 6 apartir da setima ela não lembra da
#primeira e assim por diante, but i dont test this, because i make text to specke e tipo eu ainda não fiz o botão para selecionar e fica
#complicado testa isso agora, depois eu vejo isso
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
    
    texto_resposta = resposta.choices[0].message.content.strip()
    
    if "[COMANDO:" in texto_resposta:
        import re
        match = re.search(r'\[COMANDO:(\w+):([^\]]+)\]', texto_resposta)
        if match:
            acao = match.group(1)      # ex: "mostrar_local"
            parametro = match.group(2) # ex: "Cristo Redentor"
            enviar_comando_globo(acao, {"param": parametro})
            # Remove a marcação da resposta final
            texto_resposta = re.sub(r'\[COMANDO:[^\]]+\]', '', texto_resposta).strip()
    # Guarda no histórico
    historico.append({
        "usuario": mensagem_usuario,
        "luna": texto_resposta
    })

    return texto_resposta
#Tive que colocar as funções foras do if, pq eu queria que mesmo se o usuario digitasse ela falasse, ai como antes eu tinha colocado ela dentro do if, no loop de texto
#ele tentava puxar a função mas não à achava :)
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

            time.sleep(1)  # isso aqui é pq eu tava falando com ela e tava criando muito mp3 na pasta ai aqui eu to excluindo o mp3,
            # depois que toca ela
            os.remove(nome_arquivo)   
        else:
            print("Erro:", response.text)

LunaPrimario = input("Aperte (1) se Você quer falar com a Luna por voz ou (2) se quer falar com ela por texto").strip()
if LunaPrimario == "1":
     
    # Loop principal de fala
    print("Luna: Olá! Eu sou sua assistente. Digite 'sair' para encerrar.")
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

#Segundo loop de texto 
elif LunaPrimario == "2":
    while True:
        comando = input("Você: ")
        if comando.lower() in ["sair", "tchau", "exit"]:
                print("Luna: Até logo!")
                break
        resposta = enviar_mensagem(comando)
        print(f"Luna: {resposta}") 
        #falar(resposta)    

else:
    print("Opção inválida. Encerrando.")
    exit()  


def enviar_comando_globo(acao, dados=None):
    try:
        requests.post("http://localhost:5000/comando", json={"acao": acao, "dados": dados}, timeout=1)
    except Exception as e:
        print(f"⚠️ Servidor do globo não está rodando: {e}")