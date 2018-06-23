from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from random import randint
from ..models import Quote

import uuid

@view_config(route_name='quotes_list',  renderer='json')
def quotes_list(request):
    try:

        register_request(request)
        query = request.dbsession.query(Quote)
        quotes = query.all()

        list_quote = []

        for quote in quotes:

            list_quote.append(quote.quote)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return  {'quotes':  list_quote}


@view_config(route_name='quote_detail',  renderer='json')
def quotes_detail(request):
    try:
        pk = request.matchdict['pk']
        query = request.dbsession.query(Quote)

        if pk == 'random':
            count_quotes = query.count()
            random_number = randint(1, count_quotes)
            quote = query.get(random_number)
            return {'pk': random_number, 'quote': quote.quote}

        quote = query.get(pk)

        if quote is None:
            return Response("Bad request!The parameter 'pk' is invalid.", content_type='text/plain', status=400)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'quote':  quote.quote}


def register_request(request):

    session = request.session

    if 'userid' in session:
        print(session['userid'])
    else:
        create_userid(session)

def create_userid(session):

    userid = str(uuid.uuid4())

    session['userid'] = userid

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_geru_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
