from typing import Any

class TemporaryValue:
    """
    context manager for a temporary value.

    >>> TemporaryValue.furby = furby
    >>> with TemporaryValue('red', True):
    >>>      pass

    The furby bound ``use_temporarily`` knows furby

    >>> with furby.use_temporarily('red', True):
    >>>       pass
    """
    _furby = None

    def __init__(self, attribute_name: str, value: Any):
        assert attribute_name in ('volume', 'rate', 'speed', 'red', 'green')
        self.attribute_name = attribute_name
        self.temporary = value
        self.original = self.get()

    def get(self):
        if self.attribute_name == 'volume':
            return self._furby.volume  # this is not a typo
        elif self.attribute_name == 'rate':
            return self._furby.rate
        elif self.attribute_name == 'speed':
            return self._furby.percent_speed
        elif self.attribute_name == 'red':
            return self._furby.red_pin.value
        elif self.attribute_name == 'green':
            return self._furby.green_pin.value
        else:
            raise ValueError(f'Unknown attribute name {self.attribute_name}')

    def set(self, value):
        if self.attribute_name == 'volume':
            self._furby.volume = value
        elif self.attribute_name == 'rate':
            self._furby.rate = value
        elif self.attribute_name == 'speed':
            self._furby.percent_speed = value
        elif self.attribute_name == 'red':
            self._furby.red_pin.value = value
        elif self.attribute_name == 'green':
            self._furby.green_pin.value = value
        else:
            raise ValueError(f'Unknown attribute name {self.attribute_name}')

    def __enter__(self):
        self.set(self.temporary)

    def __exit__(self, *args):
        self.set(self.original)
