import os

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from charmhelpers.core.hookenv import config, charm_dir


LUIGI_SERVER_PORT = 8082
LUIGI_CONFIG_PATH = Path('/var/snap/luigi-server/common/luigid/luigi.cfg')


def render_luigi_config(ctxt=None):
    """Render Luigi config file
    """

    if ctxt:
        ctxt = ctxt
    else:
        ctxt = {}

    if LUIGI_CONFIG_PATH.exists():
        LUIGI_CONFIG_PATH.unlink()

    app_yml = load_template('luigi.cfg.j2')
    app_yml = app_yml.render(ctxt=ctxt)

    LUIGI_CONFIG_PATH.write_text(app_yml)
    LUIGI_CONFIG_PATH.chmod(0o755)


def load_template(name, path=None):
    """ load template file
    :param str name: name of template file
    :param str path: alternate location of template location
    """
    if path is None:
        path = os.path.join(charm_dir(), 'templates')
    env = Environment(
        loader=FileSystemLoader(path))
    return env.get_template(name)
