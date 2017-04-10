import urllib.request as r
import bs4


def do_something():
    url = 'http://hip-hop.name/text/guf/'
    response = r.urlopen(url)
    html_doc = response.read()
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    links = [x for x in filter(lambda x: x is not None and x[:4] == '/guf', links)]
    texts_urls = ['http://hip-hop.name' + link for link in links]
    learning_text = ''
    for url in texts_urls:
        try:
            response = r.urlopen(url)
            html_doc = response.read()
            soup = bs4.BeautifulSoup(html_doc, 'html.parser')
            s = soup.find_all('div', 'entry')[0]
            learning_text += s.get_text()
        except:  # just don't care about some troubles
            pass
