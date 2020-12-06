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

	result = html('Not found', 404)
	path = config['assetpath'] + (config['paths']['index'] if path == '/' else path)
	
	type = [ type for (ext, type) in config['types'].items() if path.endswith(ext) ]

	if isfile(path):
		with open(path) as file:
			result = html(file.read(), type[0])

	return result


def json(content: dict, status: int = 200):
	return { 'statusCode': status, 'body': jsonify(content) }


def html(content: str, type: str, status: int = 200):
	return {
		'statusCode': status,
		'body': content,
		'headers': { 'Content-Type': type, 'Cache-Control': 'max-age=864000' }
	}
