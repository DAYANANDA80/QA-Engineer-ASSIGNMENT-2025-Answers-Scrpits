from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class OrangeHRMAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def open_url(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        print("[INFO] Logged in successfully.")

    def navigate_to_pim(self):
        pim_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        pim_tab.click()
        print("[INFO] Navigated to PIM module.")

    def add_employees(self, employee_list):
        for emp in employee_list:
            # Navigate to Add Employee page
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()

            # Fill first and last name
            first_name_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
            first_name_field.clear()
            first_name_field.send_keys(emp["first"])

            last_name_field = self.driver.find_element(By.NAME, "lastName")
            last_name_field.clear()
            last_name_field.send_keys(emp["last"])

            # Save
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

            # Wait for Personal Details page
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Personal Details']")))
            print(f"[INFO] Employee Added: {emp['first']} {emp['last']}")

        # Wait before verification to ensure records are updated
        print("[INFO] Waiting 5 seconds before verification...")
        time.sleep(5)

    def verify_employees(self, employee_list):
        for emp in employee_list:
            self.driver.refresh()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Employee List']"))).click()

            full_name = f"{emp['first']} {emp['last']}"
            print(f"[INFO] Verifying employee: {full_name}")

            found = False
            for attempt in range(2):  # Try twice
                search_input = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//input[@placeholder='Type for hints...']")))
                search_input.clear()
                search_input.send_keys(full_name)

                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']"))).click()
                time.sleep(2)

                try:
                    result_name = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, f"//div[@role='row']//div[contains(text(), '{emp['first']}')]")))
                    print(f"[PASS] Found: {result_name.text}")
                    found = True
                    break
                except:
                    print(f"[WARN] Attempt {attempt+1} failed for: {full_name}, retrying...")
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='reset']"))).click()
                    time.sleep(2)

            if not found:
                print(f"[FAIL] Not Found: {full_name}")

    def logout(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))).click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))).click()
        print("[INFO] Logged out successfully.")

    def close(self):
        self.driver.quit()
        print("[INFO] Browser closed successfully.")


# ==================== EXECUTION ====================
if __name__ == "__main__":
    app = OrangeHRMAutomation()
    app.open_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Demo credentials
    app.login("Admin", "admin123")
    app.navigate_to_pim()

    employees = [
        {"first": "Daya", "last": "Analyst"},
        {"first": "Moksha", "last": "Dev"},
        {"first": "Sowmya", "last": "QA"}
    ]

    app.add_employees(employees)
    app.verify_employees(employees)

    app.logout()
    app.close()
