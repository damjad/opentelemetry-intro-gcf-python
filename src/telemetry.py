from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.resourcedetector.gcp_resource_detector import GoogleCloudResourceDetector
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.semconv.resource import ResourceAttributes

request_counter = None


def _setup_telemetry():
    global request_counter

    # Detect context and resource in which the code is executed. Set resource attributes accordingly.
    # These attributes are appear as dimensions (metadata) in the metrics.
    resource = GoogleCloudResourceDetector(raise_on_error=True).detect()
    print(resource.attributes)

    # Create a backend exporter for sending metrics.
    gcp_metrics_exporter = CloudMonitoringMetricsExporter(
        add_unique_identifier=True,
        prefix=f'custom.googleapis.com/function/{resource.attributes[ResourceAttributes.FAAS_NAME]}'
    )

    # Attach the exporter to the provider with a periodic reader
    metrics_reader = PeriodicExportingMetricReader(gcp_metrics_exporter)

    # Set up the metrics provider
    metrics_provider = MeterProvider(
        metric_readers=[metrics_reader],
        resource=resource
    )

    meter = metrics_provider.get_meter("com.danish.world.telemetry")
    # Create a counter
    request_counter = meter.create_counter(
        "danish-requests",
        description="Number of requests received",
        unit="1",  # Unit is "1" as it counts occurrences
    )


# Ensure this is called at the start
_setup_telemetry()
