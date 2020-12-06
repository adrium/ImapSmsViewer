from base64 import b64encode as base64
from json import dumps as jsonify
from os.path import isfile as isfile
from util import getConfig, getMails


def lambda_handler(event, context):

	config = getConfig()
	path = event['path']

	if path.startswith(config['paths']['numbers']):
		return numbers(config, event)

	if path.startswith(config['paths']['messages']):
		return messages(config, event)

	return render(config, path)


def numbers(config, event):
	result = { name: number['info'] for (name, number) in config['numbers'].items() }

	return json(result)


def messages(config, event):

	number = event['pathParameters']['number']

	if number not in config['numbers']:
		return json({'error': 'Not found'}, 404)

	result = getMails(config['numbers'][number]['secrets'])

	result = [ {
		'from': msg['subject'].replace(config['smsprefix'], ''),
		'body': msg['body']
	} for msg in result ]

	result = result[:config['maxmessages']]
	result.reverse()

	return json(result)


def render(config, path):

	result = text('Not found', 'text/plain', 404)
	path = config['assetpath'] + (config['paths']['index'] if path == '/' else path)

	type = [ t for (ext, t) in config['types'].items() if path.endswith(ext) ][0]
	isbin = [ isbin for (t, isbin) in config['binary_types'].items() if type.startswith(t) ][0]

	if isfile(path):
		if isbin:
			with open(path, 'rb') as file:
				result = binary(file.read(), type)
		else:
			with open(path) as file:
				result = text(file.read(), type)

	return result


def json(content: dict, status: int = 200):
	return { 'statusCode': status, 'body': jsonify(content) }


def text(content: str, type: str, status: int = 200):
	return {
		'statusCode': status,
		'headers': { 'Content-Type': type, 'Cache-Control': 'max-age=86400' },
		'body': content,
	}


def binary(content: bytes, type: str):
	return {
		'statusCode': 200,
		'isBase64Encoded': True,
		'headers': { 'Content-Type': type, 'Cache-Control': 'max-age=86400' },
		'body': base64(content).decode("utf-8"),
	}
