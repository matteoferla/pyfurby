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
    furby = None

    def __init__(self, attribute_name, value):
        assert attribute_name in ('volume', 'rate', 'speed', 'red', 'green')
        self.attribute_name = attribute_name
        self.temporary = value
        self.original = self.get()

    def get(self):
        if self.attribute_name == 'volume':
            return self.furby.volume
        elif self.attribute_name == 'rate':
            return self.furby.rate
        elif self.attribute_name == 'speed':
            return self.furby.percent_speed
        elif self.attribute_name == 'red':
            return self.furby.red_pin.value
        elif self.attribute_name == 'green':
            return self.furby.green_pin.value
        else:
            raise ValueError(f'Unknown attribute name {self.attribute_name}')

    def set(self, value):
        if self.attribute_name == 'volume':
            self.furby.volume = value
        elif self.attribute_name == 'rate':
            self.furby.rate = value
        elif self.attribute_name == 'speed':
            self.furby.percent_speed = value
        elif self.attribute_name == 'red':
            self.furby.red_pin.value = value
        elif self.attribute_name == 'green':
            self.furby.green_pin.value = value
        else:
            raise ValueError(f'Unknown attribute name {self.attribute_name}')

    def __enter__(self):
        self.set(self.temporary)

    def __exit__(self, *args):
        self.set(self.original)
