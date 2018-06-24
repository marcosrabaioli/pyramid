import unittest
import transaction

from pyramid import testing

import uuid

from datetime import datetime

def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestQuoteList(BaseTest):

    def setUp(self):
        super(TestQuoteList, self).setUp()
        self.init_database()

        from .models import Quote

        quote = Quote(quote='Quote test.')
        self.session.add(quote)

    def test_quotes_list_success(self):
        from .views.default import quotes_list
        info = quotes_list(dummy_request(self.session))
        self.assertEqual(info['quotes'], ['Quote test.'])



class TestQuoteDetail(BaseTest):

    def setUp(self):
        super(TestQuoteDetail, self).setUp()
        self.init_database()

        from .models import Quote

        quote = Quote(quote='Quote test.')
        self.session.add(quote)

    def test_quote_detail_success(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 1
        info = quotes_detail(request)
        self.assertEqual(info['quote'], 'Quote test.')

    def test_quote_detail_bad_request(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 'a'
        info = quotes_detail(request)
        self.assertEqual(info.status_code, 400)


    def test_quote_detail_random_success(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 'random'
        info = quotes_detail(request)
        self.assertEqual(info['pk'], 1)
        self.assertEqual(info['quote'], 'Quote test.')


class TestRequestLog(BaseTest):

    def setUp(self):
        super(TestRequestLog, self).setUp()
        self.init_database()

        from .models import Quote

        quote = Quote(quote='Quote test.')
        self.session.add(quote)

    def test_request_log_for_quote_list(self):

        from .views.default import quotes_list
        from .models import RequestLog
        request = dummy_request(self.session)
        quotes_list(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.sessionId == session_id).first()

        self.assertEqual(log.sessionId, session_id)
        self.assertEqual(log.request, request.path)

    def test_request_log_for_quote_detail(self):

        from .views.default import quotes_list
        from .models import RequestLog
        request = dummy_request(self.session)
        quotes_list(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.sessionId == session_id).first()

        self.assertEqual(log.sessionId, session_id)
        self.assertEqual(log.request, request.path)


class TestRequestLogList(BaseTest):

    session_id = str(uuid.uuid4())
    request = '/test'
    date = datetime.now()

    def setUp(self):
        super(TestRequestLogList, self).setUp()
        self.init_database()

        from .models import RequestLog

        quote = RequestLog(sessionId = self.session_id, request=self.request, timestamp=self.date)
        self.session.add(quote)

    def teste_log_request_list_success(self):

        from .views.default import log_requests_list
        info = log_requests_list(dummy_request(self.session))
        log = info['requests'][0]
        self.assertEqual(log['sessionId'], self.session_id)