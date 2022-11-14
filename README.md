# Telegram Downloader

> Download any media content from TG chats!

## First step

Before continue, be sure that you:

* install the latest version of [python](https://www.python.org/)
* have your api credentials: [api id](https://t.me/c/1297554030/69) and [api hash](https://t.me/c/1297554030/69)

## Install dependencies and start client

If you have already installed pyrogram, remove it:

```
pip uninstall pyrogram
```

Then, install the following python packages:

```
pip install tgcrypto rich https://github.com/Drrivao/pyrogram/archive/refs/heads/master.zip
```

Finally, connect to Telegram API:
```
python telegram_downloader.py -i 'YOUR API ID' -s 'YOUR API HASH'
```

## Basic usage

Download all media files from chat:
```
python telegram_downloader.py -o 'origin chat title' -w 'number of simultaneous process' -a y
```
> The default number of simultaneous process is 5 and the maximum is 10.

For more detail of available options run:
```
python telegram_downloader.py --help
```

## Telegram Downloader on colab

1. Open the [notebook](https://colab.research.google.com/github/Drrivao/Telegram-Downloader/blob/master/telegram_downloader.ipynb). 
2. To the first cell insert the path to a shared drive to save program files or ignore this step if you want to save them to your personal drive.
> Note: you'll need read/write permissions to the shared drive.
3. In the second cell edit the texts "YOUR API ID HERE" and "YOUR API HASH" adding your api id and api hash repectively.
4. In the third cell, change the text "ORIGIN CHAT TITLE" to the chat title contains the media files you want to downloade and set a value less than 10 in "WORKERS" to indicate the number of simultaneous download.
