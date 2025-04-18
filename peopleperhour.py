from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
import time

# Initialiser le navigateur
driver = webdriver.Chrome()
driver.get("https://www.peopleperhour.com/services/technology-programming/social-media-app")
time.sleep(5)

# Créer le fichier Excel
wb = Workbook()
ws = wb.active
ws.append(["Titre", "Lien Profil", "Prix", "Votes"])  # En-têtes

while True:
    time.sleep(3)  # Laisse le temps à la page de se charger

    # Récupérer les éléments
    titres = driver.find_elements(By.CSS_SELECTOR, "div > div:nth-child(2) > ul > li > div > a > h2")
    profiles = driver.find_elements(By.CSS_SELECTOR, "div > div:nth-child(2) > ul > li > div > div[class*='card__meta'] > div[class*='card__user'] > a")
    prix = driver.find_elements(By.CSS_SELECTOR, "div > div:nth-child(2) > ul > li > div > div[class*='card__meta'] > div[class*='card__price'] > span > span")
    votes = driver.find_elements(By.CSS_SELECTOR, "div > div:nth-child(2) > ul > li > div > div[class*='card__meta'] > div[class*='card__user'] > a > span > span[class*='card__freelancer-ratings'] > span")

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
        next_button = driver.find_element(By.XPATH, "//li[contains(@class, 'pagination__item--next')]/a")
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        time.sleep(1)
        ActionChains(driver).move_to_element(next_button).click().perform()
        print("Page suivante...")
        time.sleep(5)
    except NoSuchElementException:
        print("Plus de page suivante.")
        break

# Sauvegarder le fichier
wb.save("peopelesocialmedia.gigs.xlsx")
driver.quit()
