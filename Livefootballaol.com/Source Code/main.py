# -*- coding: utf-8 -*-

""" P2P-STREAMS XBMC ADDON

http://1torrent.tv module parser

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
import acestream as ace

base_url = 'http://www.livefootballol.com/sopcast-channel-list.html'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: livefootballaol_main()
    
def livefootballaol_main():
	try:
		source = abrir_url(base_url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('">(.+?)</s.+?td>\n<td>(.+?)</td>\n<td>(.+?)</td>').findall(source)
		for titulo,sopaddress,language in match:
			addDir("[B][COLOR orange][SopCast] [/COLOR]"+titulo.replace('<strong>','').replace('</a>','')+"[/B] ("+language.replace('<strong>','').replace('</strong>','')+ ')',sopaddress,2,os.path.join(current_dir,"icon.png"),len(match),False)
