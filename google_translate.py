from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import pysrt

def init_driver(language_code):
    #firefox_options = Options()
    #firefox_options.add_argument("--disable-extensions")
    #firefox_options.add_argument("--disable-gpu")
    #firefox_options.add_argument("--headless")
    driver = webdriver.Firefox()
    driver.get('https://translate.google.com/#view=home&op=translate&sl=en&tl='+language_code)
    return driver

def put_text_get_translation(text, driver):
    input_selector = 'textarea'
    time.sleep(1)
    driver.find_element(By.TAG_NAME,"textarea").clear() 
    driver.find_element(By.TAG_NAME,"textarea").send_keys(text)
    time.sleep(1)
    output = driver.find_elements(By.CSS_SELECTOR,'c-wiz')[11].find_elements(By.CSS_SELECTOR,'span > span >span' )[0].text
    print(output)
    return output

def get_translated_srt(srt_file, language_code):
    driver = init_driver(language_code)

    original_subs = pysrt.open(srt_file)
    translated_subs = pysrt.open(srt_file)

    for n,subtitle in enumerate(original_subs):
        translated_subs[n].text = put_text_get_translation(subtitle.text, driver)

    return translated_subs

