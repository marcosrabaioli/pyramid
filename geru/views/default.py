from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from random import randint
from ..models import Quote
from ..models import RequestLog

from datetime import datetime

import uuid

from ..wrapper.quotes_wrapper import QuotesWrapper

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    register_request(request)
    return {"title": "Web Challenge 1.0"}


@view_config(route_name='quotes_list',  renderer='json', request_method="GET")
def quotes_list(request):
    try:
        wrapper = QuotesWrapper()
        status, data = wrapper.get_quotes()
        register_request(request)
        if status == 200:
            return data
    except DBAPIError:
        return Response('Internal server error!', content_type='text/plain', status=500)

    return Response(data['message'], content_type='text/plain', status=status)


@view_config(route_name='quote_detail',  renderer='json', request_method="GET")
def quotes_detail(request):
    try:
        register_request(request)
        pk = request.matchdict['pk']
        wrapper = QuotesWrapper()

        if pk == 'random':
            status, data = wrapper.get_quote_random()

            if status == 200:
                return data
            else:
                return Response(data['message'], content_type='text/plain', status=status)

        status, data = wrapper.get_quote(pk)

        if status == 200:
            return data
        else:
            return Response(data['message'], content_type='text/plain', status=status)

    except Exception:
        return Response('Internal server error!', content_type='text/plain', status=500)



@view_config(route_name='log_requests_list',  renderer='json', request_method="GET")
def log_requests_list(request):
    try:
        register_request(request)
        query = request.dbsession.query(RequestLog)
        logs = query.all()

        list_logs = []

        for log in logs:

            list_logs.append({'sessionId': log.session_id,
                              'request': log.request,
                              'timestamp': log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                              })

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'requests':  list_logs}


def register_request(request):

    session = request.session

    if 'userid' in session:
        log_request(request)
    else:
        create_userid(session)
        log_request(request)


def log_request(request):

    session_id = request.session['userid']

    url = request.path

    timestamp = datetime.now()

    request_log = RequestLog(session_id=session_id, request=url, timestamp=timestamp)

    request.dbsession.add(request_log)


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
