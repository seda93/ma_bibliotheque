def formater_auteurs(auteurs_liste):
    return ", ".join(auteurs_liste)

def nettoyer_texte(texte):
    return texte.strip() if texte else ""
