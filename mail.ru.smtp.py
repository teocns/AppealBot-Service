import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pprint,time

import pymysql.cursors

db = pymysql.connect(host="alpha.mobileproxy.network", user="root", passwd="uryeGjjq2Zfjumywdhygnxnnmqv!dpkyft5jc{gxaumsp]Yepszasnwejy4yq>xgkbwabvskceyasaxymnjbDyxumedtvMw@jswx", db="recap", use_unicode=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
db.autocommit(True)
db.ping(True)
cur = db.cursor()

def sendMail(email,username,password,receiver,filepath=None):

	email_sender = email
	email_receiver = receiver
	 
	subject = 'RE: My Instagram Account Was Deactivated'
	 
	msg = MIMEMultipart()
	msg['From'] = email_sender
	# msg['To'] = email_receiver.replace('>','').replace('Facebook <','')
	msg['To'] = email_receiver
	# msg['Bcc'] = 'schokobecher@gmail.com'
	msg['Subject']= subject

	body = ''
	msg.attach(MIMEText(body, 'plain'))
	
	if filepath:
		filename = filepath
		attachment = open(filename, 'rb')	 
		part = MIMEBase('application', 'octet_stream')	 
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= "+filename)
		msg.attach(part)
 
	text = msg.as_string()
	 
	connection = smtplib.SMTP_SSL('smtp.mail.ru:465')

	# connection.starttls()
	connection.login(email_sender, password)
	connection.sendmail(email_sender, email_receiver, text )
	connection.quit()

while 1:
	
	db.ping(True)
	cur.execute("SELECT e.sender, e.file_path, e.id, r.username, r.password, r.email, e.relay_id, e.inbox FROM emails as e, relays as r WHERE e.file_path IS NOT NULL AND e.time_responded IS NULL AND e.relay_id = r.id AND (r.time_send_lock < %(time)s OR r.time_send_lock IS NULL) LIMIT 1", { 'time':int(time.time()) })
	# cur.execute("SELECT * FROM relays WHERE id = 1")
	if cur.rowcount > 0:
		row = cur.fetchone()
	else:
		continue
	
	print(row)
	
 	# sendMail(row['email'], row['username'], row['password'], 'saschazeman@gmail.com')
	sendMail(row['email'], row['username'], row['password'], row['sender'], row['file_path'])
	# sendMail('RuhaniiaZaleskaya@bk.ru', 'RuhaniiaZaleskaya@bk.ru', 'EZtTz8K7Tc', 'saschazeman@gmail.com', row['file_path'])

	cur.execute("UPDATE relays SET time_send_lock = %(time)s WHERE id = %(relay)s", { 'time':int(time.time())+(60*60*24), 'relay':row['relay_id'] })
	cur.execute("UPDATE emails SET time_responded = %(time)s WHERE inbox = %(inbox)s", { 'time':int(time.time()), 'inbox':row['inbox'] })

	print("150 seconds break")
	time.sleep(150)

