from telethon import TelegramClient
import configparser
config = configparser.ConfigParser()
config.read('credential.config')

api_id = config['TELEGRAM']['ApiId']
api_hash= config['TELEGRAM']['ApiHash']

client = TelegramClient('maaxowBot', api_id, api_hash)

async def main():
	await client.send_message('+33601020304, 'Test message.')


with client:
	client.loop.run_until_complete(main())
