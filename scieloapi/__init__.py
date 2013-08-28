__version__ = '0.4'
__user_agent__ = 'scieloapi/%s' % __version__

try:
    from .core import Connector, Endpoint, Client
except ImportError as e:
    if 'requests' in e.message:
        print 'requests is not present. please run python setup.py install'
    else:
        raise

