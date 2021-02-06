import threading
from typing import *

class BackFurby:

    def background(self, command: Union[str, Callable], *args, **kwargs):
        """
        Run a command in the background.
        It is a fake-overloaded function where command is either a str (name of method to be called)
        or a method to be called.

        >>> furby.background('ambulance', 10)

        or

        >>> furby.background(furby.ambulance, 10)

        :param command: method
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(command, str):
            command = getattr(self, command)
        thread = threading.Thread(target=command, args=args, kwargs=kwargs).start()
        return thread
