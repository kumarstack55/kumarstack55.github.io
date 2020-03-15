#!/usr/bin/env python
# coding: utf-8

import argparse
import jinja2
import pathlib
import yaml


def render(data, template):
    script_dir = pathlib.Path(__file__).resolve().parent
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_dir))
    template = env.get_template(template)
    ctx = dict(data=data)
    return template.render(ctx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default='data.yml')
    parser.add_argument("--template", default='index.html.j2')
    parser.add_argument("--output", default='index.html')
    args = parser.parse_args()

    with open(args.data, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    record = dict(heading='目次', nav_menus=True)
    list_items = list()
    for r in data:
        name = r.get('heading')
        list_items.append({'name': name, 'url': '#%s' % (name)})
    record.update(list_items=list_items)
    data.insert(0, record)

    html = render(data=data, template=args.template)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
