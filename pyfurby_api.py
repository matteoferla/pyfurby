import requests

class RemoteFurby:
    """
    Interact with a furby running in "restful mode".
    i.e. this script is run on a laptop and commands excecuted on Furby with same network.

    >>> furby = RemoteFurby('192.168.1.10')
    >>> furby.say(text='hello world')
    >>> furby.help() # return the list of commands

    """
    def __init__(self, ip:str, port:int=1998):
        self.ip=ip
        self.port=port

    def help(self):
        return requests.get(f'{self.url}/').text

    @property
    def url(self):
        return f'{self.url}:{self.port}'

    def __getattr__(self, cmd):
        def command(**params):
            return requests.get(f'{self.url}/{cmd}', params=params).json()
        return command
