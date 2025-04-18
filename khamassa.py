from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time

# Initialiser le navigateur
driver = webdriver.Chrome()
driver.get("https://khamsat.com/programming/desktop-app")
time.sleep(5)

# Créer le fichier Excel
wb = Workbook()
ws = wb.active
ws.append(["Titre", "Lien Profil", "Prix", "Votes"])  # En-têtes

while True:
    time.sleep(3)  # Laisse le temps à la page de se charger

    # Récupérer les éléments
    titres = driver.find_elements(By.CSS_SELECTOR, "div > div.product-body > h4 > a")
    profiles = driver.find_elements(By.CSS_SELECTOR, "div.product-user > a")
    prix = driver.find_elements(By.CSS_SELECTOR, "div > div.product-body > div.product-price > div > span")
    votes = driver.find_elements(By.CSS_SELECTOR, "div > div.product-body > div.product-body-rate.line-clamp-1 > a > ul > li.c-list__item.info")

    # Boucle sur les éléments, tous ensemble
    for t, p, pr, v in zip(titres, profiles, prix, votes):
        titre_text = t.text.strip()
        profile_link = p.get_attribute('href').strip()
        price_text = pr.text.strip()
        vote_text = v.text.strip()

        if titre_text and profile_link:
            print(f"{titre_text} | {profile_link} | {price_text} | {vote_text}")
            ws.append([titre_text, profile_link, price_text, vote_text])

    # Passer à la page suivante
    try:
        next_button = driver.find_element(By.LINK_TEXT, "التالي")  # "Suivant" en arabe
        next_button.click()
    except:
        print("Pas de page suivante.")
        break

# Sauvegarder le fichier
wb.save("khamassatdesktop.gigs.xlsx")
driver.quit()
