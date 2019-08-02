# -*- coding: utf-8 -*-

import logging

import opentracing
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from jaeger_client import Config
from opentracing import tags, Format

LOG = logging.getLogger(__name__)


class TracingMiddleware(MiddlewareMixin):
    """opentracing 调用链 使用"""

    def process_request(self, request):

        if settings.OPENTRSCING:
            if not (hasattr(self, "tracing") and self.tracing):
                config = Config(config={'sampler': {'type': 'const', 'param': 1, },
                                        'local_agent': {'reporting_host': settings.OPENTRSCING_REPORTIONG_HOST,
                                                        'reporting_port': settings.OPENTRSCING_REPORTIONG_PORT, },
                                        'logging': True, }, service_name=settings.OPENTRSCING_SERVER_NAME, )
                self.tracing = config.initialize_tracer()

            span_context = opentracing.tracer.extract(Format.HTTP_HEADERS, request.META)
            operation_name = "HTTP {} {}".format(request.method, request.get_full_path())
            span = opentracing.tracer.start_span(operation_name, child_of=span_context)
            span.set_tag('http.url', request.get_full_path())

            remote_ip = request.get_host()
            if remote_ip:
                span.set_tag(tags.PEER_HOST_IPV4, remote_ip)

            remote_port = request.get_port()
            if remote_port:
                span.set_tag(tags.PEER_PORT, remote_port)
            setattr(request, "span", span)
            span.finish()

    def process_response(self, request, response):
        return response
