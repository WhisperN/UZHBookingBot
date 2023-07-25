# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
import time
import datetime

__pwd__ = "YourPWD"
__email__ = "YourEMAIL"
seat_name = "NameOfSeat"
faculty = "YourFaculty"

driver = webdriver.Chrome()

# Reservation Time:
curr = datetime.datetime.now()
month = curr.month

now_time = datetime.datetime.now().time()

# Date for next week
# Careful! Special case if +7 days is greater than max days of month not implemented

if datetime.time(20, 0) <= now_time <= datetime.time(23, 59, 59):
    day = curr.day + 8
elif datetime.time(0, 0) <= now_time <= datetime.time(7, 59, 59):
    day = curr.day + 7
else:
    day = curr.day + 7


__URL__ = "https://hbzwwws005.uzh.ch/booked-ubzh/Web/schedule.php?&clearFilter=1&sid=21&sd=2023-"+str(month)+"-"+str(day)
# UB-nw: sid=21
driver.get(__URL__)

# Login
# name: id="email" pwd: id="password"
# + Keys.ENTER
driver.find_element(By.ID, "email").send_keys(__email__)
driver.find_element(By.ID, "password").send_keys(__pwd__ + Keys.ENTER)

# Find a seat && open page of seat
driver.find_element(By.LINK_TEXT, seat_name).send_keys(Keys.ENTER)

# select time
select_time = driver.find_element(By.NAME, "endPeriod")
selectEnd = Select(select_time)
selectEnd.select_by_value("18:00:00")

# select Faculty
select_faculty = driver.find_element(By.NAME, "psiattribute[5]")
selectFaculty = Select(select_faculty)
selectFaculty.select_by_value(faculty)

# accept Nutzerbedingung
terms_conditions = driver.find_element(By.ID, 'termsAndConditionsAcknowledgement')
ActionChains(driver)\
        .click(terms_conditions)\
        .perform()

time.sleep(3)

# click Anlegen button
anlegen = driver.find_element(By.CLASS_NAME, 'btn-success')
ActionChains(driver)\
        .click(anlegen)\
        .perform()

# Log file
log = open("UB-Logs.txt", "a")
n = datetime.datetime.now()
ts = n.strftime("%H:%M:%S")

time.sleep(2)

if(driver.find_element(By.ID, 'reservation-failed')):
    log.write(ts + ": failed")
else:
    log.write(ts + ": success -> booked... 127")

log.close()

driver.quit()
