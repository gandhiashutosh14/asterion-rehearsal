"""Optional OTel spans; never capture contract text, raw notes or credentials."""
from contextlib import contextmanager
import os
_configured = False

def configure() -> None:
    global _configured
    if _configured:
        return
    endpoint = os.environ.get("ASTERION_OTLP_ENDPOINT")
    if not endpoint:
        return
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    provider = TracerProvider(resource=Resource.create({"service.name": "asterion"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)
    _configured = True

@contextmanager
def span(name: str):
    try:
        from opentelemetry import trace
    except ImportError:
        yield None
        return
    with trace.get_tracer("asterion").start_as_current_span(name) as current:
        yield current
