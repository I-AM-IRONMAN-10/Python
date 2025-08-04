from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Launch WhatsApp Web
driver = webdriver.Safari()  # Requires ChromeDriver in PATH
driver.get("https://web.whatsapp.com")

# Step 2: Wait for QR scan and interface load
input("📱 Scan the QR code in WhatsApp Web and press Enter when ready...")

# Step 3: Define contact and message
contact = "sam"  # Make sure it matches exactly
message = "Hello, this is a fully automated message from Selenium!"

try:
    # Step 4: Wait for the search box to become visible
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(contact)
    time.sleep(2)

    # Step 5: Click on the contact from the list
    contact_xpath = f'//span[@title="{contact}"]'
    contact_title = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, contact_xpath))
    )
    contact_title.click()

    # Step 6: Type the message
    msg_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
    )
    msg_box.click()
    msg_box.send_keys(message + Keys.ENTER)

    print("✅ Message sent successfully!")

except Exception as e:
    print("❌ Failed to send message:", e)

# Optional: Keep WhatsApp open for a bit
time.sleep(5)
driver.quit()