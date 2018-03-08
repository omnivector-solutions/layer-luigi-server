from charms.reactive import (
    endpoint_from_flag,
    is_state,
    set_flag,
    when,
    when_not
)

from charmhelpers.core.hookenv import config, open_port, status_set

from charms.layer.luigi_server import render_luigi_config, LUIGI_SERVER_PORT


@when('snap.installed.luigi-server')
@when_not('luigi.config.check.complete')
def configure_luigid():
    """Configure Luigi-Server
    """

    ctxt = {}
    conf = config()

    if conf.get('sendgrid-creds'):
        ctxt['sendgrid'] = \
            {'username': conf.get('sendgrid-creds').split(':')[0],
             'password': conf.get('sendgrid-creds').split(':')[1]}
        ctxt['core'] = {'send_failure_email': True}

    if is_state('hive.ready'):
        hive = RelationBase.from_state('hive.ready')
        ctxt['hive'] = \
            {'metastore_host': hive.get_private_ip(),
             'metastore_port': hive.get_port()}

    render_luigi_config(ctxt=ctxt)

    set_flag('luigi.config.check.complete')


@when('snap.installed.luigi-server')
@when_not('luigi.http.port.available')
def open_port_set_status():
    """Open port and set status when luigi snap is installed.
    """
    open_port(LUIGI_SERVER_PORT)
    status_set('active', "Luigi-Server available")
    set_flag('luigi.http.port.available')


@when('http.available')
def provide_http_relation_data():
    """Provide http relation data
    """
    endpoint = endpoint_from_flag('http.available')
    endpoint.configure(LUIGI_SERVER_PORT)
