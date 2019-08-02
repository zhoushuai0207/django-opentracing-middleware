# -*- coding: utf-8 -*-
import json
import logging

from django.http import HttpResponse

from common.baseview import UnCsrfView
from utils.http import requests_noauth

logger = logging.getLogger(__name__)


class PingHandler(UnCsrfView):
    def get(self, request):
        """检查服务是否正常使用"""
        return HttpResponse("OK")

    def post(self, request):
        """检查服务是否正常使用"""
        return HttpResponse("OK")


class TestHandler(UnCsrfView):
    def post(self, request):

        params = dict()
        if request.body:
            params = json.loads(request.body.decode('utf-8'))

        r_data = requests_noauth(request.method, "" + request.get_full_path(), data=json.dumps(params),
                                 headers=self.opentracing_headers)
        if r_data.status_code // 100 == 2:
            data = r_data.json()
            self.response = data
            return self.response_success()
        else:
            return self.response_success()
