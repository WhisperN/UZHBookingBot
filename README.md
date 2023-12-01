# Booking bot for UB @UZH

### Functionality
This is a bot that books a seat in a UB library for a given place, library and time (as defined in the moment of execution via cronjob).
### requirements
- Selenium: current pip version
- Chromedriver: 119.* or newer
- Chrome: 119.* or newer
- Python: 3.9 or newer

### Installation
[**Selenium**](https://www.selenium.dev)

<code>pip install selenium</code>

[**Chromedriver**](https://chromedriver.chromium.org) 

<code>curl https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/mac-arm64/chromedriver-mac-arm64.zip </code>

Chrome from the official [site](https://www.google.de/chrome/?brand=YTUH&gclid=CjwKCAiApaarBhB7EiwAYiMwqlRnbnsNuUgGB8O6Gyj_0hDLWbuQS99gUTPqzgT0d_u82THF9M0rNBoCnEEQAvD_BwE&gclsrc=aw.ds)

[Python](https://www.python.org) 3.9 or newer

### Implementation

**Setup variables**

```
__pwd__ = Password
__mail__ = name@uzh.ch
```

