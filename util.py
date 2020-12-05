from email import message_from_bytes as parsemail
from glob import glob as glob
from imaplib import IMAP4 as imap
from json import load as loadjson

def getConfig(names = 'config/*.json'):
	result = {}
	for name in glob(names):
		with open(name) as file:
			result = merge(result, loadjson(file))
	return result

def getMails(config: dict):
	M = imap(config['host'])
	M.starttls()
	M.login(config['user'], config['pass'])
	M.select()

	typ, data = M.search(None, 'ALL')

	result = []

	for num in data[0].split():
		typ, data = M.fetch(num, 'RFC822')
		eml = parsemail(data[0][1])
		msg = None
		
		for part in eml.walk():
			if part.get_content_type().startswith('text/'):
				msg = part.get_payload(decode = True).decode(part.get_content_charset())
	
		result += [ {'to': eml['to'], 'subject': eml['subject'], 'body': msg } ]
	
	M.close()
	M.logout()
	
	return result

def merge(a: dict, b: dict):
	return {**a, **b}