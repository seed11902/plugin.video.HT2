# -*- coding: utf-8 -*- 
import urllib,urllib2,re,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
import urlparse
import requests
import base64
import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
def find(pattern, string):
        match = re.search(pattern,string)
        if match:
                ret =  match.group()
        else: 
                ret = "not find"
        return ret
def hdx3(url):
        #http://hdx3.blogspot.com/search/label/Regular%20Show?max-results=200
        #http://hdx3.blogspot.com/search/label/Mr.%20Pickles
        #http://hdx3.blogspot.com/search/label/%E6%8E%A2%E9%9A%AA%E6%B4%BB%E5%AF%B6?max-results=200
        while url:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            for outer in soup.select('.post-outer'):
                for a in outer.find_all('a', href=True):
                    try:
                        resSub = requests.get(a['href'])
                        soupSub = BeautifulSoup(resSub.text, "html.parser")       
                        for hentry in soupSub.select('.hentry'):
                            for index,iframe in enumerate(hentry.select('iframe')):
                                findxuite = iframe['src'].find('http://vlog.xuite.net');
                                if findxuite == 0:
                                    for content in hentry.select('.entry-content'):
                                        str1 = content.text.replace('\n','')
                                        str1 = str1.replace(' ', '')
                                        text = find(u'密碼\W*：' + r'\d{4}',str1)
                                        passwd = text[-4:]
                                    url = urlparse.urlparse(iframe['src'])
                                    mediumId = base64.b64decode(url.path.split('/')[2]).split('-')[1].split('.')[0]
                                    #http://vlog.xuite.net/_ajax/default/media/ajax?act=checkPasswd&mediumId=26057911&passwd=0214
                                    a = 'http://vlog.xuite.net/_ajax/default/media/ajax?act=checkPasswd&mediumId={}&passwd={}'.format(mediumId, passwd)
                                    obj = requests.get(a).json()
                                    encodedjson = json.dumps(obj)
                                    jd = json.loads(encodedjson)
                                    encodedjson2 = json.dumps(jd["media"])
                                    jd2 = json.loads(encodedjson2)
                                    if index == 0:
                                        title = hentry.select('h3')[0].text.replace('\n', '')
                                    else:
                                	title = hentry.select('h3')[0].text.replace('\n', '') + str(index)                                    
                                    media = jd2["html5Url"]
                                    image = 'http://vlog.xuite.net' + jd2["thumbnailUrl"]
                                    addLink(title, media, image)
                    except:
                        print("except")
            test = soup.find("a", {"id": "Blog1_blog-pager-older-link"})
            if test:
                url = test['href']
            else:
                break
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=liz)
        return ok
def adddir(name,Url,iconimage):
        ok=True
        url = build_url(Url)
        li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage=iconimage)
        li.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)        
        return ok
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
        adddir('Regular Show',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Regular%20Show?max-results=200'},'')
        adddir('Adventure Time',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Adventure%20Time?max-results=200'},'')
        adddir('Superjail',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Superjail?max-results=200'},'')
        adddir('Ugly Americans',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Ugly%20Americans?max-results=200'},'')
        adddir('Mr. Pickles',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Mr.%20Pickles?max-results=200'},'')
        adddir('My Little Pony',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/My%20Little%20Pony?max-results=200'},'')
        adddir('Sonic Boom',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Sonic%20Boom?max-results=200'},'')
        adddir('Bee and PuppyCat',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Bee%20and%20PuppyCat?max-results=200'},'')
        adddir('Metalocalypse',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Metalocalypse?max-results=200'},'')
        adddir('Rick and Morty',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/Rick%20and%20Morty?max-results=200'},'')
        adddir('RWBY',{'mode': 'folder', 'Url': 'http://hdx3.blogspot.com/search/label/RWBY?max-results=200'},'')
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
        Url = args['Url'][0]
        hdx3(Url)
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)
