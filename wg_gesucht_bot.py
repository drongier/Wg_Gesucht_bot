import requests
from bs4 import BeautifulSoup
import time
import telegram
import asyncio
import json
import logging
from datetime import datetime
import os

def load_config():
    """Charge la configuration depuis le fichier config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("❌ Fichier config.json non trouvé!")
        raise

# Charger la configuration
config = load_config()

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.get('LOG_FILE', 'wgbot.log')),
        logging.StreamHandler()
    ]
)

# === CONFIGURATION ===
URL = config['URL']
BOT_TOKEN = config['BOT_TOKEN']
CHAT_ID = config['CHAT_ID']

# Mots-clés à exclure (en minuscules)
EXCLUDED_KEYWORDS = [
    "tausch",
    "nur frauen",
    "coworking",
    "büro",
    "büroräum",
    "büroraum",
    "praxis",
]

# Fichier pour sauvegarder les IDs vus
SEEN_IDS_FILE = config.get('SEEN_IDS_FILE', 'seen_ids.json')

def load_seen_ids():
    """Charge les IDs déjà vus depuis le fichier"""
    try:
        with open(SEEN_IDS_FILE, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen_ids(seen_ids):
    """Sauvegarde les IDs vus dans le fichier"""
    with open(SEEN_IDS_FILE, 'w') as f:
        json.dump(list(seen_ids), f)

# Initialisation du bot
bot = telegram.Bot(token=BOT_TOKEN)

def should_exclude_listing(title, description=""):
    """Vérifie si l'annonce doit être exclue selon les mots-clés"""
    text_to_check = f"{title} {description}".lower()
    
    for keyword in EXCLUDED_KEYWORDS:
        if keyword in text_to_check:
            logging.info(f"🚫 Annonce exclue (mot-clé: '{keyword}'): {title[:50]}...")
            return True
    return False

async def send_telegram_message(message):
    """Envoie un message via Telegram de façon asynchrone"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        return True
    except Exception as e:
        logging.error(f"❌ Erreur envoi Telegram: {e}")
        return False

async def main():
    # Charger les IDs déjà vus
    SEEN_IDS = load_seen_ids()
    
    # Message de ping au démarrage
    start_msg = f"✅ Bot WG démarré sur Raspberry Pi à {datetime.now().strftime('%H:%M:%S')}"
    await send_telegram_message(start_msg)
    
    logging.info("🚀 Surveillance des nouvelles annonces WG-Gesucht démarrée...")
    logging.info(f"🚫 Mots-clés exclus: {', '.join(EXCLUDED_KEYWORDS)}")
    
    while True:
        try:
            logging.info(f"🔍 Scan en cours... {datetime.now().strftime('%H:%M:%S')}")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            res = requests.get(URL, headers=headers, timeout=30)
            logging.info(f"📡 Status HTTP: {res.status_code}")
            
            if res.status_code != 200:
                logging.error(f"❌ Erreur HTTP: {res.status_code}")
                await asyncio.sleep(300)
                continue
                
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("article")
            logging.info(f"📊 Articles trouvés: {len(articles)}")
            
            new_count = 0
            excluded_count = 0
            
            for article in articles:
                ad_id = article.get("data-id") or article.get("id") or article.get("data-adid")
                
                if ad_id and ad_id not in SEEN_IDS:
                    SEEN_IDS.add(ad_id)
                    
                    title_tag = (article.find("h2") or 
                                article.find("h3") or 
                                article.find("a", href=True))
                    
                    link_tag = article.find("a", href=True)
                    
                    if title_tag and link_tag:
                        title = title_tag.get_text(strip=True)
                        
                        description_tag = article.find("p") or article.find("div", class_="text-module-begin")
                        description = description_tag.get_text(strip=True) if description_tag else ""
                        
                        if should_exclude_listing(title, description):
                            excluded_count += 1
                            continue
                        
                        new_count += 1
                        href = link_tag.get("href")
                        
                        if href.startswith("/"):
                            link = "https://www.kleinanzeigen.de" + href
                        elif href.startswith("http"):
                            link = href
                        else:
                            link = "https://www.kleinanzeigen.de/" + href
                            
                        message = f"🏠 Nouvelle annonce WG !\n{title}\n{link}"
                        
                        if await send_telegram_message(message):
                            logging.info(f"✅ Nouvelle annonce envoyée : {title}")
            
            # Sauvegarder les IDs vus
            save_seen_ids(SEEN_IDS)
            
            logging.info(f"📈 {new_count} nouvelles, {excluded_count} exclues. Total: {len(SEEN_IDS)}")
            
            # Attendre 10 minutes
            logging.info("⏰ Attente 10 min avant le prochain scan...")
            await asyncio.sleep(600)
            
        except Exception as e:
            logging.error(f"⚠️ Erreur : {e}")
            await send_telegram_message(f"⚠️ Erreur bot Pi: {str(e)}")
            await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())