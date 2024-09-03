import time
import os
import logging
import threading
from platform import system as platform_system
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import winsound

current_platform = platform_system()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Edge
        self._implicit_wait_time = 3

    def __enter__(self) -> webdriver.Edge:
        logging.info("Opening browser")
        options = webdriver.EdgeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Edge(options=options)
        self._driver.implicitly_wait(self._implicit_wait_time)
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/83.0.4103.53 Safari/537.36'
        })
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Closing browser")
        if hasattr(self, '_driver'):
            self._driver.quit()

class BerlinBot:
    def __init__(self):
        self.wait_time = 3
        self._sound_file = os.path.join(os.getcwd(), "alarm.wav")

    @staticmethod
    def visit_start_page(driver: webdriver.Edge):
        login = "A194095"
        logging.info("Visiting start page")
        driver.get("https://dsp.dekra.de/login/xhtml/mainpage.jsf")
        login_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm-username"]'))
        )
        login_input.send_keys(login)

    @staticmethod
    def enter_password(driver: webdriver.Edge):
        password = "Adventure704."
        logging.info("Entering password")
        password_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm-password"]'))
        )
        password_input.send_keys(password)

    @staticmethod
    def confirm_login(driver: webdriver.Edge):
        logging.info("Confirming login")
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm-loginLink"]'))
        )
        login_button.click()

    @staticmethod
    def click_first_option(driver: webdriver.Edge):
        logging.info("Selecting first option")
        first_option = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt74-0-j_idt81-3-j_idt82-j_idt84-0-img-"]'))
        )
        first_option.click()

    @staticmethod
    def select_second_option(driver: webdriver.Edge):
        logging.info("Selecting second option")
        second_option = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/ul[2]/li[3]/a'))
        )
        second_option.click()

    @staticmethod
    def the_next_week(driver: webdriver.Edge):
        logging.info("Selecting next week")
        for _ in range(3):
            next_week_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[3]'))
            )
            next_week_button.click()
            time.sleep(1)

    @staticmethod
    def select_ort(driver: webdriver.Edge):
        logging.info("Selecting ort")
        ort_dropdown = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="scheduling-panel-form:j_idt55"]'))
        )
        ort_dropdown.click()
        time.sleep(1)

    @staticmethod
    def select_place(driver: webdriver.Edge):
        logging.info("Selecting place")
        place_option = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="scheduling-panel-form:j_idt55_12"]'))
        )
        place_option.click()
        time.sleep(1)

    @staticmethod
    def select_termin(driver: webdriver.Edge):
        logging.info("Selecting termin")
        try:
            slots = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.slot.available'))
            )
            return slots
        except:
            return []

    # def select_applicant(self, driver: webdriver.Edge, person_index: int):
    #     logging.info(f"Selecting applicant with index {person_index}")
    #     applicant_dropdown = WebDriverWait(driver, 3).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt196:j_idt245"]'))
    #     )
    #     applicant_dropdown.click()
    #     time.sleep(1)
    #     applicant_option = WebDriverWait(driver, 3).until(
    #         EC.element_to_be_clickable((By.XPATH, f'//*[@id="j_idt196:j_idt245_{person_index}"]'))
    #     )
    #     applicant_option.click()
    #     time.sleep(1)

    def create_termin(self, driver: webdriver.Edge, place: str, person_index: int):
        while True:
            logging.info(f"Creating termin for person")
            create_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt196:j_idt275"]'))
            )
            create_button.click()
            time.sleep(2)

            # try:
            #     error_block = driver.find_element(By.CLASS_NAME, "error-block")
            #     if error_block.is_displayed():
            #         logging.error(f"Error encountered during termin creation for person with index {person_index}.")

            #         logging.info(f"Selecting next person due to error.")
            #         person_index += 1
            #         self.select_applicant(driver, person_index)

            #         continue  
            # except:
            # logging.info(f"Termin created successfully for person with index {person_index}.")
            # self.play_sound_for_duration(self._sound_file, 1)
            # return True 

    @staticmethod
    def play_sound_for_duration(sound_file: str, duration: int):
        """Play sound for a specific duration in seconds."""
        def play_sound():
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
        time.sleep(1)
        
        winsound.PlaySound(None, winsound.SND_PURGE)

    def perform_login(self):
        with WebDriver() as driver:
            self.visit_start_page(driver)
            self.enter_password(driver)
            self.confirm_login(driver)
            self.click_first_option(driver)
            self.select_second_option(driver)
            self.select_ort(driver)
            self.select_place(driver)
            self.the_next_week(driver)

            # person_index = 1
            # while person_index <= 100:
            slots = self.select_termin(driver)
            if not slots:
                logging.info("No slots available. Ending process.")
                return 

            slots[0].click()

                # self.select_applicant(driver, person_index)
            # success = self.create_termin(driver, place="Berlin", person_index=person_index)
            success = self.create_termin(driver, place="Berlin")

            if success:
                logging.info(f"Termin created. Moving to next person in queue.")
            else:
                logging.warning(f"Failed to create termin for person")

            # person_index += 1 

                # if person_index > 80: 
                #     logging.info("All persons tried. Ending process.")
                #     return 

if __name__ == "__main__":
    bot = BerlinBot()
    bot.perform_login()