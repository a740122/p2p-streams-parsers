# -*- coding: utf-8 -*-
import xbmc,urllib

all_modules = [ 'http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Wiziwig.tv/wiziwig.tar.gz?raw=true', 'http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Arenavision.in/arenavision.tar.gz?raw=true', 'http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Livefootball.ws/livefootballws.tar.gz?raw=true', 'http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Livefootballvideo.com/livefootballvideo.tar.gz?raw=true', 'http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Livefootballaol.com/livefootballaol.tar.gz?raw=true','http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Rojadirecta.me/rojadirecta.tar.gz?raw=true','http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/SopCast.ucoz/sopcastucoz.tar.gz?raw=true','http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Torrent-tv.ru%20all/torrenttvruall.tar.gz?raw=true','http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/Torrent-tv.ru%20sports/torrenttvrusports.tar.gz?raw=true','http://github.com/manuelsousa7/p2p-streams-parsers/blob/master/1Torrent.tv/onetorrenttv.tar.gz?raw=true']

for parser in all_modules:
	xbmc.executebuiltin('XBMC.RunPlugin("plugin://plugin.video.p2p-streams/?mode=405&name=p2p&url=' + urllib.quote(parser) + '")')
	xbmc.sleep(1000)

xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('P2P-Streams', "All parsers imported",1,''))
