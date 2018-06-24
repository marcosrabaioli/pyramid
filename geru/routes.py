from pyramid_nacl_session import generate_secret
from pyramid_nacl_session import EncryptedCookieSessionFactory

SECRET = generate_secret(as_hex=False)

def includeme(config):

    factory = EncryptedCookieSessionFactory(SECRET, timeout=None)
    config.set_session_factory(factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('quotes_list', '/quotes')
    config.add_route('quote_detail', '/quote/{pk}')
    config.add_route('log_requests_list', '/requests')
    config.add_route('home', '/')
