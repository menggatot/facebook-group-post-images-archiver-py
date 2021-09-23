## Facebook Group Post Image Archiver
This project's purpose is to archive every single image of a single profile in the FB group.
### dependency :
 - python 3.8+
 - selenium
 - pickle
 - webdriver chrome
 - urllib
 - time
 - re
## The Preparation
**> How to get the url in line 25**<br/>
It has to be the mobile version of FB ex: `m.facebook.com`<br/>
To get the URL, you need to press their profile when you're on the group page while you're in the mobile version of Facebook<br/>
What does the URL look like? And please don't use this. this is just an example `https://m.facebook.com/firstname.lastname?groupid=2187593695444431&ref=content_filter`<br/>
after you get the url now you can paste it in `driver.get()` example: 
```python
# please do not use this, this is just an example
driver.get('https://m.facebook.com/firstname.lastname?groupid=2187593695444431&ref=content_filter)
```
**> How to generate cookies.pkl to login to Facebook automatically**<br/>
Run `python ./CreateCookies.py` Insert your email and password, press login, and then ok.
After the window close, look at your directory. There should be a file named `cookies.pkl`

## How to run the script
Make sure your `cookies.pkl` is at the same directory as `FBScrapper.py` then run it as usual.
```python
python ./FBScrapper.py
```
