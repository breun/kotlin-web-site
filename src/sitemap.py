from os import path

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


root_folder_path = path.dirname(path.dirname(__file__))


def generate_sitemap(pages):
    non_static_urls = []

    for url, type in pages:
        if type is None:
            continue

        is_page = type.startswith('Page')
        is_exclude = type == 'Page_NotFound'

        if is_page and not is_exclude:
            location = dict(url=url, priority=0.3, lastmod=None)

            if url == '/':
                location['priority'] = 1
            if type == 'Page_Documentation':
                location['priority'] = 0.8

            non_static_urls.append(location)

    env = Environment(loader=FileSystemLoader(path.join(root_folder_path, 'templates')))
    template = env.get_template('sitemap.xml')
    sitemap_content = template.render(locations=non_static_urls)

    with open(path.join(root_folder_path, 'dist', 'sitemap.xml'), 'w') as sitemap_file:
        sitemap_file.write(sitemap_content)
