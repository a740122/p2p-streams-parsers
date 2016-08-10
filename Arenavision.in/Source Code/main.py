# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of p2p-streams addon

Arenavision.in

edited by manuelsousa7

"""
import sys,os,requests
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from peertopeerutils.webutils import *
from peertopeerutils.pluginxbmc import *
from peertopeerutils.directoryhandle import *
import acestream as ace
import sopcast as sop
from cleaner import *
import operator


base_url = "http://www.arenavision.in/"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: arenavision_menu()
	elif parserfunction == "arenavision_streams": arenavision_streams(name,url)
	elif parserfunction == "arenavision_schedule": arenavision_schedule(url)
	elif parserfunction == "arenavision_chooser": arenavision_chooser(url)
	


def arenavision_menu():
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(base_url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('leaf"><a href="(.+?)">(.+?)</a').findall(source)
		for link, nome in match:
			if "agenda" in nome.lower():
				addDir("[B][COLOR red]Agenda/Schedule[/COLOR][/B]",base_url+link,401,os.path.join(current_dir,"icon.png"),1,True,parser="arenavision",parserfunction="arenavision_schedule")
			elif "#" in nome.lower() or "av" in nome.lower() or "arenavision" in nome.lower():
				addDir(nome,base_url+link,401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision",parserfunction="arenavision_streams")
			else: pass


def arenavision_streams(name,url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('sop://(.+?)"').findall(source)
		if match: sop.sopstreams(name,os.path.join(current_dir,"icon.png"),"sop://" + match[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: ace.acestreams(name,os.path.join(current_dir,"icon.png"),match[0])
			else: xbmcgui.Dialog().ok(translate(40000),translate(40022))

def arenavision_schedule(url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.findall('(.*?)</tr><tr><td class="auto-style3"', source, re.DOTALL)

		for event in match:
			eventmatch = re.compile('>(\d+)/(\d+)/(\d+)</td>\n<td class="auto-style3" style="width: 182px">(.+?):(.+?) CET</td>\n<td class="auto-style3" style="width: 188px">(.+?)</td>\n<td class="auto-style3" style="width: 283px">(.+?)</td>\n<td class="auto-style3" style="width: 685px">(.+?)<').findall(event)
			iii=1
			for dia,mes,year,hour,minute,modalidade,campeonato,evento in eventmatch:
				try:
					import datetime
					from peertopeerutils import pytzimp
					d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(mes), int(dia), hour=int(hour), minute=int(minute)))
					timezona= settings.getSetting('timezone_new')
					my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
					convertido=d.astimezone(my_location)
					fmt = "%d-%m-%y %H:%M"
					time=convertido.strftime(fmt)
				except:
					time='N/A'
				c1=re.findall('style="width: 317px">(.+?)</td>', event, re.DOTALL)
				c1=c1[0].split()
				c1=[ x for x in c1 if "/>" not in x ]
				for x in range(0,len(c1)):
					if c1[x][0]=='[':
						c1[x]=c1[x][0:4]+"]"
				dic={}
				dic["temp"]=[]
				for x in c1:
					if x[0]=='[':
						if x not in dic:
							dic[x] = dic.pop('temp')
						else:
							dic[x]=dic[x]+dic["temp"]
						dic["temp"]=[]
					else:
						dic["temp"]=dic["temp"]+[x]
				del(dic["temp"])
				event_channels=[]
				cores=["green","orange","blue","white","peru","gold","pink","red","darkcyan"]
				html_escape_table = {"&amp;": "&",'"': "&quot;","'": "&apos;",">": "&gt;","<": "&lt;"}
				flag=0
				for key in dic:
					for canais in dic[key]:
						for canal in canais.split("-"):
							event_channels.append('[B][COLOR '+cores[0]+']'+"AV"+str(canal) + "[/B][/COLOR] "  + '[B][COLOR yellow]' + str(key) + '[/B][/COLOR]')
							if str(canal)[0]=="S":
								del(cores[0])
								flag=1
						if flag!=1:
							del(cores[0])
						flag=0
				evento=evento.replace("&amp;", "&")
				try: addDir('[B][COLOR red]' + time + '[/B][/COLOR] ' + '[B][COLOR green]' + removeNonAscii(clean(modalidade)) + '[/B][/COLOR] '+ '[B][COLOR yellow]' + removeNonAscii(clean(evento)) + '[/B][/COLOR] '+ removeNonAscii(clean(campeonato)),str(event_channels),401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision",parserfunction="arenavision_chooser")
				except:pass	
		
def arenavision_chooser(url):
	dictionary = eval(url)
	index = xbmcgui.Dialog().select("On...", dictionary)
	if index > -1:
		headers = {
			"Cookie" : "beget=begetok; has_js=1;"
		}
		try:
			source = requests.get(base_url,headers=headers).text
		except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
		if source:
			match = re.compile('leaf"><a href="(.+?)">(.+?)</a').findall(source)
			dictionary[index]=re.sub('\[.*?]','',dictionary[index])
			dictionary[index] = dictionary[index][:-1]
			for link,name in match:
				if (dictionary[index] == name) or (dictionary[index] == name.replace('AV','#')) or (dictionary[index] == name.replace('#','AV')) or (dictionary[index] == name.replace('ArenaVision ','AV')):
					arenavision_streams(name,base_url+link)
					
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))