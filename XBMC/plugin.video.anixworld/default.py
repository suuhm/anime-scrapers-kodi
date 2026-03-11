# -*- coding: utf-8 -*-
import re,sys
import urllib,urllib2,cookielib
import time,random
import xbmc,xbmcgui,xbmcplugin, xbmcaddon
from voeresolver import VoeResolver
from HTMLParser import HTMLParser

ADDON = xbmcaddon.Addon()
cookie_jar=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

_base_url=sys.argv[0]
_handle=int(sys.argv[1])

ANIME_CACHE={}
PROXY_BASE = get_base_url()
WIN=xbmcgui.Window(10000)

html_parser=HTMLParser()

USER_AGENTS=[
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/121.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:120.0) Gecko/20100101 Firefox/120.0"
]

def get_base_url():
    base = ADDON.getSetting("base_url")

    if not base:
        try:
            kb = xbmc.Keyboard("", "Anime Seite URL eingeben")
            kb.doModal()

            if kb.isConfirmed():
                base = kb.getText()
                ADDON.setSetting("base_url", base)
        except:
            xbmcgui.Dialog().ok("Fehler", "Bitte URL in den Addon Einstellungen setzen")
            return None

    return base

def set_anime_cache(key,meta):
    def u(v):
        if not v:
            return u""
        try:
            if isinstance(v,str):
                v=v.decode("utf-8","ignore")
        except:
            pass
        return v

    title=u(meta.get("title",""))
    desc=u(meta.get("desc",""))
    year=u(meta.get("year",""))
    genres=u(meta.get("genres",""))
    cover=u(meta.get("cover",""))

    val=u"|||".join([title,desc,year,genres,cover])
    try:
        val=val.encode("utf-8")
    except:
        pass

    ADDON.setSetting(key,val)

def get_anime_cache(anime_key):
    val = ADDON.getSetting(anime_key)
    if not val:
        return {}

    parts = val.split("|||")

    return {
        "title": parts[0] if len(parts)>0 else "",
        "desc": parts[1] if len(parts)>1 else "",
        "year": parts[2] if len(parts)>2 else "",
        "genres": parts[3] if len(parts)>3 else "",
        "cover": parts[4] if len(parts)>4 else ""
    }

def get_html(url):
    for i in range(4):
        ua=random.choice(USER_AGENTS)
        headers={
        "User-Agent":ua,
        "Referer":PROXY_BASE,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"de-DE,de;q=0.9,en;q=0.8",
        "Connection":"keep-alive"}
        try:
            req=urllib2.Request(url,headers=headers)
            r=opener.open(req,timeout=60)
            html=r.read()
            try:
                html=html.decode("utf-8","ignore")
            except:
                pass
            if "ddos-guard" in html.lower():
                time.sleep(random.uniform(1.5,3.5))
                continue
            if len(html)>1500:return html
        except Exception as e:
            xbmc.log("HTTP ERROR: "+str(e))
        time.sleep(random.uniform(1.0,3.0))
    return ""


def clean(title):
    if not title:
        return ""

    try:
        if isinstance(title, str):
            title = title.decode("utf-8","ignore")
    except:
        pass

    title = html_parser.unescape(title)
    title = re.sub(r"<[^>]+>","",title)
    title = re.sub(r"\s*(stream|online schauen|kostenlos|anschauen).*","",title,flags=re.I)
    title = re.sub(r"\b(Deutsch|Ger Sub|German Sub|HD Stream|Stream)\b","",title,flags=re.I)
    title = re.sub(r"\s+-\s+"," - ",title)
    title = re.sub(r"\s+"," ",title)
    return title.strip()
	

def menu():
    xbmcplugin.setContent(_handle,"tvshows")
    for n,m in [("Animes","letters"),("Beliebte Animes","top"),("Neue Episoden","new"),("Suchen","search")]:
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode="+m,xbmcgui.ListItem(n),True)
    xbmcplugin.endOfDirectory(_handle)


def letters():
    xbmcplugin.setContent(_handle,"tvshows")
    for l in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")+["#"]:
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=letter&l="+l,xbmcgui.ListItem(l),True)
    xbmcplugin.endOfDirectory(_handle)

