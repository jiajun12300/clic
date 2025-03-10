from flask import Flask, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os

app = Flask(__name__)

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")  # Open full-screen
options.add_experimental_option("detach", True)  # Keep browser open

# Start the browser and open the website
driver = webdriver.Chrome(options=options)
driver.get("https://clic.mmu.edu.my/psp/csprd/?cmd=login")

# Function to keep session alive
def keep_alive():
    while True:
        try:
            time.sleep(60)  # Every 1 minute
            driver.execute_script("document.getElementById('PT_HOME').click();")
            print("Clicked 'Home' button to keep session alive.")
        except Exception as e:
            print(f"Error: {e}")
            break

# Start keep-alive function
import threading
threading.Thread(target=keep_alive, daemon=True).start()

@app.route("/")
def index():
    return redirect("https://clic.mmu.edu.my/psp/csprd/?cmd=login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
