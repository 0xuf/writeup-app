from os import (
    name, system
)
from sys import stdout
from random import choice
from time import sleep
from requests import post
from datetime import datetime


def cleanup():
    """
    This function will clean the command line
    """
    system("cls") if name == "nt" else system("clear")


def ascii_art():
    """
    This method will print ASCII art of writeup app
    """
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = r"""
$$\      $$\           $$\   $$\                                          $$$$$$\                      
$$ | $\  $$ |          \__|  $$ |                                        $$  __$$\                     
$$ |$$$\ $$ | $$$$$$\  $$\ $$$$$$\    $$$$$$\  $$\   $$\  $$$$$$\        $$ /  $$ | $$$$$$\   $$$$$$\  
$$ $$ $$\$$ |$$  __$$\ $$ |\_$$  _|  $$  __$$\ $$ |  $$ |$$  __$$\       $$$$$$$$ |$$  __$$\ $$  __$$\ 
$$$$  _$$$$ |$$ |  \__|$$ |  $$ |    $$$$$$$$ |$$ |  $$ |$$ /  $$ |      $$  __$$ |$$ /  $$ |$$ /  $$ |
$$$  / \$$$ |$$ |      $$ |  $$ |$$\ $$   ____|$$ |  $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |
$$  /   \$$ |$$ |      $$ |  \$$$$  |\$$$$$$$\ \$$$$$$  |$$$$$$$  |      $$ |  $$ |$$$$$$$  |$$$$$$$  |
\__/     \__|\__|      \__|   \____/  \_______| \______/ $$  ____/       \__|  \__|$$  ____/ $$  ____/ 
                                                         $$ |                      $$ |      $$ |      
                         github.com/0xuf                 $$ |                      $$ |      $$ |      
                              v1.0                       \__|                      \__|      \__|      
           """
    for N, line in enumerate(x.split("\n")):
        stdout.write("\x1b[1;%dm%s%s\n" % (choice(colors), line, clear))
        sleep(0.05)


def notify_script_launch(notify_webhook: str) -> bool:
    """
    This function will notify you when Script launched.
    :param notify_webhook: get webhook_url to send message
    :rtype: bool
    """
    data = dict(
        content=f"Writeup app launched at {datetime.now()}"
    )
    _resp = post(url=notify_webhook, json=data)
    if _resp.status_code == 204:
        return True

    return False


def notify_writeup(notify_webhook: str, data) -> bool:
    """
    This function will notify you when it finds a new write-up on the Discord server
    :param notify_webhook: get webhook_url to send message
    :param data: get writeup-data to post it on discord chat
    :rtype: bool
    """
    author = data.get("author")
    _post = data.get("post")
    parse_data = f"🟢 New WriteUp !\n\n" \
                 f"🖇 WriteUp Link: ||[{_post['title']}]({_post['link']})||\n\n" \
                 f"🧑‍💻 Writeup Author: ||[{author['name']}]({author['username']})||\n"
    data = dict(
        content=parse_data
    )
    _resp = post(url=notify_webhook, json=data)
    if _resp.status_code == 204:
        return True

    return False
