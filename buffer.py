
import datetime
import json
import os
from pathlib import Path

import pyperclip
import pytz
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def read_config():
    path = Path(os.environ["HOME"]) / ".config" / "buffer-automation.json"
    if not path.exists():
        raise Exception(f"Create configation file in {path} with username and password files")

    with open(path, encoding="utf-8") as stream:
        return json.loads(stream.read())


class LoginPage:
    @staticmethod
    def login(driver, config):
        email = driver.find_element("id", "email")
        email.send_keys(config["username"])

        password = driver.find_element("id", "password")
        password.send_keys(config["password"])

        button = driver.find_element("xpath", "//*[text()='Log In']")
        button.click()
        return MainPage()


class MainPage:
    @staticmethod
    def open_post(driver):
        post_button = driver.find_element("xpath", "//nav//*[text()='New Post']//ancestor::button")
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

    def open_schedule(self, driver):
        driver.find_element("xpath", "//*[@data-testid='stacked-save-buttons-section']//div[@role='button']").click()
        driver.find_element("xpath", "//*[text()='Schedule Post']").click()
        return SchedulePage(self)

class SchedulePage:
    def __init__(self, post_page):
        self.post_page = post_page

    def schedule(self, driver, dt):
        hour = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[1]")
        minutes = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[2]")
        half = driver.find_element("xpath", "//*[@data-testid='date-time-picker']//descendant::select[3]")
        Select(half).select_by_value("am" if dt.hour < 12 else "pm")
        Select(hour).select_by_value(str(dt.hour))
        Select(minutes).select_by_value(str(dt.minute))
        driver.find_element("xpath", f"//*[@class='DayPicker']/descendant::div[text()='{dt.day}']").click()
        driver.find_element("xpath", "//*[text()='Schedule']").click()
        return self.post_page


def post_string(driver, string: str):
    page = MainPage()
    date_string, message = string.split(" ", 1)
    dt = datetime.datetime.fromisoformat(date_string)
    post(driver, page, dt, message)


def post(driver, page: MainPage, dt: datetime.datetime, post: str) -> MainPage:
    tz = pytz.timezone('Europe/London')
    dt = dt.astimezone(tz)

    page = page.open_post(driver)
    page = page.fill_post(driver, post)
    page = page.open_schedule(driver)
    page = page.schedule(driver, dt)
    return page


# Script to use
class Buffer:
    def __init__(self, ):
        self.driver = webdriver.Chrome()
        self.driver.get("https://publish.buffer.com")

    def login(self):
        config = read_config()
        LoginPage.login(self.driver, config)

    def post_clipboard():
        "Read a string of the form TIMSTAMP tweet from the clipboard and post from it"
        string = pyperclip.paste()
        post_string(self.driver, string)
