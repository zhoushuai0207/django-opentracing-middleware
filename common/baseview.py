import datetime
import json

import opentracing
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from opentracing import Format


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class UnCsrfView(View):
    def __init__(self, *args, **kwargs):
        super(UnCsrfView, self).__init__(*args, **kwargs)
        self.response = dict()
        self.request = None
        self.opentracing_headers = {}

    def get_opentracing_headers(self, request):
        headers = {}
        if hasattr(request, "span"):
            opentracing.tracer.inject(span_context=request.span.context, format=Format.HTTP_HEADERS, carrier=headers)
        return headers

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.opentracing_headers = self.get_opentracing_headers(request)
        return super(UnCsrfView, self).dispatch(request, *args, **kwargs)

    def response_success(self):
        self.response["requestId"] = self.request.request_id
        self.response["timestamp"] = self.request.timestamp
        return JsonResponse(self.response, encoder=DateTimeEncoder)
