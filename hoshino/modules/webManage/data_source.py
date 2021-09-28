import jinja2
import os
import random
from quart import session, url_for

template_folder = os.path.join(os.path.dirname(__file__), 'templates')

static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


def _url_for(endpoint, *args, **kwargs):
    if endpoint == 'static':
        kwargs['v'] = '1.0'
    return url_for(endpoint, *args, **kwargs)


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_folder),
    enable_async=True
)

env.globals['session'] = session
env.globals['url_for'] = _url_for


async def render_template(template, **kwargs):
    t = env.get_template(template)
    return await t.render_async(**kwargs)


def get_random_str(num: int):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt
