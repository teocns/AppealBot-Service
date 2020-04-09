import asyncio, time
from pyppeteer import launch

def patch_pyppeteer():
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method
    
patch_pyppeteer()

async def main(name,account,email):
    browser = await launch({'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    await page.setViewport({'width': 1400, 'height': 1080})

    await page.goto('https://help.instagram.com/contact/1652567838289083')

    btnLanguage = await page.xpath('//a[contains(text(), "English (UK)")]')
    await btnLanguage[0].click()
    await page.waitForNavigation()

    btnAccountType = await page.xpath('//input[contains(@value, "Personal")]/../../label')
    await btnAccountType[1].click()

    formFields = await page.xpath('//form[contains(@rel, "async")]//input')
    # name
    await formFields[4].type(name)    

    # account
    await formFields[5].type(account)

    # email
    await formFields[6].type(email)

    # country
    await formFields[8].type('United', delay=100)
    await page.waitFor(1000)
    await formFields[8].press('Enter')
    await page.waitFor(1000)
    await formFields[8].press('Enter')
    await page.keyboard.press('Enter')
    
    try:
        await page.waitFor(10000)
        await page.waitForXPath('//div[contains(text(), "Instagram Account is active")]', timeout=10000)
        print('> instagram account is active')

        #await page.waitForXPath('//div[contains(text(), "something incorrectly")]', timeout=5)
        #print('> something went wrong found')
    except:
        pass

    try:
        await page.waitFor(10000)
        await page.waitForXPath('//p[contains(text(), "currently have any known issues to report")]', timeout=10000)
        print('> request sent successfully')

        print(page.url)

        if page.url == 'https://help.instagram.com/':
            print('> URL MATCH')
            
            # SUCCESS    
        
    except:
       pass    

    await page.screenshot({'path': 'C:/Users/sascha/Desktop/example.png','fullPage':True})
    time.sleep(5)
    await browser.close()

asyncio.get_event_loop().run_until_complete( main('Sascha Zeman','professional.adventure','dellrocks5@fastmail.com') )
