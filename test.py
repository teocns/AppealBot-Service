import requests
from api import req
import time


email = b"Salve,\n\nTi ringraziamo per averci contattato. Prima di poterti fornire assistenza, dobbiamo verificare che tu sia il titolare dell'account. \n\nTi preghiamo di rispondere a questa e-mail allegando una tua foto in cui reggi il codice scritto a mano riportato di seguito.\n\n80867\n\nAssicurati che la foto che invii:\n\n- mostri il codice sopra riportato scritto su un foglio di carta e seguito dal tuo nome completo e dal tuo nome utente;\n- mostri le tue mani che reggono il foglio e il tuo viso per intero;\n- sia ben illuminata, non sia troppo piccola, scura o sfocata;\n- sia allegata alla tua risposta come file JPEG.\n\nTieni presente che anche se questo account non comprende foto tue o viene usato per rappresentare qualcun altro o qualcos'altro, non potremo fornirti assistenza finch\xc3\xa9 non riceviamo una foto che soddisfi questi requisiti.\n\nGrazie,\nIl team di Instagram\n\n"

current_email_data = {
    'appeal_process_id':  123,
    'time_fetched': int(time.time()),
    'time_received':int(time.time()) + 132994949,
    'body': str(email),
    'status': 'CODE_RECEIVED',
    'message_id': '<e1521839071e3154dec0cd153f3353c1@2d4a6334d2f2bb73c1c106ccaf5b5e83c5a47abe274260dadc6a33286199d452>',
    'from': str('Facebook <instagram++aazqggbkbltwbj@support.facebook.com>'),
    'code': '80867',
    'subject': str('My Instagram Account Was Deactivated'),
    'email_id':3088
}

result = req('register_email_received',data = current_email_data)
print (str(result['message']))