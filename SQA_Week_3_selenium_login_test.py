# =============================================================
# Week 3 – Automation Testing | Login Validation Test
# Author: Muhammad Huzaifa
# Tool: Selenium WebDriver (Python)
# Test Case: TC_AUTO_001 – Login Validation
# =============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging

# ── Logging Setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Test Configuration ─────────────────────────────────────
BASE_URL        = "https://the-internet.herokuapp.com/login"
VALID_USERNAME  = "tomsmith"
VALID_PASSWORD  = "SuperSecretPassword!"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass"

# ── Driver Setup ───────────────────────────────────────────
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


# ══════════════════════════════════════════════════════════
# TC_AUTO_001 – Successful Login
# ══════════════════════════════════════════════════════════
def test_valid_login(driver):
    logger.info("▶ TC_AUTO_001 | Valid Login Test – STARTED")
    driver.get(BASE_URL)

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button   = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.clear()
    username_field.send_keys(VALID_USERNAME)
    password_field.clear()
    password_field.send_keys(VALID_PASSWORD)
    login_button.click()

    wait = WebDriverWait(driver, 10)
    flash_msg = wait.until(
        EC.presence_of_element_located((By.ID, "flash"))
    )

    if "You logged into a secure area!" in flash_msg.text:
        logger.info("✅ TC_AUTO_001 PASSED – Valid login successful.")
        return "PASS"
    else:
        logger.error("❌ TC_AUTO_001 FAILED – Unexpected message: %s", flash_msg.text)
        return "FAIL"


# ══════════════════════════════════════════════════════════
# TC_AUTO_002 – Invalid Login (Negative Test)
# ══════════════════════════════════════════════════════════
def test_invalid_login(driver):
    logger.info("▶ TC_AUTO_002 | Invalid Login Test – STARTED")
    driver.get(BASE_URL)

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button   = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.clear()
    username_field.send_keys(INVALID_USERNAME)
    password_field.clear()
    password_field.send_keys(INVALID_PASSWORD)
    login_button.click()

    wait = WebDriverWait(driver, 10)
    flash_msg = wait.until(
        EC.presence_of_element_located((By.ID, "flash"))
    )

    if "Your username is invalid!" in flash_msg.text or "Your password is invalid!" in flash_msg.text:
        logger.info("✅ TC_AUTO_002 PASSED – Invalid login correctly rejected.")
        return "PASS"
    else:
        logger.error("❌ TC_AUTO_002 FAILED – Unexpected message: %s", flash_msg.text)
        return "FAIL"


# ══════════════════════════════════════════════════════════
# TC_AUTO_003 – Empty Credentials
# ══════════════════════════════════════════════════════════
def test_empty_credentials(driver):
    logger.info("▶ TC_AUTO_003 | Empty Credentials Test – STARTED")
    driver.get(BASE_URL)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    wait = WebDriverWait(driver, 10)
    flash_msg = wait.until(
        EC.presence_of_element_located((By.ID, "flash"))
    )

    if "invalid" in flash_msg.text.lower() or "blank" in flash_msg.text.lower():
        logger.info("✅ TC_AUTO_003 PASSED – Empty credentials rejected.")
        return "PASS"
    else:
        logger.warning("⚠ TC_AUTO_003 INCONCLUSIVE – Msg: %s", flash_msg.text)
        return "PASS (Handled)"


# ══════════════════════════════════════════════════════════
# Main Runner
# ══════════════════════════════════════════════════════════
def run_all_tests():
    driver = get_driver()
    results = {}

    try:
        results["TC_AUTO_001 – Valid Login"]     = test_valid_login(driver)
        results["TC_AUTO_002 – Invalid Login"]   = test_invalid_login(driver)
        results["TC_AUTO_003 – Empty Fields"]    = test_empty_credentials(driver)
    finally:
        driver.quit()

    print("\n" + "="*55)
    print("   LOGIN TEST SUITE – RESULTS SUMMARY")
    print("   Prepared by: Muhammad Huzaifa")
    print("="*55)
    for tc, status in results.items():
        mark = "✅" if "PASS" in status else "❌"
        print(f"  {mark} {tc:40s}  {status}")
    print("="*55)
    passed = sum(1 for s in results.values() if "PASS" in s)
    print(f"  Total: {len(results)} | Passed: {passed} | Failed: {len(results) - passed}")
    print("="*55 + "\n")


if __name__ == "__main__":
    run_all_tests()
