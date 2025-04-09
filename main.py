# Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

# Login data
# __pwd__: Password
# __main__: uzh mail
__pwd__ = "PWD"
__mail__ = "name.surname@uzh.ch"
# List of seats that should be tried (i.e. [f"Y15/1{i}" for i in range(15, 27)])
__plaetze__ = ["preferred seat", "alternative seat"]
# The faculty you are part of (i.e. WWF, MNF )
__fakultaet__ = "Faculty"
# A logging file that makes life easier for you (Optional)
__log__ = "UB-Logs.txt"
# Start time of reservation
__startTime__ = "08:00:00"
# End time of reservation
__endTime__ = "17:00:00"

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

# Settings for development
__DEV__ = True

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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

# Reservation Time:
reservation_time = datetime.now() + timedelta(days=7)

log = open(__log__, "a")

# UB-nw: sid=21
while __repeat__:
    if len(__plaetze__) == 0:
        log = open(__log__, "a")
        log.write(datetime.now().strftime("%H:%M:%S") + f": failed, Alle plätze getestet, for {__mail__} day: " + str(reservation_time.day) + ". \n")
        break

    __URL__ = f"https://hbzwwws005.uzh.ch/booked-ubzh/Web/reservation.php?rid={__plaetze__[0]}&sid=21&rd=2025-{reservation_time.month}-{reservation_time.day}"

    driver.get(__URL__)

    # Login
    # name: id="email" pwd: id="password"
    # + Keys.ENTER
    try:
        driver.find_element(By.ID, "email").send_keys(__mail__)
        driver.find_element(By.ID, "password").send_keys(__pwd__ + Keys.ENTER)
    except:
        pass

    # select time
    select_time = driver.find_element(By.ID, "BeginPeriod")
    selectEnd = Select(select_time)
    selectEnd.select_by_value(__startTime__)

    select_time = driver.find_element(By.ID, "EndPeriod")
    selectEnd = Select(select_time)
    selectEnd.select_by_value(__endTime__)

    time.sleep(1)
    # select Faculty
    select_faculty = driver.find_element(By.ID, "psiattribute5")
    selectFaculty = Select(select_faculty)
    selectFaculty.select_by_value("WWF")

    # accept Nutzerbedingung
    terms_conditions = driver.find_element(By.ID, 'termsAndConditionsAcknowledgement')
    ActionChains(driver)\
            .click(terms_conditions)\
            .perform()

    # click Anlegen button
    anlegen = driver.find_element(By.CLASS_NAME, 'btn-success')
    ActionChains(driver)\
            .click(anlegen)\
            .perform()

    n = datetime.now()
    ts = n.strftime("%H:%M:%S")

    try:
        if(driver.find_element(By.ID, 'reservation-created')):
            log.write(ts + f": success -> booked... {__plaetze__[0]}, for {__mail__} at " + str(reservation_time.day) + "." + str(reservation_time.month) + ". \n")
            __repeat__ = False
    except:
        log.write(ts + f": failed, {__plaetze__[0]}, for {__mail__} at " + str(reservation_time.day) + "." + str(reservation_time.month) + ". \n")
        __plaetze__ = __plaetze__[1::]

driver.delete_all_cookies()
log.close()
driver.quit()
