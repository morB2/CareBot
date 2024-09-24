from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def web_scraping(disease_name, question_word):
    """
    Scrapes information about a disease from the Infomed website.

    Parameters:
    disease_name (str): The name of the disease to search for.
    question_word (str): The specific question word or category to look for.

    Returns:
    str: The HTML content of the relevant section of the disease page.
    """

    # Set up the WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-images")
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the disease page
        driver.get(f"https://www.infomed.co.il/diseases/{disease_name}")

        if question_word:
            # Locate the drawers list element
            disease_drawers_list = driver.find_elements(By.CSS_SELECTOR,
                                                        ".centeredContent.encyclopediaSection-bottom > div.drawers_list")
            if not disease_drawers_list:
                print("No drawers list found")
                return "לא נמצא מידע על המחלה"

            ul = disease_drawers_list[0].find_elements(By.CSS_SELECTOR, ".drawer")
            question_info = ""
            for li in ul:
                if (li.find_elements(By.TAG_NAME, "h2"))[0].text == question_word:
                    li.click()
                    # Wait for the content to load after click
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.visibility_of(li))
                    question_info = li.get_attribute('outerHTML')
            if not question_info:
                print("Question word not found in drawers list")
            print('Finish scraping')
            return question_info
        else:
            # Scrape the disease description if no specific question word is provided
            disease_description = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".centeredContent.encyclopediaSection-bottom > div.description"))
            )
            disease_info_description = "\n".join(
                [element.get_attribute('outerHTML') for element in disease_description])
            driver.quit()
            # print('finish scraping')
            return disease_info_description
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return "אירעה תקלה במהלך קריאת הנתונים מהאתר"
    finally:
        driver.quit()


diseases = [
    'דלקת ריאות',
    'אלרגיה',
    'אסטמה',
    'מיגרנה',
    'צהבת',
    'מלריה',
    'התקף לב',
    'אקנה',
    'שפעת',
    'כאב בטן',
    'דלקת גרון',
    'דלקת עיניים',
    'אבעבועות רוח',
]

question_words = [
    "סיבות וגורמי סיכון",
    "אבחון ובדיקות",
    "סיבוכים אפשריים",
    "טיפולים ותרופות",
    "מניעה"
]

data = {}

for disease in diseases:
    disease_data = {}
    for question_word in question_words:
        result = web_scraping(disease, question_word)
        disease_data[question_word] = result

    description = web_scraping(disease, "")
    disease_data["תיאור כללי"] = description

    data[disease] = disease_data

with open('diseases_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("הנתונים נשמרו בהצלחה בקובץ diseases_data.json")
