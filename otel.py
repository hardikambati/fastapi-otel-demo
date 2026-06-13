import logging
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider



# Resource
def get_resource():
    return Resource.create({
        "service.name": "fastapi-otel-demo"
    })

# Logger provider
logger_provider = LoggerProvider(resource=get_resource())

# Exporter -> Loki
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(endpoint="http://otel-collector:4318/v1/logs")
    )
)


# Set global provider
set_logger_provider(logger_provider)

handler = LoggingHandler(
    level=logging.INFO,
    logger_provider=logger_provider,
)

root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

print("[SETUP] OTEL LOGGING INITIALIZED")