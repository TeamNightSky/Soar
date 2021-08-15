import toml
from sanic import response, Blueprint
from sanic.response import html
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('soar/templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=True
)

with open('config.toml') as f:
    config = toml.load(f)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    content = await template.render_async(kwargs)
    return html(content)


def setup(app):
    app.add_route(index, '/')
    app.add_route(login, '/login')
    app.add_route(post, '/post')
    app.add_route(explore, '/explore')


async def index(request):
    return await template('messages.html', config=config['template_data'])


async def login(request):
    return await template('login.html', config=config['template_data'])


async def post(request):
    return await template('post.html', config=config['template_data'])


async def explore(request):
    return await template('explore.html', config=config['template_data'])
