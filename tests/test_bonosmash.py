from bonosmash import Smashing
import bonobo
from bonobo.nodes import SetFields
from bonobo.structs.graphs import Graph
import unittest
from mock import patch


def read():
    yield (1, 2)


class Response:
    def raise_for_status(self):
        pass


class TestBonosmash(unittest.TestCase):
    def test_bonosmash(self):
        graph = Graph()
        graph.add_chain(read, SetFields(fields=('current', 'last')), Smashing(
            server='test',
            token='token',
            widget='widget',
            fields=['current', 'last']
        ))
        with patch('requests.post') as mk:
            mk.return_value = Response()
            bonobo.run(graph)
            mk.assert_called()
