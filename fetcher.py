import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re
import os
import openai
from db import create_database, insert_article

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

# openai.api_key = "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"  # ⚠️ Remplace avec ta vraie clé OpenAI

# Vérifie si une URL correspond à un article
def is_valid_article_url(href):
    """Vérifie si l'URL est valide pour un article."""
    return bool(re.search(r'/news/[\w-]+-\d+$', href)) or '/news/articles/' in href

# Récupère le vrai titre depuis la page de l’article
def extract_title_from_article(article_url):
    """Extrait le titre de l'article depuis l'URL de l'article."""
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text().strip().replace(" - BBC News", "")
    except Exception as e:
        print(f"Erreur en récupérant le titre depuis {article_url} : {e}")
        return None

# Vérifie si le titre est lié au domaine des affaires
def is_business_related_with_trade(title):
    """Vérifie si le titre est lié au domaine des affaires, de l'économie ou du commerce."""
    try:
        prompt = f"Le titre suivant est-il lié au domaine des affaires, de l'économie ou du commerce ? Réponds par OUI ou NON uniquement.\nTitre : \"{title}\""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Tu es un assistant qui évalue si un titre est lié au domaine des affaires, de l'économie ou du commerce."},
                      {"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        answer = response.choices[0].message.content.strip().lower()
        return "oui" in answer
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return False

# Génère un résumé de l’article avec GPT (une fois qu’il est validé comme lié au domaine des affaires)
def generate_summary_with_gpt(content):
    """Génère un résumé de l'article à l'aide de GPT."""
    try:
        prompt = f"Voici le contenu d’un article. Peux-tu me fournir un résumé clair et concis en 2 ou 3 phrases ?\n\n{content}"
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Tu es un assistant qui résume des articles de manière professionnelle."},
                      {"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Erreur de résumé : {e}")
        return ""

# Extraction de la date de publication
def extract_publication_date(article_soup):
    """Extrait la date de publication depuis l'article."""
    try:
        meta_date = article_soup.find("meta", {"property": "article:published_time"})
        if meta_date and meta_date.get("content"):
            date_iso = meta_date["content"]
            date_only = date_iso.split("T")[0]
            return date_only
        meta_date2 = article_soup.find("meta", {"name": "OriginalPublicationDate"})
        if meta_date2 and meta_date2.get("content"):
            date_iso = meta_date2["content"]
            date_only = date_iso.split("T")[0]
            return date_only
    except Exception as e:
        print(f"⚠️ Erreur d’extraction de date : {e}")
    return None

# Récupère les articles depuis la page d’accueil BBC
def fetch_bbc_articles_from_website():
    """Récupère les articles d'actualité de BBC News liés aux affaires."""
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    seen = set()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Parcours des liens d'articles sur la page d'accueil
    for link in soup.find_all('a', href=True):
        href = link['href']
        if is_valid_article_url(href):
            full_url = "https://www.bbc.com" + href if href.startswith("/") else href
            if full_url not in seen:
                seen.add(full_url)
                title = extract_title_from_article(full_url)
                if title and is_business_related_with_trade(title):
                    # Récupère le contenu complet de l'article pour générer un résumé
                    content = ""
                    try:
                        article_page = requests.get(full_url)
                        article_soup = BeautifulSoup(article_page.content, 'html.parser')
                        paragraphs = article_soup.find_all('p')
                        content = ' '.join(p.get_text() for p in paragraphs if p.get_text())
                    except Exception as e:
                        print(f"Erreur lors de la récupération du contenu de l'article : {e}")

                    summary = generate_summary_with_gpt(content) if content else ""
                    publication_date = extract_publication_date(article_soup) or datetime.now().strftime('%Y-%m-%d')
                    articles.append({
                        'title': title,
                        'url': full_url,
                        'publication_date': publication_date,
                        'summary': summary,
                        'source': 'BBC'
                    })

    return articles

if __name__ == "__main__":
    try:
        create_database()  # Créer la base de données (si elle n'existe pas déjà)
        articles = fetch_bbc_articles_from_website()  # Récupérer les articles
        if not articles:
            print("Aucun article trouvé.")
        for article in articles:
            print(f"📌 Titre : {article['title']}")
            print(f"🔗 URL : {article['url']}")
            print(f"📅 Date : {article['publication_date']}")
            print(f"📝 Résumé : {article['summary']}")
            print(f"🏷️ Source : {article['source']}")
            print("-" * 80)
            insert_article(article)  # Insérer chaque article dans la base de données
    except Exception as e:
        print("Une erreur est survenue :", e)
