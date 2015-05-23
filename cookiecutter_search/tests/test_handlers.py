# coding: utf-8

from tornado.testing import AsyncHTTPTestCase

from cookiecutter_search.application import MainApplication
from cookiecutter_search.urls import urlpatterns


class GoogleSiteVerificationTest(AsyncHTTPTestCase):
    def get_app(self):
        return MainApplication(urlpatterns)

    def test_responds_to_google_site_verification_url(self):
        response = self.fetch('/googleab9b146cb86fad01.html')
        self.assertEqual(200, response.code)

    def test_return_correct_verification_content(self):
        expected = b'google-site-verification: googleab9b146cb86fad01.html\n'
        response = self.fetch('/googleab9b146cb86fad01.html')
        self.assertEqual(expected, response.body)
