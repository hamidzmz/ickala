from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import os


def process_images(images):
    # راه‌اندازی مرورگر Chrome
    driver = webdriver.Chrome()

    # باز کردن صفحه وب
    driver.get("https://dewatermark.ai/")

    try:
        # وارد کردن مسیر عکس‌ها به صورت یکجا
        input_paths = ' '.join(['"{}"'.format(os.path.join(folder_path, image_file)) for image_file in images])

        # صبر کردن تا المان قابل کلیک باشد
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/button'))
        )

        # کلیک کردن بر روی المان
        element.click()
        time.sleep(3)

        # وارد کردن مسیر عکس‌ها
        pyautogui.typewrite(r'"{}"'.format(input_paths))
        pyautogui.press('enter')

        # صبر کردن تا المان مورد نظر بر روی صفحه ظاهر شود
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]'))
        )

        # کلیک کردن بر روی المان دیگر
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]').click()

        # صبر کردن تا المان مورد نظر دیگر ظاهر شود
        WebDriverWait(driver, 1000000).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div/div/div/div/div[1]/div'))
        )

        # Wait for the button to be visible and clickable
        button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Download")]'))  # Adjust XPath if needed
        )
        # Click the button
        driver.execute_script("arguments[0].click();", button2)

        WebDriverWait(driver, 1000000).until(
            EC.staleness_of(driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div[1]/div/div/div')))
    finally:
        # در پایان بستن مرورگر
        driver.quit()


folder_path = r"E:\bedoneBG-IC"
# پیدا کردن تمامی فایل‌های عکس در پوشه
image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# تقسیم لیست عکس‌ها به گروه‌های 500 تایی
for i in range(0, len(image_files), 500):
    images_group = image_files[i:i+500]
    process_images(images_group)
