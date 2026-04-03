# =============================================================
# Week 3 – Automation Testing | Dashboard Functionality Test
# Author: Muhammad Huzaifa
# Tool: Selenium WebDriver (Python)
# Test Case: TC_AUTO_004 & TC_AUTO_005 – Feature Tests
# =============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import logging

# ── Logging Setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://the-internet.herokuapp.com"

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
# TC_AUTO_004 – Dropdown Feature Test
# ══════════════════════════════════════════════════════════
def test_dropdown_functionality(driver):
    logger.info("▶ TC_AUTO_004 | Dropdown Feature Test – STARTED")
    driver.get(f"{BASE_URL}/dropdown")

    from selenium.webdriver.support.ui import Select
    dropdown = Select(driver.find_element(By.ID, "dropdown"))

    # Select option 1
    dropdown.select_by_value("1")
    selected = dropdown.first_selected_option.text
    assert "Option 1" in selected, f"Expected Option 1, got {selected}"
    logger.info("   ✔ Option 1 selected successfully: %s", selected)

    # Select option 2
    dropdown.select_by_value("2")
    selected = dropdown.first_selected_option.text
    assert "Option 2" in selected, f"Expected Option 2, got {selected}"
    logger.info("   ✔ Option 2 selected successfully: %s", selected)

    logger.info("✅ TC_AUTO_004 PASSED – Dropdown works correctly.")
    return "PASS"


# ══════════════════════════════════════════════════════════
# TC_AUTO_005 – Dynamic Content / Checkbox Feature Test
# ══════════════════════════════════════════════════════════
def test_checkbox_functionality(driver):
    logger.info("▶ TC_AUTO_005 | Checkbox Feature Test – STARTED")
    driver.get(f"{BASE_URL}/checkboxes")

    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    assert len(checkboxes) == 2, f"Expected 2 checkboxes, found {len(checkboxes)}"

    # Check state of checkbox 1
    cb1_initial = checkboxes[0].is_selected()
    checkboxes[0].click()
    cb1_after = checkboxes[0].is_selected()
    assert cb1_initial != cb1_after, "Checkbox 1 state did not toggle"
    logger.info("   ✔ Checkbox 1 toggled: %s → %s", cb1_initial, cb1_after)

    # Check state of checkbox 2
    cb2_initial = checkboxes[1].is_selected()
    checkboxes[1].click()
    cb2_after = checkboxes[1].is_selected()
    assert cb2_initial != cb2_after, "Checkbox 2 state did not toggle"
    logger.info("   ✔ Checkbox 2 toggled: %s → %s", cb2_initial, cb2_after)

    logger.info("✅ TC_AUTO_005 PASSED – Checkboxes functioning correctly.")
    return "PASS"


# ══════════════════════════════════════════════════════════
# TC_AUTO_006 – Alert Handling Test
# ══════════════════════════════════════════════════════════
def test_alert_handling(driver):
    logger.info("▶ TC_AUTO_006 | Alert Handling Test – STARTED")
    driver.get(f"{BASE_URL}/javascript_alerts")

    # Click JS Alert button
    alert_btn = driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']")
    alert_btn.click()

    wait = WebDriverWait(driver, 5)
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    logger.info("   ✔ Alert appeared with text: %s", alert_text)
    alert.accept()

    # Verify result
    result = driver.find_element(By.ID, "result")
    assert "You successfully clicked an alert" in result.text
    logger.info("✅ TC_AUTO_006 PASSED – Alert handled correctly.")
    return "PASS"


# ══════════════════════════════════════════════════════════
# TC_AUTO_007 – Navigation / Link Click Test
# ══════════════════════════════════════════════════════════
def test_navigation(driver):
    logger.info("▶ TC_AUTO_007 | Navigation Test – STARTED")
    driver.get(BASE_URL)

    # Find and click 'Form Authentication' link
    link = driver.find_element(By.LINK_TEXT, "Form Authentication")
    link.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "username")))

    current_url = driver.current_url
    assert "login" in current_url, f"Navigation failed. URL: {current_url}"
    logger.info("   ✔ Navigated to: %s", current_url)
    logger.info("✅ TC_AUTO_007 PASSED – Navigation works correctly.")
    return "PASS"


# ══════════════════════════════════════════════════════════
# Main Runner
# ══════════════════════════════════════════════════════════
def run_all_tests():
    driver = get_driver()
    results = {}

    try:
        results["TC_AUTO_004 – Dropdown Feature"]   = test_dropdown_functionality(driver)
        results["TC_AUTO_005 – Checkbox Feature"]   = test_checkbox_functionality(driver)
        results["TC_AUTO_006 – Alert Handling"]     = test_alert_handling(driver)
        results["TC_AUTO_007 – Navigation Test"]    = test_navigation(driver)
    except Exception as e:
        logger.error("Test suite error: %s", str(e))
    finally:
        driver.quit()

    print("\n" + "="*58)
    print("   DASHBOARD FEATURE TEST SUITE – RESULTS SUMMARY")
    print("   Prepared by: Muhammad Huzaifa")
    print("="*58)
    for tc, status in results.items():
        mark = "✅" if "PASS" in status else "❌"
        print(f"  {mark} {tc:42s}  {status}")
    print("="*58)
    passed = sum(1 for s in results.values() if "PASS" in s)
    print(f"  Total: {len(results)} | Passed: {passed} | Failed: {len(results) - passed}")
    print("="*58 + "\n")


if __name__ == "__main__":
    run_all_tests()
