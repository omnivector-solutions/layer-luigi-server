from charms.reactive import endpoint_from_flag, set_flag, when, when_not
from charmhelpers.core.hookenv import open_port, status_set


LUIGI_SERVER_PORT = 8082


@when('snap.installed.luigi-server')
@when_not('luigi.init.complete')
def open_port_set_status():
    """Open port and set status when luigi snap is installed.
    """
    open_port(LUIGI_SERVER_PORT)
    status_set('active', "Luigi-Server available")
    set_flag('luigi.init.complete')


@when('http.available')
def provide_http_relation_data():
    """Provide http relation data
    """
    endpoint = endpoint_from_flag('http.available')
    endpoint.configure(LUIGI_SERVER_PORT)
