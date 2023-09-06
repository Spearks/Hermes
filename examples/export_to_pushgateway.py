from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import time

# Prometheus Pushgateway URL
pushgateway_url = 'http://0.0.0.0:9091'

# Create a CollectorRegistry
registry = CollectorRegistry()

# Create Gauge metrics for six pressure channels
pressure_gauges = []
for i in range(1, 7):
    gauge_name = f'dummy_nome_{i}'
    gauge_description = f'Random pressure data for channel {i} in Bar'
    pressure_gauges.append(Gauge(gauge_name, gauge_description, registry=registry))

while True:
    for i, gauge in enumerate(pressure_gauges):
        # Generate random pressure value between 0 and 10
        pressure = random.uniform(0, 10)

        # Set the value of the Gauge metric for the corresponding channel
        gauge.set(pressure)
    
    # Push all metrics to Prometheus Pushgateway
    push_to_gateway(pushgateway_url, job='pressure_monitor', registry=registry)
    
    # Sleep for 1 second before generating the next data point
    time.sleep(1)

