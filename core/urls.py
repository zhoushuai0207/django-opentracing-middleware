from django.conf.urls import url

from core.views import PingHandler, TestHandler

demo_urls = [url(r'^ping$', PingHandler.as_view()), url(r'^test$', TestHandler.as_view()), ]
