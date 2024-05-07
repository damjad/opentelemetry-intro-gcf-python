import time

import functions_framework

import telemetry


@functions_framework.http
def hello_http(request):
    time.sleep(5)
    telemetry.request_counter.add(10)

    return 'Hello {}!'.format(process_request(request))


def process_request(request):
    request_json = request.get_json(silent=True)

    if request_json and 'name' in request_json:
        name = request_json['name']
    else:
        name = 'World'
    return name
