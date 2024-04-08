# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

# Login data
# __pwd__: Password
# __main__: uzh mail
__pwd__ = "PWD"
__mail__ = "name.surname@uzh.ch"
# List of seats that should be tried
__plaetze__ = ["preferred seat", "alternative seat"]
# The faculty you are part of
__fakultaet__ = "Faculty"
# A logging file that makes life easier for you
__log__ = "UB-Logs.txt"

# [Settings for development]
# Do not touch if not developing
__DEV__ = False

if __DEV__:
    headless = input("headless? y/n")
    if headless == "y":
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    elif headless == "n":
        driver = webdriver.Chrome()
    else:
        raise Warning("Invalid value for headless")
else:
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
# [/Settings for development]

# Reservation Time:
reservation_time = datetime.now() + timedelta(days=7)

# Building the URL
# IMPORTANT: YEAR IS HARD CODED! INCOMMING BUG
__URL__ = f"https://hbzwwws005.uzh.ch/booked-ubzh/Web/schedule.php?&clearFilter=1&sid=21&sd=2024-{reservation_time.month}-{reservation_time.day}"
# UB-nw: sid=21

log = open(__log__, "a")

while True:
    if len(__plaetze__) == 0:
        log = open(__log__, "a")
        log.write(datetime.now().strftime("%H:%M:%S") + f": failed, Alle plätze getestet, for {__mail__} day: " + str(reservation_time.day) + ". \n")
        break

    driver.get(__URL__)

    # Login
    # + Keys.ENTER
    try:
        driver.find_element(By.ID, "email").send_keys(__mail__)
        driver.find_element(By.ID, "password").send_keys(__pwd__ + Keys.ENTER)
    except:
        pass
    finally:
        # Find a seat && open page of seat
        driver.find_element(By.LINK_TEXT, __plaetze__[0]).send_keys(Keys.ENTER)

    # select end time of reservation
    select_time = driver.find_element(By.NAME, "endPeriod")
    selectEnd = Select(select_time)
    selectEnd.select_by_value("18:00:00")

    # buffer
    time.sleep(2)
    # select Faculty
    select_faculty = driver.find_element(By.ID, "psiattribute5")
    selectFaculty = Select(select_faculty)
    selectFaculty.select_by_value("WWF")

    # accept Nutzerbedingung
    terms_conditions = driver.find_element(By.ID, 'termsAndConditionsAcknowledgement')
    ActionChains(driver)\
            .click(terms_conditions)\
            .perform()

    # buffer
    time.sleep(2)

    # click Anlegen button
    anlegen = driver.find_element(By.CLASS_NAME, 'btn-success')
    ActionChains(driver)\
            .click(anlegen)\
            .perform()

    # buffer
    time.sleep(2)

    n = datetime.now()
    ts = n.strftime("%H:%M:%S")

    time.sleep(2)
    # Logging
    try:
        if(driver.find_element(By.ID, 'reservation-created')):
            log.write(ts + f": success -> booked... {__plaetze__[0]}, for {__mail__} at " + str(reservation_time.day) + ". \n")
            break
    except:
        log.write(ts + f": failed, {__plaetze__[0]}, for {__mail__} at " + str(reservation_time.day) + ". \n")
        __plaetze__ = __plaetze__[1::]

# close everything and exit code
log.close()
driver.quit()
