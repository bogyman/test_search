import json
from collections import defaultdict

import requests

base_url_get = 'http://www.giantbomb.com/api/games/?api_key=84e4fdf8957ddf84247c3ea012a4773ffead8156&format=json&offset={offset}&limit={limit}&platforms={platform}&&field_list=deck,name,image,platforms,site_detail_url'
base_url_fetch = 'http://www.giantbomb.com/api/games/?api_key=84e4fdf8957ddf84247c3ea012a4773ffead8156&format=json&offset=0&limit=1&platforms={platform}&&field_list=name'

platforms = ['21', '9', '43']

LIMIT = 300
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


def fetch_resources():
    """
    Get amount of items on each resource
    :return:
    """
    platforms_count = {}
    for platform in platforms:
        url = base_url_fetch.format(platform=platform)
        response = requests.get(url, headers={'user-agent': user_agent})
        data = json.loads(response.content)
        platforms_count[platform] = int(data['number_of_total_results'])
        # platforms_count[platform] = 10  # reduce giantbomb load, they asked

    return platforms_count


def get_nodes_offsets(node_holder, platforms2count):
    """
    Calculate what part of data should process each node
    :param node_holder:
    :param platforms2count:
    :return:
    """
    nodes_offsets = defaultdict(dict)
    nodes_count = node_holder.nodes_count()

    for platform, items_count in platforms2count.items():
        iterations_count = (items_count // LIMIT) + (items_count % LIMIT and 1 or 0)
        avg_iterations = iterations_count // nodes_count + (iterations_count % nodes_count and 1 or 0)
        iterations_list = [LIMIT*i for i in range(iterations_count)]

        for i, node in enumerate(node_holder.get_nodes()):
            nodes_offsets[node][platform] = iterations_list[0:avg_iterations]
            iterations_list = iterations_list[avg_iterations:]

    return nodes_offsets


def get_nodes_tasks(nodes_offsets):
    """
    Make list of urls for nodes
    :param nodes_iterations:
    :return:
    """
    nodes_tasks = defaultdict(set)
    for node, platform_offset in nodes_offsets.items():
        for platform, offsets in platform_offset.items():
            for offset in offsets:
                url = base_url_get.format(
                    limit=LIMIT,
                    offset=offset,
                    platform=platform
                )
                nodes_tasks[node].add(url)

    return nodes_tasks


def get_resource(url):
    """
    Get items from external resource
    :param url:
    :return:
    """
    response = requests.get(url, headers={'user-agent': user_agent})
    return json.loads(response.content)['results']

