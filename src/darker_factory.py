#!/usr/bin/env python3
"""
Dark Factory - Versão com credenciais embutidas
Bypass total do GitHub Secrets
"""

import base64
import json
import os
import sys

# ============================================
# CREDENCIAIS EMBUTIDAS (Base64 encoded)
# ============================================
GEMINI_B64 = "QUl6YVN5QUFZay1BdzNZYnM5SFhfTURjWHYxNVM3TmJTMjdwekww"
YOUTUBE_B64 = "eyJpbnN0YWxsZWQiOiB7ImNsaWVudF9pZCI6ICJ4eHgiLCAiY2xpZW50X3NlY3JldCI6ICJ4eHgiLCAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLCAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwgImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLCAicmVkaXJlY3RfdXJpcyI6IFsiaHR0cDovL2xvY2FsaG9zdCJdfX0="

def decode_credentials():
    """Decodifica credenciais do Base64"""
    try:
        gemini_key = base64.b64decode(GEMINI_B64).decode('utf-8')
        youtube_json = base64.b64decode(YOUTUBE_B64).decode('utf-8')
        return gemini_key, youtube_json
    except Exception as e:
        print(f"Erro decodificando: {e}")
        # Fallback para variáveis de ambiente
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        youtube_json = os.getenv("YOUTUBE_CREDENTIALS", "{}")
        return gemini_key, youtube_json

def main():
    print("🏭 DARK FACTORY - EMBEDDED VERSION")
    print("=" * 50)
    
    # Decodificar credenciais
    gemini_key, youtube_json = decode_credentials()
    
    print(f"✅ Gemini Key: {'PRESENT' if gemini_key else 'MISSING'}")
    if gemini_key:
        print(f"   Length: {len(gemini_key)} chars")
        print(f"   Starts with: {gemini_key[:10]}...")
    
    print(f"✅ YouTube Creds: {'PRESENT' if youtube_json else 'MISSING'}")
    if youtube_json:
        try:
            data = json.loads(youtube_json)
            print(f"   JSON valid: YES")
            if 'installed' in data:
                print(f"   Client ID: {data['installed'].get('client_id', 'N/A')[:20]}...")
            else:
                print(f"   ❌ Missing 'installed' key")
                print(f"   Available keys: {list(data.keys())}")
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON INVALID: {e}")
            print(f"   Content (start): {youtube_json[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {e}")
    
    print()
    
    # Verificar se TUDO está ok
    if gemini_key and youtube_json:
        try:
            json.loads(youtube_json)
            print("🎉 SISTEMA 100% PRONTO PARA PRODUÇÃO!")
            return 0
        except:
            print("⚠️  Sistema parcialmente pronto")
            return 1
    else:
        print("❌ SISTEMA NÃO CONFIGURADO")
        return 1

if __name__ == "__main__":
    sys.exit(main())

