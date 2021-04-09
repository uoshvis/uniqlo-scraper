# uniqlo-scraper

Uses
* mongoDB
* scrapy
* scrapy-splash
* selenium

**MongoDB setup**

Ensure that there is an existing /data/bin folder in your $PWD
```
docker pull mongo
docker run -p 27017:27017 -d --mount type=bind,source=$PWD/data/bin,destination=/data/bin mongo
```
You can use MongoDB Compass to view the data in MongoDb.

**Scrapy-Splash setup**

```buildoutcfg
pip3 install scrapy-splash
docker pull scrapinghub/splash
docker run -p 8050:8050 -d scrapinghub/splash
```

Check out required scrapy-splash configuration: 

https://github.com/scrapy-plugins/scrapy-splash 

**Selenium setup**

To use selenium you need to specify the path where
your chromedriver is located.

More information on this can be found in this stackoverflow:

https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver

In short:

1. [Download chromedriver for your desired platform from here.](https://sites.google.com/a/chromium.org/chromedriver/downloads)
2. unzip chromedriver_linux64.zip
3. Place **chromedriver** file in the main project directory