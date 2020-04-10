from api import req
from time import sleep
from helpers import prttime
while True:
    sleep(1)
    
    data = req('subscription_service');
    if data:
        print(prttime() + data['message'])
    else:
        print(prttime() + " No accounts found")
    