def list_letter(l):
    url=PROXY_BASE+"/katalog/"+l
    html=get_html(url)
    xbmcplugin.setContent(_handle,"tvshows")
    matches=re.findall(r'href="(/anime/stream/[^"]+)".*?title="([^"]+)".*?data-src="([^"]+)"',html,re.S)
    for link,title,thumb in matches:
        title=clean(title)
        if thumb.startswith("/"):thumb=PROXY_BASE+thumb
        li=xbmcgui.ListItem(title)
        li.setThumbnailImage(thumb)
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=anime&url="+urllib.quote(PROXY_BASE+link),li,True)
    xbmcplugin.endOfDirectory(_handle)


def list_top():
    url=PROXY_BASE+"/beliebte-animes"
    html=get_html(url)
    xbmcplugin.setContent(_handle,"tvshows")
    matches=re.findall(r'href="(/anime/stream/[^"]+)".*?title="([^"]+)".*?data-src="([^"]+)"',html,re.S)
    for link,title,thumb in matches:
        title=clean(title)
        if thumb.startswith("/"):thumb=PROXY_BASE+thumb
        li=xbmcgui.ListItem(title)
        li.setThumbnailImage(thumb)
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=anime&url="+urllib.quote(PROXY_BASE+link),li,True)
    xbmcplugin.endOfDirectory(_handle)

#def anime_page(url):
#    html=get_html(url)
#    title=clean(re.search(r'<h1[^>]*><span>(.*?)</span>',html).group(1) if re.search(r'<h1[^>]*><span>(.*?)</span>',html) else"Anime")
#    desc=clean(re.search(r'class="seri_des".*?>(.*?)</p>',html,re.S).group(1) if re.search(r'class="seri_des".*?>(.*?)</p>',html,re.S) else"")
#    year=re.search(r'/jahr/(\d{4})',html)
#    year=year.group(1) if year else""
#    genres=", ".join(re.findall(r'itemprop="genre">(.*?)</a>',html))
#    cover=re.search(r'data-src="([^"]+cover[^"]+)"',html)
#    cover=PROXY_BASE+cover.group(1) if cover and cover.group(1).startswith("/") else cover.group(1) if cover else""
#    anime_key=re.sub(r"\W+","_",title+"_"+year)
#    set_anime_cache(anime_key,{"title":title,"desc":desc,"year":year,"genres":genres,"cover":cover})
#    li=xbmcgui.ListItem(title)
#    li.setThumbnailImage(cover)
#    li.setInfo("Video", {"Title": title, "Plot": desc})
#    xbmcplugin.setContent(_handle,"seasons")
#    xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=seasons&url="+urllib.quote(url)+"&akey="+urllib.quote(anime_key),li,True)
#    xbmcplugin.endOfDirectory(_handle)

def seasons(url):
    html=get_html(url)
    xbmcplugin.setContent(_handle,"seasons")
    
    title=clean(re.search(r'class="seasonEpisodeTitle".*?<span>(.*?)</span>',html).group(1) if re.search(r'class="seasonEpisodeTitle".*?<span>(.*?)</span>',html) else"Anime title onknown")
    desc=clean(re.search(r'class="seri_des".*?>(.*?)</p>',html,re.S).group(1) if re.search(r'class="seri_des".*?>(.*?)</p>',html,re.S) else"")
    year=re.search(r'/jahr/(\d{4})',html)
    year=year.group(1) if year else""
    genres=", ".join(re.findall(r'itemprop="genre">(.*?)</a>',html))
    cover=re.search(r'data-src="([^"]+cover[^"]+)"',html)
    cover=PROXY_BASE+cover.group(1) if cover and cover.group(1).startswith("/") else cover.group(1) if cover else""
    anime_key=re.sub(r"\W+","_",title+"_"+year)
    set_anime_cache(anime_key,{"title":title,"desc":desc,"year":year,"genres":genres,"cover":cover})
    
    s=re.findall(r'(/anime/stream/[^"]+/staffel-(\d+))"',html)
    #xbmcgui.Dialog().notification("Debug",str(desc))
    if not s:return episodes(url,anime_key)
    for link,num in s:
        li=xbmcgui.ListItem("Staffel "+num)
        li.setThumbnailImage(cover)
        li.setInfo("Video", {"Title": title, "Plot": desc})
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=episodes&url="+urllib.quote(PROXY_BASE+link)+"&akey="+urllib.quote(anime_key),li,True)
    xbmcplugin.endOfDirectory(_handle)


