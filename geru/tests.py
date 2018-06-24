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

    def test_quotes_list_success(self):
        from .views.default import quotes_list
        info = quotes_list(dummy_request(self.session))
        self.assertEqual(info.status_code, 200)
        self.assertEqual(len(info.json['quotes']) > 0, True)


class TestQuoteDetail(BaseTest):

    def setUp(self):
        super(TestQuoteDetail, self).setUp()
        self.init_database()

    def test_quote_detail_success(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 1
        info = quotes_detail(request)
        self.assertEqual(info.status_code, 200)
        self.assertEqual('quote' in info.json, True)

    def test_quote_detail_bad_request(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 'a'
        info = quotes_detail(request)
        self.assertEqual(info.status_code, 502)

    def test_quote_detail_quote_not_found(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 10000
        info = quotes_detail(request)
        self.assertEqual(info.status_code, 404)

    def test_quote_detail_random_success(self):
        from .views.default import quotes_detail

        request = dummy_request(self.session)
        request.matchdict['pk'] = 'random'
        info = quotes_detail(request)
        self.assertEqual(info.status_code, 200)
        self.assertEqual('quote' in info.json, True)
        self.assertEqual('pk' in info.json, True)


class TestRequestLog(BaseTest):

    def setUp(self):
        super(TestRequestLog, self).setUp()
        self.init_database()

    def test_request_log_for_quote_list(self):

        from .views.default import quotes_list
        from .models import RequestLog
        request = dummy_request(self.session)
        quotes_list(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.session_id == session_id).first()

        self.assertEqual(log.session_id, session_id)
        self.assertEqual(log.request, request.path)

    def test_request_log_for_quote_detail(self):

        from .views.default import quotes_list
        from .models import RequestLog
        request = dummy_request(self.session)
        quotes_list(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.session_id == session_id).first()

        self.assertEqual(log.session_id, session_id)
        self.assertEqual(log.request, request.path)

    def test_request_log_for_request_log(self):

        from .views.default import log_requests_list
        from .models import RequestLog
        request = dummy_request(self.session)
        log_requests_list(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.session_id == session_id).first()

        self.assertEqual(log.session_id, session_id)
        self.assertEqual(log.request, request.path)

    def test_request_log_for_home(self):

        from .views.default import home
        from .models import RequestLog
        request = dummy_request(self.session)
        home(request)

        session_id = request.session['userid']

        query = request.dbsession.query(RequestLog)

        log = query.filter(RequestLog.session_id == session_id).first()

        self.assertEqual(log.session_id, session_id)
        self.assertEqual(log.request, request.path)


class TestRequestLogList(BaseTest):

    session_id = str(uuid.uuid4())
    request = '/test'
    date = datetime.now()

    def setUp(self):
        super(TestRequestLogList, self).setUp()
        self.init_database()

        from .models import RequestLog

        quote = RequestLog(session_id = self.session_id, request=self.request, timestamp=self.date)
        self.session.add(quote)

    def teste_log_request_list_success(self):

        from .views.default import log_requests_list
        info = log_requests_list(dummy_request(self.session))
        log = info.json['requests'][0]
        self.assertEqual(info.status_code, 200)
        self.assertEqual(log['sessionId'], self.session_id)


class TestQuotesWrapper(BaseTest):

    def test_get_quotes_succes(self):
        from .wrapper.quotes_wrapper import QuotesWrapper

        status, quotes = QuotesWrapper.get_quotes()
        self.assertEqual(status, 200)
        self.assertEqual(len(quotes['quotes']) > 0, True)

    def test_get_quote_success(self):
        from .wrapper.quotes_wrapper import QuotesWrapper

        status, quote = QuotesWrapper.get_quote(0)
        self.assertEqual(status, 200)
        self.assertEqual('quote' in quote, True)

    def test_get_quote_random_success(self):
        from .wrapper.quotes_wrapper import QuotesWrapper

        status, quote = QuotesWrapper.get_quote_random()
        self.assertEqual(status, 200)
        self.assertEqual('quote' in quote, True)

    def test_get_quote_bad_request(self):
        from .wrapper.quotes_wrapper import QuotesWrapper

        status, quote = QuotesWrapper.get_quote('a')
        self.assertEqual(status, 502)

    def test_get_quote_not_found(self):
        from .wrapper.quotes_wrapper import QuotesWrapper

        status, quote = QuotesWrapper.get_quote(1000)
        self.assertEqual(status, 404)