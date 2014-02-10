import pkg_resources
import logging

# Setting up a do-nothing handler. We expect the application to define
# the handler for `scieloapi`.
logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = pkg_resources.get_distribution('scieloapi').version
__user_agent__ = 'scieloapi/%s' % __version__

from .core import Connector, Endpoint, Client

