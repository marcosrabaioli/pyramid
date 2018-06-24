import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Quote


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        query = dbsession.query(Quote)
        count_quotes = query.count()

        if count_quotes == 0:

            quotes = [
                        "Beautiful is better than ugly.",
                        "Explicit is better than implicit.",
                        "Simple is better than complex.",
                        "Complex is better than complicated.",
                        "Flat is better than nested.",
                        "Sparse is better than dense.",
                        "Readability counts.",
                        "Special cases aren't special enough to break the rules.",
                        "Although practicality beats purity.",
                        "Errors should never pass silently.",
                        "Unless explicitly silenced.",
                        "In the face of ambiguity, refuse the temptation to guess.",
                        "There should be one-- and preferably only one --obvious way to do it.",
                        "Although that way may not be obvious at first unless you're Dutch.",
                        "Now is better than never.",
                        "Although never is often better than *right* now.",
                        "If the implementation is hard to explain, it's a bad idea.",
                        "If the implementation is easy to explain, it may be a good idea.",
                        "Namespaces are one honking great idea -- let's do more of those!"
                    ]
            for quote in quotes:

                model = Quote(quote=quote)
                dbsession.add(model)
