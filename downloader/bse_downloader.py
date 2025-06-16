import os
import time
import re
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_status(log_file, security_code, found, status):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"Security code: {security_code}, Found: {found}, Status: {status}\n")

def get_last_processed_code(log_file):
    if not os.path.exists(log_file):
        return None
    with open(log_file, "r", encoding="utf-8") as log:
        lines = log.readlines()
        for line in reversed(lines):
            if "Downloaded" in line:
                return line.split(",")[0].split(":")[1].strip()
    return None

def clean_company_name(name):
    return re.sub(r'[<>:"/\\|?*\n\r]', "", name).strip()

def download_annual_reports(csv_file, target_year, download_folder, log_file):
    last_processed_code = get_last_processed_code(log_file)
    df = pd.read_csv(csv_file, dtype={"Security Code": str}).dropna().drop_duplicates()
    if last_processed_code and last_processed_code in df["Security Code"].values:
        start_index = df[df["Security Code"] == last_processed_code].index[0] + 1
    else:
        start_index = 0
    security_codes = df["Security Code"].iloc[start_index:].tolist()
    os.makedirs(download_folder, exist_ok=True)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.bseindia.com/corporates/HistoricalAnnualReport.aspx")
    time.sleep(3)
    wait = WebDriverWait(driver, 2)
    for security_code in security_codes:
        print(f"🔎 Processing company with Security Code: {security_code}")
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_SmartSearch_smartSearch")))
            search_box.clear()
            search_box.send_keys(security_code)
            time.sleep(1)
            dropdown_items = driver.find_elements(By.XPATH, "//ul[@id='ulSearchQuote2']/li")
            if not dropdown_items or "No Match Found" in dropdown_items[0].text:
                log_status(log_file, security_code, "No", "No company found")
                continue
            company_name = clean_company_name(dropdown_items[0].text.split("\n")[0])
            driver.execute_script("arguments[0].click();", dropdown_items[0])
            time.sleep(1)
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Submit']")))
            driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(2)
            try:
                table = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdAnnualReport")))
            except:
                log_status(log_file, security_code, "No", "No annual report data found")
                continue
            rows = driver.find_elements(By.XPATH, "//table[@id='ContentPlaceHolder1_grdAnnualReport']/tbody/tr")
            year_found = False
            for row in rows:
                year_element = row.find_elements(By.XPATH, "./td[1]")
                if year_element:
                    year = year_element[0].text.strip()
                    pdf_element = row.find_elements(By.XPATH, "./td[2]/a")
                    pdf_link = pdf_element[0].get_attribute("href") if pdf_element else None
                    if year == target_year and pdf_link:
                        year_found = True
                        file_path = os.path.join(download_folder, f"{company_name}_{year}.pdf")
                        headers = {"User-Agent": "Mozilla/5.0"}
                        response = requests.get(pdf_link, headers=headers, stream=True, allow_redirects=True)
                        if response.status_code == 200:
                            with open(file_path, "wb") as file:
                                for chunk in response.iter_content(1024):
                                    file.write(chunk)
                            log_status(log_file, security_code, "Yes", "Downloaded")
                        else:
                            log_status(log_file, security_code, "No", f"Download failed (Status: {response.status_code})")
            if not year_found:
                log_status(log_file, security_code, "No", f"No annual report found for {target_year}")
        except Exception as e:
            log_status(log_file, security_code, "No", f"Error: {str(e)}")
            break
    driver.quit()
    log_status(log_file, "Final", "N/A", "Process completed")
