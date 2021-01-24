# SpeechRecognition

class ToldFurby:

    def _resolve_command(self, cmd, *args, **kwargs):
        getattr(self, cmd)(*args, **kwargs)

    def fill_keywords(self):
        self.keywords = {'hello': lambda decree: self.say("Hello"),
                         'execute': self.excute,
                         'pretty': lambda decree: self.flutter(),
                         'your name': lambda decree: self.say("My name is Furby")
                         }

    def be_told(self):
        # listen speech to text.
        # ????
        decree = '????'
        for keyword, action in self.keywords.items:
            if all([word in decree for word in keyword.split()]):
                action(decree)

    def excute(self, degree):
        commands = degree.split('execute')[1].strip().split()
        # ...
