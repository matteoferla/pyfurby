from typing import get_type_hints
import pydoc
import inspect


class RestlessFurby: # restful...

    def _resolve_request(self, cmd):
        """
        Restful API Mode.
        This action is trigged when any route that is not home is requested

        :param cmd:
        :return:
        """
        try:
            from flask import Flask, request
            if cmd.startswith('_') or not callable(inspect.getattr_static(self, cmd)):
                raise ValueError("Only public methods can be called")
            action = getattr(self, cmd)
            parameters = inspect.signature(action).parameters
            hints = get_type_hints(action)
            kwargs = {}
            for name, value in request.args.items():
                parameter = parameters[name]
                expected = hints.get(name)
                if expected is None and parameter.default is not inspect.Parameter.empty:
                    expected = type(parameter.default)
                if expected is bool:
                    if value.lower() not in ('true', 'false', '1', '0'):
                        raise ValueError("Boolean arguments must be true or false")
                    value = value.lower() in ('true', '1')
                elif expected in (int, float):
                    value = expected(value)
                kwargs[name] = value
            action(**kwargs)
            return {'status': 'OK'}
        except Exception as error:
            return {'status': 'error',
                    'error': f'{error.__class__.__name__}: {error}'}


    def _home(self):
        """
        Restful API Mode.
        This action is trigged when home is requested.
        """
        reply = '## Furby Restful API options\n\n'
        reply += 'To trigger a command, say `furby.yell`, use 198.162.1/0.xx:1998/yell?text=I%20hate%20you ' +\
                 'where xx is the furby\'s netword address\n'
        reply += 'Namely, the route (part before the question mark) is the command, and its arguments are ' +\
                  'key=value separated by an ampersand (that is a URL query).\n' +\
                  'Using Pythod requests, just submit it as a dictionary\n'
        for k in [k for k in dir(self) if not k.startswith('_')]:
            # Inspect without evaluating properties that read disconnected sensors.
            if not callable(inspect.getattr_static(self, k)):
                continue
            attribute = getattr(self, k)
            reply += f'###{k}\n>{inspect.signature(attribute)}\n{pydoc.getdoc(attribute)}\n\n'
        return reply

    def restful(self):
        """
        The furby listens on port 1998, the year the Furby was introduced (Nawww).
        Note that it is using Flask's internal app serving method, so is not suitable for use over the internet...
        :return:
        """
        from flask import Flask
        import waitress
        app = Flask(__name__)
        app.add_url_rule('/<cmd>', 'command', self._resolve_request)
        app.add_url_rule('/', 'home', self._home)
        waitress.serve(app, port=1998, host='0.0.0.0')
