from typing import get_type_hints
import pydoc


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
            kwargs = request.args
            print(f'Request {cmd}: {kwargs} from {request.remote_addr}')
            getattr(self, cmd)(**kwargs)
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
        for k in [k for k in dir(self) if k.find('_') != 0]:
            attribute = getattr(self, k)
            reply += f'###{k}\n>{get_type_hints(attribute)}\n{pydoc.getdoc(attribute)}\n\n'
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
