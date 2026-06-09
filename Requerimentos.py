#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher FULL da Luna Assistant
- Instala dependências Python (Flask, CORS, openrouteservice, numpy, requests)
- Baixa e instala Ollama (Windows)
- Baixa o modelo (gemma2:2b)
- Inicia servidor Flask e abre navegador
"""

import subprocess
import sys
import time
import webbrowser
import os
import platform
import urllib.request
import zipfile

# ========== CONFIGURAÇÕES ==========
MODELO_OLLAMA = "gemma2:2b"   # Você pode trocar para "phi3:mini"
PORTA_FLASK = 5000
URL_FRONTEND = f"http://localhost:{PORTA_FLASK}"


# ========== FUNÇÕES AUXILIARES ==========
def instalar_dependencias():
    """Instala as bibliotecas Python necessárias."""
    print("📦 Instalando dependências Python...")
    required = [
        "flask",
        "flask-cors",
        "openrouteservice",
        "numpy",
        "requests"
    ]
    for lib in required:
        print(f"   Instalando {lib}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
    print("✅ Dependências instaladas.\n")


def verificar_ollama():
    """Verifica se o Ollama está instalado e disponível no PATH."""
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def instalar_ollama_windows():
    """Instala o Ollama no Windows via PowerShell (recomendado)."""
    print("📥 Baixando e instalando Ollama (Windows)...")
    # Comando PowerShell oficial
    install_cmd = 'irm https://ollama.com/install.ps1 | iex'
    try:
        subprocess.run(["powershell", "-Command", install_cmd], check=True)
        print("✅ Ollama instalado com sucesso!")
        # Aguarda alguns segundos para o sistema registrar o PATH
        time.sleep(3)
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na instalação do Ollama: {e}")
        print("   Tente instalar manualmente em: https://ollama.com/download")
        sys.exit(1)


def iniciar_servico_ollama():
    """Inicia o servidor do Ollama em segundo plano (Windows)."""
    print("🚀 Iniciando servidor Ollama...")
    try:
        # Inicia o processo sem janela visível
        subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(3)  # Aguarda o servidor subir
        print("✅ Servidor Ollama rodando em segundo plano.\n")
    except Exception as e:
        print(f"❌ Erro ao iniciar Ollama: {e}")
        sys.exit(1)


def baixar_modelo():
    """Baixa o modelo especificado se ainda não estiver disponível."""
    print(f"🔍 Verificando modelo '{MODELO_OLLAMA}'...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        if MODELO_OLLAMA not in result.stdout:
            print(f"📥 Baixando modelo '{MODELO_OLLAMA}'. Isso pode levar alguns minutos...")
            subprocess.run(["ollama", "pull", MODELO_OLLAMA], check=True)
            print(f"✅ Modelo '{MODELO_OLLAMA}' baixado com sucesso!\n")
        else:
            print(f"✅ Modelo '{MODELO_OLLAMA}' já está disponível.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao verificar/baixar modelo: {e}")
        sys.exit(1)


def iniciar_flask():
    """Inicia o servidor Flask (servidor_globo.py) em um processo separado."""
    script_path = os.path.join(os.path.dirname(__file__), "servidor_globo.py")
    if not os.path.exists(script_path):
        print("❌ Arquivo 'servidor_globo.py' não encontrado na pasta atual.")
        sys.exit(1)
    print("🚀 Iniciando servidor Flask...")
    if platform.system() == "Windows":
        processo = subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        processo = subprocess.Popen([sys.executable, script_path])
    return processo


def abrir_navegador():
    """Abre o navegador padrão na URL do globo 3D."""
    print("🌍 Abrindo navegador...")
    time.sleep(2)  # Pequena pausa para o Flask terminar de subir
    webbrowser.open(URL_FRONTEND)
    print(f"   Acesse: {URL_FRONTEND}\n")


# ========== MAIN ==========
def main():
    print("🌟 Inicializando Luna Assistant - Modo FULL")
    print("   Isso pode levar alguns minutos na primeira execução...\n")
    
    # 1. Instalar dependências Python
    instalar_dependencias()
    
    # 2. Garantir que o Ollama esteja instalado
    if not verificar_ollama():
        if platform.system() == "Windows":
            instalar_ollama_windows()
        else:
            print("❌ Sistema não suportado para instalação automática.")
            print("   Instale o Ollama manualmente: https://ollama.com")
            sys.exit(1)
    
    # 3. Iniciar o serviço do Ollama
    iniciar_servico_ollama()
    
    # 4. Baixar o modelo (caso não exista)
    baixar_modelo()
    
    # 5. Iniciar o Flask
    processo_flask = iniciar_flask()
    
    # 6. Abrir o navegador
    abrir_navegador()
    
    print("\n✅ Luna está online!")
    print("   Pressione Ctrl+C no terminal para encerrar.\n")
    
    try:
        processo_flask.wait()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando Luna Assistant...")
        processo_flask.terminate()
        processo_flask.wait()
        print("✅ Servidor encerrado.")


if __name__ == "__main__":
    main()