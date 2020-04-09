import requests
import json

REQUEST_ENDPOINT = "http://localhost/api/backend.php"

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
        log(f'[REQUEST] Failed to send respones with action {action}. Respone={res.text}')
        return
    try:
        return json.loads(res.text)
    except:
        log(f'[PARSE REQ JSON] Failed loading JSON response ({res.text})')
        
def log(text):
    with open('log.txt','a') as file:
        file.write(text)