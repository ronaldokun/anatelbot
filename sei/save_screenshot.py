#!/usr/bin/python
from cStringIO import StringIO

from PIL import Image
from selenium import webdriver

verbose = 1

browser = webdriver.Firefox()
browser.get('http://stackoverflow.com/questions/37906704/taking-a-whole-page-screenshot-with-selenium-marionette-in-python')

# from here http://stackoverflow.com/questions/1145850/how-to-get-height-of-entire-document-with-javascript
js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

scrollheight = browser.execute_script(js)

if verbose > 0: 
    print(scrollheight)

slices = []
offset = 0
while offset < scrollheight:
    if verbose > 0: 
        print(offset)

    browser.execute_script("window.scrollTo(0, %s);" % offset)
    img = Image.open(StringIO(browser.get_screenshot_as_png()))
    offset += img.size[1]
    slices.append(img)

    if verbose > 0:
        browser.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
        print(scrollheight)


screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
offset = 0
for img in slices:
    screenshot.paste(img, (0, offset))
    offset += img.size[1]

screenshot.save(r'/files/boleto/test.png')
