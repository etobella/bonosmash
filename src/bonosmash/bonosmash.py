from bonobo.nodes.io.base import Writer
from bonobo.constants import NOT_MODIFIED
from bonobo.config.configurables import Configurable
from bonobo.config import Option, use_context
from collections import OrderedDict
import requests
import json
import logging

_logger = logging.getLogger(__name__)


@use_context
class Smashing(Configurable, Writer):

    server = Option(default='http://localhost:3030')
    token = Option(type=str, required=True)
    widget = Option(type=str, required=True)
    fields = Option(type=list, required=True)

    def send(self, context, *values):
        fields = context.get_input_fields()
        vals = OrderedDict(zip(fields, values))
        data = {'auth_token': self.token}
        for field in self.fields:
            field_name = field
            field_data = field
            if isinstance(field, tuple):
                field_name = field[0]
                field_data = field[1]
            data[field_data] = vals[field_name]
        url = "%s/widgets/%s" % (self.server, self.widget)
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            url, data=json.dumps(data), headers=headers
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            _logger.warn(response.status_code)
        return NOT_MODIFIED

    __call__ = send
