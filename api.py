import requests
import json

REQUEST_ENDPOINT = "https://beta.appealbot.net/api/backend.php"

token = "kasdjhnkas89432ur8jfsakdlnxczvnjfdsahn"

def req(action,data = {}):
    
    postdata = {
        'action':action,
        'data':data,
        'token':token
    }
    
    try:
        res = requests.post(
            url=REQUEST_ENDPOINT,
            json= postdata
        )
        #print(res.text);
    except:
        print(f'Server didnt respond')
        return
    try:
        return json.loads(res.text)
    except:
        print(f'Server responded with non valid json')
        
def log(text):
    with open('log.txt','a') as file:
        file.write(text)