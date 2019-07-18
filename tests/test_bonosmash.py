from bonosmash import Smashing
import bonobo
from bonobo.nodes import SetFields
from bonobo.structs.graphs import Graph
import unittest
from mock import patch
import ast


def read():
    yield (1, 2)


class Response:
    def raise_for_status(self):
        pass


class TestBonosmash(unittest.TestCase):
    def test_bonosmash(self):
        graph = Graph()
        token = 'TOKKKENNNN'
        widget = 'bomosmash_test_widget'
        url = 'http://localhost:3030'
        graph.add_chain(read, SetFields(fields=('current', 'lst')), Smashing(
            server=url,
            token=token,
            widget=widget,
            fields=['current', ('lst', 'last')]
        ))
        with patch('requests.post') as mk:
            mk.return_value = Response()
            bonobo.run(graph)
            mk.assert_called()
            args = mk.call_args_list[0]
        data = ast.literal_eval(args[1].get('data'))
        self.assertEqual(data.get('current'), 1)
        self.assertEqual(data.get('last'), 2)
        self.assertEqual(data.get('auth_token'), token)
        self.assertEqual(args[0][0], '%s/widgets/%s' % (url, widget))
