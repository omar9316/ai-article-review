import sqlite3
import streamlit as st
from fpdf import FPDF
import re

# Fonction pour nettoyer les caractères spéciaux, mais conserver les lettres accentuées
def remove_special_characters(text):
    # Remplacer tous les caractères non ASCII, sauf les lettres accentuées
    return re.sub(r'[^\x00-\x7FéèêôîùàâçÉÈÊÔÎÙÀÂÇ]+', '', text)

# Connexion à la base de données
conn = sqlite3.connect("articles.db")
cursor = conn.cursor()

# Récupérer les articles depuis la base
cursor.execute("SELECT id, title, source FROM articles")
articles = cursor.fetchall()

st.title("📰 Revue des Articles")
st.write("Sélectionnez les articles à inclure dans le PDF :")

if not articles:
    st.warning("Aucun article trouvé.")
else:
    # Interface de sélection
    selected_ids = []
    for article in articles:
        id_, title, source = article
        if st.checkbox(f"{title} ({source})", key=id_):
            selected_ids.append(id_)

    # Bouton pour générer le PDF
    if st.button("📄 Générer le PDF") and selected_ids:
        cursor.execute(
            f"SELECT title, url, publication_date, summary, source FROM articles WHERE id IN ({','.join(['?']*len(selected_ids))})",
            selected_ids
        )
        selected_articles = cursor.fetchall()

        # Création du PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Page de garde
        pdf.add_page()
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(200, 10, txt=remove_special_characters("📰 Revue des Articles Sélectionnés"), ln=True, align="C")
        pdf.ln(10)
        
        # Si tu veux ajouter un logo, décommente la ligne suivante et mets le chemin de ton logo
        # pdf.image('logo.png', x=10, y=20, w=30)

        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=remove_special_characters("Sélectionnez vos articles préférés"), ln=True, align="C")
        pdf.ln(20)

        # Création du contenu
        pdf.set_font("Arial", size=12)
        for title, url, publication_date, summary, source in selected_articles:
            # Nettoyer les titres et résumés des caractères spéciaux
            clean_title = remove_special_characters(title)
            clean_summary = remove_special_characters(summary)

            pdf.set_font("Arial", style='B', size=14)
            pdf.multi_cell(0, 10, clean_title)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Date : {publication_date} | Source : {source}", ln=True)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 10, f"{url}", ln=True, link=url)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, clean_summary)
            pdf.ln(10)

        # Sauvegarde et téléchargement
        pdf.output("selected_articles.pdf")
        
        # Message de succès
        st.success("✅ PDF généré avec succès ! Vous pouvez le télécharger ci-dessous.")

        # Bouton de téléchargement
        with open("selected_articles.pdf", "rb") as f:
            st.download_button("📥 Télécharger le PDF", f, file_name="articles_selectionnés.pdf", mime="application/pdf")
