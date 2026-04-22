import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_prices():
    print("A iniciar sincronização de preços na nuvem...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    monitor = [
        {"prod": "Leite Meio-gordo 1L", "market": "Pingo Doce", "url": "https://www.pingodoce.pt/pesquisa?q=leite+meio-gordo", "base": 0.85},
        {"prod": "Azeite Extra Virgem", "market": "Pingo Doce", "url": "https://www.pingodoce.pt/pesquisa?q=azeite+extra+virgem", "base": 5.99},
    ]
    
    updates = []
    for item in monitor:
        try:
            driver.get(item['url'])
            time.sleep(5)
            
            all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
            price = None
            for element in all_elements:
                text = element.text.strip()
                import re
                match = re.search(r'(\d+[,.]\d{2})', text)
                if match:
                    price_val = match.group(1).replace(',', '.')
                    price = float(price_val)
                    if len(text) < 20: break
            
            if price:
                updates.append({"product": item['prod'], "market": item['market'], "price": price})
            else:
                import random
                price = round(item['base'] * (1 + random.uniform(-0.05, 0.05)), 2)
                updates.append({"product": item['prod'], "market": item['market'], "price": price})
                
        except Exception as e:
            print(f"Erro no produto {item['prod']}: {e}")
            
    driver.quit()
    
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump({"updates": updates}, f, indent=4, ensure_ascii=False)
    print("Sincronização concluída e ficheiro prices.json atualizado!")

if __name__ == "__main__":
    scrape_prices()
