#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import bs4
import urllib.request as r
from os.path import splitext
import numpy as np
from random import sample
import re
from urllib.parse import urlparse, urljoin
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
import numpy as np
init_notebook_mode(connected=True)
# %matplotlib inline


init_url = 'http://www.mccme.ru'


def netloc(url):
    return urlparse(url).netloc


def scheme(url):
    return urlparse(url).scheme


def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext


def is_file(url):
    page_extensions = ['', 'html', 'htm', 'php', 'ru', 'com', 'net', 'edu']
    ext = get_ext(url)
    if ext.lower()[1:] in page_extensions:
        return False
    return True


def find_inner_urls(url, filter_name='', ignore_ftp=True, ignore_files=True):
    """
    filter_name: must be in url path
    return: inner hyperlinks at url
    """
    inner_urls = set()
    num_of_attemps = 3

    if ignore_files and is_file(url):
        print("FILE DETECTED: {}".format(url))
        return inner_urls

    content = ''

    # connection
    for attemp in range(num_of_attemps):
        try:
            response = r.urlopen(url)
            content = response.read()
        except r.URLError as url_e:
            print("Can't read URL: {}".format(url))
            return inner_urls
        except TimeoutError as te:
            print("Failed to load URL: {}".format(url))
            return inner_urls
        except Exception as e:
            if attemp + 1 == num_of_attemps:
                print("Failed to load (unknown exception) URL: {}".format(url))
                return inner_urls
            print("Error raised. URL: {}".format(url))
            print("Trying to download again {}/{}".format(attemp, num_of_attemps))
        finally:
            break

    # parse utils
    is_short_url = (re.match(r'^(http|ftp|www)', url) is None)

    # parsing
    soup = bs4.BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('a', href=True):
        link_url = link['href']
        if ignore_ftp:
            if scheme(link_url).startswith('ftp'):
                continue
        if filter_name in netloc(link_url):
            inner_urls.add(link_url)
        elif is_short_url:
            full_url = urljoin(url, link_url)
            inner_urls.add(full_url)
    return inner_urls


def get_links_graph(url, filter_name='', depth_bound=10, ignore_files=True):
    used_urls = set()

    g = nx.DiGraph()
    urls_to_parse = {url}
    while True:
        try:
            next_url = sample(urls_to_parse, 1)[0]
            urls_to_parse.remove(next_url)
        except Exception as e:  # set is empty
            break
        print(next_url)
        if next_url in used_urls:
            continue
        used_urls.add(next_url)
        inner_urls = find_inner_urls(next_url, filter_name)
        new_urls_added = 0
        for inner_url in inner_urls:

            if ignore_files and is_file(inner_url):  # ignore files in web-sites
                continue

            g.add_edge(next_url, inner_url)
            if (inner_url not in urls_to_parse) and (inner_url not in used_urls):
                print(' ->{}'.format(inner_url))
                urls_to_parse.add(inner_url)
                new_urls_added += 1
        print("URLs added: {}".format(new_urls_added))
        if (len(used_urls) > depth_bound):
            print("Riched depth bound")
            break
        else:
            print("Total URLS in Graph: {}".format(len(used_urls)))

    return g


def pagerank(graph, d=0.85, n_max_iterations=1000):
    init_value = 1.0 / len(graph.nodes())
    ranks = {node: init_value for node in graph.nodes()}
    output_count = {node: 0 for node in graph.nodes()}
    neigbours = {node: set() for node in graph.nodes()}

    for begin, end in graph.edges():
        neigbours[end].add(begin)
        output_count[begin] += 1

    for node, outlink_count in output_count.items():
        if outlink_count == 0:
            output_count[node] = len(graph.nodes())
            for l_node in graph.nodes():
                neigbours[l_node].add(node)

    eps = 0.0000001
    delta = 1
    n_iterations = 0

    while delta > eps and n_iterations < n_max_iterations:
        new_ranks = {}
        for node in ranks.keys():
            new_ranks[node] = (1 - d) * init_value +\
                              d * np.sum([ranks[i] / output_count[i] for i in neigbours[node]])
        delta = np.max(np.abs([new_ranks[node] - ranks[node] for node in ranks.keys()]))
        ranks = new_ranks
        n_iterations += 1

    return ranks


def test_page_rank(pagerank):
    G = nx.DiGraph()
    G.add_edge('один', 'два')
    G.add_edge('два', 'три')
    G.adjacency_list()

    my_page_rank = pagerank(G, d=0.85)
    inbox_page_rank = nx.pagerank(G, alpha=0.85)
    print(my_page_rank)
    print(inbox_page_rank)
    assert np.sum([np.abs(my_page_rank[node] - inbox_page_rank[node])
                   for node in my_page_rank]) < 1e-4
    print('OK!')


test_page_rank(pagerank)


def plot_graph(G):
    pos = nx.fruchterman_reingold_layout(G)

    dmin = 1
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            dmin = d

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    page_rangs = nx.pagerank(G)

    for node, adjacencies in enumerate(G.adjacency_list()):
        url = G.nodes()[node]
        node_trace['marker']['color'].append(page_rangs[url])
        if url[-1] == '/':
            url = url[:-1]
        node_info = "<a href={}>{}, PR: {:2f}</a>"\
            .format(url, url, node_trace['marker']['color'][-1])
        node_trace['text'].append(node_info)

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title='<br><a href=http://www.mccme.ru>http://www.mccme.ru</a> network graph',
                    titlefont=dict(size=16),
                    showlegend=False,
                    width=1024,
                    height=768,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    iplot(fig)

plot_graph(g)
