
import datetime
import json
import os
import time
from pathlib import Path

import pyperclip
import pytz
from selenium import webdriver
from selenium.webdriver.support.ui import Select


from . import parse


def read_config():
    path = Path(os.environ["HOME"]) / ".config" / "buffer-automation.json"
    if not path.exists():
        raise Exception(f"Create configation file in {path} with username and password files")

    with open(path, encoding="utf-8") as stream:
        return json.loads(stream.read())


class LoginPage:
    def login(self, driver, config):
        self.wait(driver)
        email = driver.find_element("id", "email")
        email.send_keys(config["username"])

        password = driver.find_element("id", "password")
        password.send_keys(config["password"])

        button = driver.find_element("xpath", "//*[text()='Log In']")
        button.click()
        return MainPage()

    @staticmethod
    def wait(driver):
        wait_for_element(driver, "//*[@id='email']")

def wait_for_element(driver, xpath, missing=False):
    start = time.time()
    while True:
        xpath = xpath.replace('"', '\\"')
        present = driver.execute_script(f"""return document.evaluate("{xpath}", document).iterateNext()""")
        if missing and not present:
            return

        if not missing and present:
            return

        time.sleep(0.5)
        if time.time() - start > 5:
            raise Exception('Timeout')

def wait_for_no_element(driver, xpath):
    return wait_for_element(driver, xpath, missing=True)

class MainPage:
    @staticmethod
    def open_post(driver):
        driver.execute_script("""
        document.evaluate("//nav//*[text()='New Post']//ancestor::button", document).iterateNext().click()
        """)
        return PostPage()

class PostPage:
    def __init__(self):
        self.filled = False

    def fill_post(self, driver, text):
        if self.filled:
            raise Exception('already filled')
        textbox = driver.find_element("xpath", "//*[@role='textbox']")
        textbox.send_keys(text)
        self.filled = True
        return self

    def add_thread_message(self, driver, text):
        if not self.filled:
            # Fill post first
            return self.fill_post(driver, text)

        driver.find_element("xpath", "//*[@data-testid='add-post-to-thread-button']").click()
        driver.find_element("xpath", "//*[@role='textbox']").send_keys(text)

        return self

    def add_image(self, driver, path: str):
        element = driver.find_element("xpath", "//*[@data-testid='uploads-dropzone-input']")
        element.send_keys(str(path))

        # wait for image to upload
        for _ in range(20):
            if driver.execute_script('''return document.evaluate("//*[starts-with(@class, ' publish_editorC')]/descendant::img", document).iterateNext()'''):
                break
            time.sleep(0.5)

        return self

    def open_schedule(self, driver):
        driver.find_element("xpath", "//*[@data-testid='stacked-save-buttons-section']//div[@role='button']").click()
        driver.find_element("xpath", "//*[text()='Schedule Post']").click()
        return SchedulePage(self)

class SchedulePage:
    def __init__(self, post_page):
        self.post_page = post_page

    def schedule(self, driver, dt):
        # Uses uk timezone
        tz = pytz.timezone('Europe/London')
        dt = dt.astimezone(tz)

        hour = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[1]")
        minutes = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[2]")
        half = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[3]")
        Select(half).select_by_value("am" if dt.hour < 12 else "pm")
        Select(hour).select_by_value(str((dt.hour - 1) % 12 + 1))
        Select(minutes).select_by_value(str(dt.minute))
        driver.find_element("xpath", f"//*[@class='DayPicker']/descendant::div[text()='{dt.day}']").click()
        driver.find_element("xpath", "//*[text()='Schedule']").click()
        self.wait_after(driver)
        return MainPage()

    def wait_after(self, driver):
        return wait_for_no_element(driver, "//*[@id='composer-root']")

def post_thread(driver, thread: dict) -> None:
    page = MainPage()
    page = page.open_post(driver)
    for message, images in zip(thread["messages"], thread["images"]):
        page = page.add_thread_message(driver, message)
        print("images", images)
        for image in images:
            page = page.add_image(driver, image)

    page = page.open_schedule(driver)
    page.schedule(driver, thread["timestamp"])


def post(driver, dt: datetime.datetime, message: str) -> MainPage:
    page = MainPage()
    page = page.open_post(driver)
    page = page.fill_post(driver, message)
    page = page.open_schedule(driver)
    page = page.schedule(driver, dt)
    return page

# Script to use
class Buffer:
    def __init__(self, image_path):
        self.driver = webdriver.Chrome()
        self.driver.get("https://publish.buffer.com")
        self.image_path = image_path

    def login(self):
        config = read_config()
        LoginPage().login(self.driver, config)

    def post_clipboard(self):
        "Read a string of the form TIMSTAMP tweet from the clipboard and post from it"
        data = pyperclip.paste()
        threads = parse.parse_threads(self.image_path, data)

        for thread in threads:
            post_thread(self.driver, thread)


# buffer.PostPage().add_thread_message("new message")
