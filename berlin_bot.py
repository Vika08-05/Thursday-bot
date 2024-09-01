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
        self.people_queue = [
            {"name": "Statnik, Illia", "index": 57},
            {"name": "Buiankova, Maiia", "index": 12},
            {"name": "Ahmadi, Ezatullah", "index": 2},
            {"name": "Arkadev, Sergei", "index": 3},
            {"name": "Astasov, Ilja", "index": 4},
            {"name": "Bakulin, Efim", "index": 6},
            {"name": "Bindernagel, Dennis Erich", "index": 9},
            {"name": "Bischoff, Mandy", "index": 10},
            {"name": "Gellert, Daniel", "index": 17},
            {"name": "Hryhorieva, Iryna", "index": 23},
            {"name": "Konitzko, Vanessa Nadine", "index": 29},
            {"name": "Kortzer, Miriam Jasmina", "index": 32},
            {"name": "Lukashchuk, Viacheslav", "index": 37},
            {"name": "Murtaj, Lennart", "index": 40},
            {"name": "Neagus, Natalia", "index": 41},
            {"name": "Popovicenco, Vladislav", "index": 47},
            {"name": "Rinas, Erika", "index": 50},
            {"name": "Turaeva, Nargis Niyozmahmadovna", "index": 60},
        ]

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
        for _ in range(4):
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
            EC.element_to_be_clickable((By.XPATH, '//*[@id="scheduling-panel-form:j_idt55_3"]'))
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

    @staticmethod
    def choose_person(driver: webdriver.Edge, person_index):
        logging.info(f"Selecting person with index {person_index}")
        person_dropdown = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt196:j_idt245"]'))
        )
        person_dropdown.click()
        time.sleep(1)
        person_option = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="j_idt196:j_idt245_{person_index}"]'))
        )
        person_option.click()

    def create_termin(self, driver: webdriver.Edge, place: str, person: str):
        logging.info("Creating termin")
        create_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt196:j_idt275"]'))
        )
        create_button.click()
        logging.info("Termin created successfully")
        
        self.play_sound_for_duration(self._sound_file, 2)
        logging.info(f"Termin created at {place} for {person}")

    @staticmethod
    def play_sound_for_duration(sound_file: str, duration: int):
        """Play sound for a specific duration in seconds."""
        def play_sound():
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
        time.sleep(duration)
        
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

            for person in self.people_queue:
                slots = self.select_termin(driver)
                if not slots:
                    logging.info("No slots available. Ending process.")
                    return 
                
                slots[0].click()
                self.choose_person(driver, person['index'])
                self.create_termin(driver, place="Berlin", person=person['name'])
                # Переходимо до наступного учасника
                logging.info(f"Moving to next person in queue.")

if __name__ == "__main__":
    bot = BerlinBot()
    bot.perform_login()
