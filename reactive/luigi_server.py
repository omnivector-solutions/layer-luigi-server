from charms.reactive import endpoint_from_flag, when, when_not
from charmhelpers.core.hookenv import open_port, status_set


LUIGI_SERVER_PORT = 8082


@when('snap.installed.luigi-server')
@when_not('luigi.init.complete')
def open_port_set_status():
    """Open port and set status when luigi snap is installed.
    """
    open_port(LUIGI_SERVER_PORT)
    status_set('active', "Luigi Server: http://{}")
    set_flag('luigi.init.complete')


@when('endpoint.http.joined')
def provide_http_relation_data():
    """Provide http relation data
    """
    endpoint = endpoint_from_flag('endpoint.http.joined')
    endpoint.configure(port=LUIGI_SERVER_PORT)
