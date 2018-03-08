from charms.reactive import (
    clear_flag,
    endpoint_from_flag,
    hook,
    is_flag_set,
    RelationBase,
    set_flag,
    when,
    when_any,
    when_not,
)

from charmhelpers.core.hookenv import config, open_port, status_set

from charms.layer.luigi_server import render_luigi_config, LUIGI_SERVER_PORT


@hook('start')
def set_started():
    set_flag('started')


@when('snap.installed.luigi-server', 'started')
@when_not('luigi.config.check.complete')
def configure_luigid():
    """Configure Luigi-Server
    """

    ctxt = {}
    conf = config()

    if conf.get('sendgrid-creds'):
        ctxt['sendgrid'] = {
            'username': conf.get('sendgrid-creds').split(':')[0],
            'password': conf.get('sendgrid-creds').split(':')[1]
        }
        ctxt['core'] = {'send_failure_email': True}
        ctxt['email'] = {
            'method': "sendgrid",
            'receiver': conf.get('email-recipient', "")
        }

    if is_flag_set('hive.ready'):
        hive = RelationBase.from_flag('hive.ready')
        ctxt['hive'] = {
            'metastore_host': hive.get_private_ip(),
            'metastore_port': hive.get_port()
        }

    if is_flag_set('spark.ready'):
        spark = RelationBase.from_flag('spark.ready')
        ctxt['spark'] = {'master': spark.get_master_url()}

    render_luigi_config(ctxt=ctxt)
    set_flag('luigi.config.check.complete')


@when('snap.installed.luigi-server')
@when_not('luigi.http.port.available')
def open_port_set_status():
    """Open port and set status when luigi snap is installed
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


@when('started')
@when_any('hive.ready', 'spark.ready')
def re_render_config():
    clear_flag('luigi.config.check.complete')
