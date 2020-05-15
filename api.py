import requests
import json

REQUEST_ENDPOINT = "https://betaapi.appealbot.net/api/backend"

token = "sadsaX+asdsd09i0fs9dmk43jm1ki2432187uf8das778+fsjaifjdsjifsadjkidfa_nhasdfjnvzcxnldkasfj8ru23498saknhjdsak"

def req(action,data = {}):
    
    postdata = {
        'action':action,
        'data':data
    }
    
    try:
        res = requests.post(
            url=REQUEST_ENDPOINT,
            json= postdata,
            headers={
                "X-Token":token
            }
        )
        #print(res.text);
    except:
        print(f'Server didnt respond')
        return
    try:
        return json.loads(res.text)
    except:
        print(f'Server responded with non valid json: {res.text}')
        
def log(text):
    with open('log.txt','a') as file:
        file.write(text)