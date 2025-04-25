import os
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("✅ Clé API valide.")
    openai.api_key = api_key
else:
    print("❌ Problème avec la clé API.")
    exit()

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Bonjour, quel est ton modèle ?"}]
    )

    print("✅ Réponse GPT :")
    print(response['choices'][0]['message']['content'])

except Exception as e:
    print("❌ GPT Error:", e)
s