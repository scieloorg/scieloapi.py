try:
    from scieloapi import Connector, Endpoint, Client
except ImportError as e:
    if 'requests' in e.message:
        print 'requests is not present. please run python setup.py install'
    else:
        raise


__version__ = '0.3'

