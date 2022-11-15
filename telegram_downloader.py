"""Telegram Downloader"""

import asyncio
from re import sub,search
from os import system,name
from pyrogram import Client
import logging
from rich.logging import RichHandler
from argparse import (
	ArgumentParser,BooleanOptionalAction
)
from os.path import (
dirname,join,abspath,isdir,exists
)

def _is_exist(file_path: str) -> bool:
	return not isdir(file_path) and exists(file_path)

def get_name(i,msg_type,mime):
	z=mime.find('/')
	ext=mime[z:].replace('/','.')
	savef=f'[{i}] {msg_type}{ext}'
	return savef

async def func(id,client):
	msg= await client.get_messages(ch_id, id)
	msg_media=str(msg.media)
	msg_type=msg_media.replace('MessageMediaType.','').lower()
	i=ids_to_try.index(msg.id)

	if msg_type == 'photo':savef=f'[{i}] {msg_type}.jpg'
	elif msg_type == 'voice':savef=get_name(i,'voice',msg.voice.mime_type)
	elif msg_type == 'video_note':savef=get_name(i,'video_note',msg.video_note.mime_type)
	else:savef=f'[{i}] '+ search(r'"file_name": "(.*)"',str(msg))[1]
	THIS_DIR = dirname(abspath(__file__))
	file_path=join(THIS_DIR,'downloads',CHAT_TITLE,msg_type,savef)

	if _is_exist(file_path):
		logger.warning("[%s] Message - Media file already downloaded", msg.id)
		skipped_ids.append(msg.id)
	else:
		download_path=await client.download_media(msg,file_name=file_path)
		logger.info("Media downloaded - %s", download_path)

def bytesto(bytes,u):
	units={
		'kiB':10,'MiB':20,
		'GiB':30,'TiB':40
	}
	size=bytes / (2 ** units[u])
	size='{:.2f}'.format(size)
	return f'{size} {u}'

def separate_groups(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

async def main():
	client=Client('user')
	async with client:
		for subgp in groups:
			await asyncio.gather(
				*[func(id,client)for id in subgp]
			)
	logger.info(
		"%d files downloaded",len(ids_to_try)-
		len(skipped_ids)
	)

def get_chat_id(client,chat_title):
	dialogs = client.get_dialogs()
	for dialog in dialogs:
		name=f"{dialog.chat.first_name} {dialog.chat.last_name}"
		if chat_title == dialog.chat.title or chat_title in name:
			ch_id=dialog.chat.id
	return ch_id

def get_file_size(message):
	fsize=search(r'"file_size": (.*)',str(message))[1].strip(',')
	return int(fsize)

def filter_messages(messages,kind):
	list=[]
	total_size=[]
	kind=kind.split(",") if kind\
	is not None else None
	for message in messages:
		if message.media:
			if kind is not None:
				msg_media=str(message.media)
				msg_type=msg_media.replace('MessageMediaType.','').lower()
				if msg_type in kind:
					total_size.append(get_file_size(message))
					list.append(message.id)
			else:
				total_size.append(get_file_size(message))
				list.append(message.id)	
	return list,total_size

def connect_to_api():
	client=Client(
		'user',
		options.api_id,
		options.api_hash
	)
	with client:
		client.send_message(
			'me',"Message sent with **Telegram Downloader**!"
		)

system('clear || cls')
parser = ArgumentParser()
parser.add_argument("-o","--orig",help="origin chat title")
parser.add_argument('-w','--workers', type=int,default=5,help="max number of simultaneos downloads")
parser.add_argument("-f","--filter",type=str,default=None,help="filter messages by kind")
parser.add_argument("-q","--query",type=str,default=None,help="filter messages contais string query")
parser.add_argument("-a","--ask", action=BooleanOptionalAction,help="show total size and ask for download")
parser.add_argument('-i','--api-id',type=int,help="Your api id")
parser.add_argument('-s','--api-hash',type=str,help="Your api hash")
options = parser.parse_args()

if name == 'nt':
	CHAT_TITLE=sub(r'[\W_]+', '_',options.orig)
	asyncio.set_event_loop_policy(
		asyncio.WindowsSelectorEventLoopPolicy()
	)
else:
	CHAT_TITLE=options.orig

if options.api_id is not None:
	connect_to_api()
	exit()

ids_to_try=[]
skipped_ids=[]

logging.basicConfig(
level=logging.INFO,
format="%(message)s",
datefmt="[%X]",
handlers=[RichHandler(),
logging.FileHandler(
'events.log',"w", "utf-8"
)])
logger = logging.getLogger()

try:
	app=Client('user',takeout=True)
	with app:
		ch_id=get_chat_id(app,options.orig)
		if options.query is None:
			messages=app.get_chat_history(ch_id)
		else:
			messages=app.search_messages(ch_id,options.query)
		ids_to_try,total_size=filter_messages(messages,options.filter)
	ids_to_try.sort()
	workers=options.workers if\
	options.workers < 10 else 10
	groups = list(separate_groups(ids_to_try, workers))
except ValueError:
	logger.error('No chat found. Be sure you typed the title\n'+
	'correctly and you participate in.')
	exit()
except AttributeError:
	logger.error('No session was found\n')
	exit()
	
if options.ask:
	info=bytesto(sum(total_size),'GiB')
	inp=input(
		f'\nTotal size of files to download: {info}. '+
		'Do you wish to continue? Y/n: '
	)
	if inp == 'n':
		exit()

if __name__=='__main__':
	asyncio.run(main())