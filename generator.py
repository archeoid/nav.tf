from jinja2 import FileSystemLoader, Environment
import os
from os.path import join as pjoin
import inspect
from shutil import copytree
import xml.etree.ElementTree as ET

def pwd():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    return path

pwd = pwd()

###
def outFile(path, content):
    with open(path, 'w') as f:
        f.write(content)

def write(section, page, platform, content):
    base = pjoin(pwd, 'output', platform, section, page)
    path = pjoin(base, 'index.html')

    os.makedirs(base, exist_ok=True)
    outFile(path, content)

def read(section, page):
    path = pjoin(pwd, 'content', section, page, 'index.html')

    out = ""
    with open(path, 'r') as f:
        out = f.read()
    
    return out

    
### Parse the site structure from structure.xml
sections = []
default = ""

root = ET.parse(pjoin(pwd, 'structure.xml')).getroot()
default = root.get("default")
for s in root.findall('section'):
    sn = s.get('name')
    sections.append({'name':sn, 'href':f'/{sn}/', 'default':s.get('default'), 'pages':[]})
    for p in s.findall('page'):
        pn = p.get('name')
        sections[-1]['pages'].append({'name': pn, 'href': f'/{sn}/{pn}/'})

### Load the templates
loader = FileSystemLoader(searchpath='templates')
env = Environment(loader=loader, autoescape=False, trim_blocks=True, lstrip_blocks=True)


### Render the HTML templates and copy auxiliary files
style = pjoin(pwd, 'style')
output = pjoin(pwd, 'output')
content = pjoin(pwd, 'content')

platforms = ['desktop', 'mobile']
for platform in platforms:
    t = env.get_template(platform + '.html')
    for s in sections:
        pages = s['pages']
        for p in pages:
            copytree(pjoin(content, s['name'], p['name']), pjoin(output, platform, s['name'], p['name']), dirs_exist_ok=True)
            html = read(s['name'], p['name'])
            out = t.render(sections=sections, pages=pages, content=html)
            write(s['name'], p['name'], platform, out)
    copytree(pjoin(style, 'both'), pjoin(output, platform), dirs_exist_ok=True)
    copytree(pjoin(style, platform), pjoin(output, platform), dirs_exist_ok=True)

## Render the nginx configs
nginx = env.get_template("nginx.conf")
conf = nginx.render(sections=sections, default=default)
outFile(pjoin(pwd, 'output', 'url.conf'), conf)


