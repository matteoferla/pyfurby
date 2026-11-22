import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

RestlessFurby = runpy.run_path(str(Path(__file__).parents[1] / 'pyfurby/restless.py'))['RestlessFurby']


class DummyFurby(RestlessFurby):
    def say(self, text, move: bool = True):
        self.called = (text, move)

    def flutter(self, cycles: int = 5):
        self.called = cycles

    @property
    def sensor(self):
        raise AssertionError('Must not read hardware for REST help or dispatch')


class RestApiTests(unittest.TestCase):
    def setUp(self):
        self.furby = DummyFurby()

    def dispatch(self, command, **args):
        flask = types.ModuleType('flask')
        flask.Flask = object
        flask.request = types.SimpleNamespace(args=args)
        with patch.dict(sys.modules, {'flask': flask}):
            return self.furby._resolve_request(command)

    def test_false_does_not_enable_motion(self):
        self.assertEqual(self.dispatch('say', text='Hello', move='false')['status'], 'OK')
        self.assertEqual(self.furby.called, ('Hello', False))

    def test_numeric_arguments(self):
        self.assertEqual(self.dispatch('flutter', cycles='3')['status'], 'OK')
        self.assertEqual(self.furby.called, 3)

    def test_invalid_boolean_does_not_call_motor(self):
        self.assertEqual(self.dispatch('say', text='Hello', move='maybe')['status'], 'error')
        self.assertFalse(hasattr(self.furby, 'called'))

    def test_private_methods_and_properties_are_rejected(self):
        for name in ('__init__', 'sensor'):
            self.assertEqual(self.dispatch(name)['status'], 'error')

    def test_help_does_not_evaluate_sensors(self):
        self.assertIn('say', self.furby._home())
