# Booking bot for UB @UZH

If you are not familiar with scheduled tasks and programming in general. Feel free to ask me, I can give you detailed information or help you to install.
~nilsjosef.jacobi@uzh.ch

If you like my work [buy my a coffee - paypal](https://www.paypal.me/nilsCSJ)


### Functionality
This is a bot that books a seat in a UB library for a given place, library and time (as defined in the moment of execution via cronjob).
### requirements
- Selenium: current pip version
- Chromedriver: 135.* or newer
- Chrome: 135.* or newer
- Python: 3.9 or newer

### Installation
[**Selenium**](https://www.selenium.dev)

<code>pip install selenium</code>

<code>pip install webdriver-manager</code>

*The following is only here for legacy reasons. This step became obsolete in the newest patch. Skip to the chrome installation.*
[**Chromedriver**](https://chromedriver.chromium.org) 

For MacOS (ARM Architecture)

<code>curl https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/mac-arm64/chromedriver-mac-arm64.zip </code>

[Select a version](https://googlechromelabs.github.io/chrome-for-testing/)

*Continue here*

Chrome from the official [site](https://www.google.de/chrome/?brand=YTUH&gclid=CjwKCAiApaarBhB7EiwAYiMwqlRnbnsNuUgGB8O6Gyj_0hDLWbuQS99gUTPqzgT0d_u82THF9M0rNBoCnEEQAvD_BwE&gclsrc=aw.ds)

[Python](https://www.python.org) 3.9 or newer

### Note
For this code to run on a schedule, components must be configured to run in "headless" mode.
That means it should run without a GUI. If you encounter errors this is a reoccuring problem.

### Implementation

**Setup variables**
Example:
```
__pwd__ = Password
__mail__ = name@uzh.ch
```
Read the comments in the code for further variables that need to be set.

### Setting up a Cronjob

```
crontab -e
```

On the end of the file add the following code:
```
0 6 * * * sh /path/to/ubbookedbot/main.sh >> /path/to/ubbookedbot/UB-Cron-Log.txt 2>&1
```

This will make the main.sh code run every day at 6:00 am. For security and implementation reasons I created a main.sh file that can run the main.py file using the following command:
```
python3 /path/to/ubbookedbot/main.py
```


DO NOT SAVE THE main.sh IN THE HOME DIRECTORY. The home directory is encrypted as soon as you logout of your machine.


TODO: Installation script. Coming soon...