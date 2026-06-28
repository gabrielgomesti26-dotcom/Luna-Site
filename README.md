# 🌙 Luna Assistant – Assistente Virtual 3D com IA Local

Uma assistente virtual interativa com globo 3D, Street View, rotas e emoções. Tudo rodando localmente com IA (Ollama) e Python/Flask.

---

## ✨ Funcionalidades

- **💬 Conversa com IA** – Interaja por texto ou voz com a Luna (IA local com Ollama).
- **🌍 Globo 3D interativo** – Gire, aproxime e explore o mundo com Three.js.
- **📍 Mostrar locais** – Peça para ver qualquer lugar no Street View (Google Maps).
- **🗺️ Rotas** – Calcule rotas de carro, avião, bicicleta ou a pé e visualize no mapa.
- **😊 Emoções** – Luna expressa sentimentos com avatares diferentes (feliz, triste, pensativa, brava).
- **🎙️ Voz** – Interaja por voz (reconhecimento de fala e síntese com ElevenLabs).
- **⚡ 100% local** – A IA roda no seu PC, sem depender de internet (exceto para mapas).

---

## 📋 Pré‑requisitos

- **Windows 10/11** (recomendado)
- **Python 3.10 ou superior** ([baixar aqui](https://www.python.org/downloads/))
- **Ollama** ([baixar aqui](https://ollama.com/download/windows))
- **Git** (opcional, para clonar o repositório)
- **Conexão com internet** (apenas para baixar o modelo da IA e usar os mapas)

---

## 🚀 Instalação e execução manual

### 1. Baixe o projeto

```bash
git clone https://github.com/seu-usuario/luna-assistant.git
cd luna-assistant
Ou baixe o ZIP do repositório e extraia.

2. Instale as dependências Python
Abra um terminal na pasta do projeto e execute:

bash
# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate

# Instale as bibliotecas necessárias
pip install flask flask-cors openrouteservice numpy requests
3. Instale o Ollama e baixe o modelo
Baixe o Ollama em ollama.com/download/windows e instale.

Depois, no terminal, baixe o modelo de IA:

bash
ollama pull gemma2:2b
(O download pode levar alguns minutos – cerca de 1,5 GB.)

4. Configure as chaves de API
O projeto usa serviços externos para mapas e rotas:

Serviço	Onde configurar	O que fazer
Google Maps API	main.js (variável API_KEY)	Crie uma chave no Google Cloud Console, ative as APIs Maps Embed API e Directions API.
OpenRouteService	servidor_globo.py (variável ORS_API_KEY)	Crie uma conta em OpenRouteService, gere uma chave.
ElevenLabs (opcional)	assistente.py (variáveis API_KEY_ELEVEN e VOICE_ID)	Crie uma conta em ElevenLabs, gere uma chave e pegue um Voice ID.
5. Execute o servidor
bash
python servidor_globo.py
O servidor Flask vai subir na porta 5000.

6. Abra o frontend
Se você estiver usando um servidor web (como Live Server do VS Code), abra index.html com ele.

Ou abra o arquivo diretamente no navegador (duplo clique), mas algumas funcionalidades podem ter problemas de CORS.

Importante: O frontend faz requisições para http://localhost:5000. Certifique-se de que o Flask está rodando antes de interagir.

▶️ Como usar
Conversar com a Luna
Modo texto: Digite sua mensagem no chat e pressione Enter.

Modo voz: Clique no microfone (requer configuração da ElevenLabs).

Comandos especiais
Comando	Exemplo	O que faz
mostra [lugar]	mostra a Torre Eiffel	Abre Street View do local.
quero ir de [origem] para [destino]	quero ir de Brasília para São Paulo	Calcula rota de carro.
quero ir de avião de [origem] para [destino]	quero ir de avião de Recife para Lisboa	Calcula rota aérea.
tchau ou sair	tchau	Encerra a conversa.
Controles do globo
Arrastar – gira o globo.

Scroll – zoom.

Duplo clique – abre Street View no ponto clicado.

🎨 Personalização
Adicionar emoções
Coloque as imagens na pasta luna_faces/.

No main.js, adicione a nova emoção no objeto mapa dentro de atualizarAvatar():

javascript
const mapa = {
    'NOVA_EMOCAO': 'luna_faces/nova.png',
    // ...
};
Na personalidade da Luna (servidor_globo.py), adicione a emoção à lista disponível:

text
Emoções disponíveis: FELIZ, TRISTE, PENSATIVA, BRAVA, NEUTRO, NOVA_EMOCAO.
Trocar o modelo de IA
No servidor_globo.py, altere a variável MODELO_LOCAL:

python
MODELO_LOCAL = "phi3:mini"  # ou "llama3.2", "mistral", etc.
Baixe o novo modelo com ollama pull <nome>.

Alterar a personalidade
Edite a variável personalidade em servidor_globo.py para mudar o comportamento, o sotaque ou as regras da Luna.

🐛 Solução de problemas
Problema	Solução
Erro de CORS ao acessar o Flask	Certifique-se de que CORS(app) está no servidor_globo.py e que o Flask está na porta 5000.
Ollama não responde	Inicie o Ollama manualmente: ollama serve em um terminal separado.
Modelo não encontrado	Baixe o modelo com ollama pull gemma2:2b.
Street View não carrega	Verifique se a chave da API Google Maps está correta e ativa.
Avatar não aparece	Confira o caminho das imagens e se o elemento #avatar-luna existe no HTML.
Erro 500 no /calcular_rota	Verifique se a chave ORS é válida e se o Nominatim está respondendo.
📁 Estrutura do projeto
text
luna-assistant/
├── servidor_globo.py      # Backend Flask (chat, rotas, comandos)
├── assistente.py          # Script com voz e interação alternativa
├── index.html             # Página principal do globo 3D
├── main.js                # Lógica do frontend (Three.js, chat, comandos)
├── textures/              # Texturas do globo e fundo
├── luna_faces/            # Imagens do avatar (emoções)
├── static/                # Arquivos estáticos (CSS, imagens, etc.)
├── requirements.txt       # Dependências Python
└── README.md              # Este arquivo
🤝 Contribuição
Sinta-se à vontade para fazer um fork, abrir issues ou enviar pull requests. Sugestões são sempre bem-vindas!

📜 Licença
Este projeto está sob a licença MIT – veja o arquivo LICENSE para mais detalhes.

🙏 Agradecimentos
Three.js – motor 3D.

Ollama – IA local.

Google Maps API – mapas e Street View.

OpenRouteService – rotas.

ElevenLabs – síntese de voz.

Feito por Gabriel Gomes
