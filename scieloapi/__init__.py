import pkg_resources


__version__ = pkg_resources.get_distribution('scieloapi').version
__user_agent__ = 'scieloapi/%s' % __version__

from .core import Connector, Endpoint, Client

