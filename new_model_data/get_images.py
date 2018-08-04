import os
import urllib.request as ulib
from bs4 import BeautifulSoup as Soup

url_a = 'https://www.google.com/search?ei=1m7NWePfFYaGmQG51q7IBg&hl=en&q={}'
url_b = '&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start={}'
url_c = '&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg'
url_base = ''.join((url_a, url_b,url_c))

headers = {'User-Agent': 'Chrome/41.0.2228.0 Safari/537.36'}


def get_links(search_name,num_page):
    search_name = search_name.replace(' ', '+')
    url = url_base.format(search_name, num_page)
    print(url)
    request = ulib.Request(url, None, headers)
    json_string = ulib.urlopen(request).read()
    print(json_string)
    new_soup = Soup(json_string, 'lxml')
    images = new_soup.find_all('img')
    links = [image['src'] for image in images]
    return links


def save_images(links, search_name, num_page):
    directory = search_name.replace(' ', '_')+str(num_page)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for i, link in enumerate(links):
        savepath = os.path.join(directory, '{:06}.png'.format(i))
        ulib.urlretrieve(link, savepath)

def group_images(folder_name):
    imdir = str(folder_name)+'_images'

    folders = [folder for folder in os.listdir('.') if 'py' not in folder]

    if not os.path.isdir(imdir):
        os.mkdir(imdir)

    n = 0
    for folder in folders:
        print(folder)
        for imfile in os.scandir(folder):
            os.rename(imfile.path, os.path.join(imdir, '{:06}.png'.format(n)))
            n += 1
        os.rmdir(folder)

if __name__ == '__main__':
    #search_names = ['referee', 'soccer referee', 'football referee', 'fifa referee', 'arbitro di calcio']
    #search_names = ['croatia shirt football']
    search_names = ['france blue shirt football 2018']
    for search_name in search_names:
        for num_page in range (0, 10):
            links = get_links(search_name, num_page*20)
            save_images(links, search_name, num_page)

    #group_images('referee')
    #group_images('croatia')
    group_images('france')
