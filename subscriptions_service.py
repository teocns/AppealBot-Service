from api import req
from time import sleep
from helpers import prttime
while True:
    sleep(1)
    print(prttime())
    req('subscription_service');
    