import re
import urllib2
import base64
import json


class VoeResolver(object):

    def get_media_url(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        req = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(req).read()

        # JS redirect
        r = re.search("window.location.href\s*=\s*'([^']+)", html)
        if r:
            url = r.group(1)
            req = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(req).read()

        # encoded JSON
        r = re.search(r'json">\["([^"]+)"]</script>\s*<script\s*src="([^"]+)', html)
        if not r:
            raise Exception("VOE source not found")

        encoded = r.group(1)
        script = r.group(2)

        script_url = url.split("/e/")[0] + script

        req = urllib2.Request(script_url, headers=headers)
        html2 = urllib2.urlopen(req).read()

        repl = re.search(r"(\[(?:'\W{2}'[,\]]){1,9})", html2)

        data = self.voe_decode(encoded, repl.group(1))

        stream = data.get("direct_access_url") or data.get("file") or data.get("source")
        
        if ".m3u8" in stream:
            raise Exception("HLS not supported on Xbox")
        
        return stream


        raise Exception("No stream found")

    def voe_decode(self, ct, luts):

        lut = []

        for i in luts[2:-2].split("','"):
            esc = ""
            for x in i:
                if x in ".*+?^${}()|[]\\":
                    esc += "\\" + x
                else:
                    esc += x
            lut.append(esc)

        txt = ""

        for i in ct:
            x = ord(i)

            if 64 < x < 91:
                x = (x - 52) % 26 + 65
            elif 96 < x < 123:
                x = (x - 84) % 26 + 97

            txt += chr(x)

        for i in lut:
            txt = re.sub(i, "", txt)

        ct = base64.b64decode(txt)

        txt = ""
        for i in ct:
            txt += chr(ord(i) - 3)

        txt = base64.b64decode(txt[::-1])

        return json.loads(txt)