def episodes(url,anime_key):
    html=get_html(url)
    xbmcplugin.setContent(_handle,"tvshows")
    meta=get_anime_cache(anime_key)
    title=meta.get("title","Anime")
    desc=meta.get("desc","")
    year=meta.get("year","")
    genres=meta.get("genres","")
    cover=meta.get("cover","")
    #eps=re.findall(r'(/anime/stream/[^"]+/episode-(\d+))"',html)
    eps=re.findall(r'class="seasonEpisodeTitle".*?(/anime/stream/[^"]+/episode-(\d+))".*?<span>(.*?)</span>',html)
    done=[]
    for link,n,tit in eps:
        if link in done:continue
        done.append(link)
        li=xbmcgui.ListItem("Folge "+n+" - "+tit)
        li.setProperty("IsPlayable","true")
        li.setThumbnailImage(cover)
        li.setInfo("Video", {"Title": title, "Plot": desc})
        #li.setLabel(title + "\n" + desc[:50] + "…")
        xbmcplugin.addDirectoryItem(_handle,_base_url+"?mode=play&url="+urllib.quote(PROXY_BASE+link),li,False)
    xbmcplugin.endOfDirectory(_handle)


def get_mirrors(html):
    mirrors = []
    redirect_links = re.findall(r'href="(/redirect/\d+)"', html)
    hoster_names = re.findall(r'<h4[^>]*>([^<]+)</h4>', html)

    for i in range(min(len(redirect_links), len(hoster_names))):
        mirrors.append({
            'url': PROXY_BASE + redirect_links[i],
            'hoster': hoster_names[i].strip()
        })

    xbmc.log("DEBUG: Redirects: {} Hosters: {} Mirrors: {}".format(
        len(redirect_links), len(hoster_names), len(mirrors)
    ), level=xbmc.LOGNOTICE)

    return mirrors


def show_mirror_dialog(mirrors):
    if not mirrors:
        xbmcgui.Dialog().ok('Fehler', 'Keine Streams gefunden')
        return None

    titles = [m['hoster'] for m in mirrors]
    dialog = xbmcgui.Dialog()
    selected = dialog.select('Stream wählen:', titles)

    if selected >= 0:
        return mirrors[selected]['url']
    return None


def redirect_voe(url):
    try:
        voe = VoeResolver()
        stream_url = voe.get_media_url(url)
        return stream_url
    except Exception as e:
        xbmcgui.Dialog().ok("VOE Fehler", str(e))
        return None

def play_voe_with_mirrors(url):
    html = get_html(url)
    mirrors_list = get_mirrors(html)

    selected_url = show_mirror_dialog(mirrors_list)
    if not selected_url:
        return

    stream_url = redirect_voe(selected_url)
    if not stream_url:
        xbmcgui.Dialog().ok("Fehler", "Stream konnte nicht geladen werden")
        return

    li = xbmcgui.ListItem(path=stream_url)
    li.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(_handle, True, li)

def search():
    keyboard = xbmc.Keyboard("", "Anime suchen")
    keyboard.doModal()
    if not keyboard.isConfirmed():
        return
    q = keyboard.getText()
    if not q:
        return

    html = get_html(PROXY_BASE + "/animes")
    xbmcplugin.setContent(_handle,"tvshows")
    m = re.findall(r'(/anime/stream/[^"]+)".*?title="([^"]+)"', html, re.S)
    for url, title in m:
        if q.lower() in title.lower():
            xbmcplugin.addDirectoryItem(
                _handle,
                _base_url + "?mode=anime&url=" + urllib.quote(PROXY_BASE + url),
                xbmcgui.ListItem(clean(title)),
                True
            )
    xbmcplugin.endOfDirectory(_handle)


if __name__=="__main__":
    p={}
    if len(sys.argv)>2:
        for x in sys.argv[2][1:].split("&"):
            if "=" in x:
                k,v=x.split("=",1)
                p[k]=urllib.unquote_plus(v)
    m=p.get("mode","")
    if m=="letters":letters()
    elif m=="letter":list_letter(p.get("l"))
    elif m=="top":list_top()
    elif m=="anime":seasons(p.get("url"))
#    elif m=="seasons":
#        url=p.get("url")
#        anime_key=urllib.unquote(p.get("akey",""))
#        seasons(url,anime_key)
    elif m=="episodes":
        url=p.get("url")
        anime_key=urllib.unquote(p.get("akey",""))
        episodes(url,anime_key)
    elif m=="play": play_voe_with_mirrors(p.get("url"))
    elif m=="search":search()
    else:menu()