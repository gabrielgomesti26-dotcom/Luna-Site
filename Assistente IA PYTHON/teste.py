from google import genai

client = genai.Client(api_key="AIzaSyDvqKg5i127snsgPRldncO2_NcwSGmrHQ0")
modelo = "gemini-2.0-flash-lite"
resposta = client.models.generate_content(model=modelo, contents="Oi, tudo bem?")
print(resposta.text)