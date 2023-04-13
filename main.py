from cProfile import run
import pstats
from techdev.utils import sizeof_fmt,get_file_size,createID,nice_time
from techdev.client import TechDevClient,inlineQueryResultArticle
from techdev.client import inlineKeyboardMarkup,inlineKeyboardMarkupArray,inlineKeyboardButton
from JDatabase import JsonDatabase
import zipfile
import os
import infos
import datetime
import time
from pydownloader.downloader import Downloader
import socket
import S5Crypto
import asyncio
import aiohttp
import requests
from yarl import URL
import re
import random
from bs4 import BeautifulSoup
import S5Crypto
import pyrogram
from os.path import exists

listproxy = []

class WebAppUpload:
	def __init__(self, username, password, host, repo):
		self.username = username
		self.password = password
		self.host = host
		self.repo = repo
	def upload(self, path, proxy):
		upload = requests.session()
		var = 1
		while var == 1:
			try:
				token1 = upload.get(self.host+'/login',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},proxies=dict(http=proxy,https=proxy))
			except:
				token1 = upload.get(self.host+'/login',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},proxies=dict(http=proxy,https=proxy))
			else:
				var = 0
		token2 = BeautifulSoup(token1.text,"html.parser")
		token = token2.find('input',attrs={"name":"csrfToken"})["value"]
		logIn = upload.post(self.host+'/login/signIn', params={'csrfToken':token, 'password':self.password, 'remember':1,'source':'','username':self.username},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}, proxies=dict(http=proxy,https=proxy))
		if 'Salir' in logIn.text:
			token1 = upload.get(self.host+'/submission/wizard/2?submissionId='+str(self.repo)+'#step-2',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}, proxies=dict(http=proxy,https=proxy))
			token = token1.text.split('"csrfToken":"')[1].split('"')[0]
			precarga = upload.get(self.host+'/submission/wizard/2?submissionId='+str(self.repo), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36","X-Csrf-Token":token}, proxies=dict(http=proxy,https=proxy))
			fileUpload = upload.post(self.host+'/api/v1/submissions/'+str(self.repo)+'/files', data={'fileStage':'2','name[es_ES]':path,'name[en_US]':path},  files={'file':open(path,'rb')},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36","X-Csrf-Token":token}, proxies=dict(http=proxy,https=proxy))
			FileID = str(fileUpload.text.split('_href":"')[1].split('"')[0]).replace(str('\/'), '/').split('/')[-1]
			link = 'https://anuarioeco.uo.edu.cu/index.php/aeco/$$$call$$$/api/file/file-api/download-file?submissionFileId='+FileID+'&submissionId=5329&stageId=1'
			return link

def sign_url(token: str, url: URL):
    query: dict = dict(url.query)
    query["token"] = token
    path = "webservice" + url.path
    return url.with_path(path).with_query(query)

def nameRamdom():
    populaton = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    name = "".join(random.sample(populaton,10))
    return name

def downloadFile(downloader,filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        thread = args[2]
        if thread.getStore('stop'):
            downloader.stop()
        downloadingInfo = infos.createDownloading(filename,totalBits,currentBits,speed,time,tid=thread.id)
        reply_markup = inlineKeyboardMarkup(
            r1=[]
        )
        bot.editMessageText(message,downloadingInfo,reply_markup=reply_markup)
    except Exception as ex: print(str(ex))
    pass

def uploadFile(filename,update, bot, message, thread=None, proxy=""):
    app = WebAppUpload('techdev', '@A1a2a3mo', 'https://anuarioeco.uo.edu.cu/index.php/aeco', 5329)
    if exists(str(message.chat.id)+'proxy'):
    	proxy = open(str(message.chat.id)+'proxy', 'r').read()
    else:
    	proxy = ''
    UploadFile = app.upload(filename, proxy)
    reply_markup = inlineKeyboardMarkup(r1=[inlineKeyboardButton("Descargar", url=UploadFile)])
    bot.editMessageText(message,filename,reply_markup=reply_markup)
    os.unlink(filename)
def uploadFileZip(filename, update, bot, message, thread, proxy=""):
	app = WebAppUpload('techdev', '@A1a2a3mo', 'https://anuarioeco.uo.edu.cu/index.php/aeco', 5329)
	if exists(str(update.message.chat.id)+'proxy'):
	   proxy = open(str(update.message.chat.id)+'proxy', 'r').read()
	else:
		proxy = ''
	UploadFile = app.upload(filename, proxy)
	reply_markup = inlineKeyboardMarkup(r1=[inlineKeyboardButton("Descargar", url=UploadFile)])
	bot.sendMessage(update.message.chat.id,filename,reply_markup=reply_markup)
	return UploadFile
	os.unlink(filename)
def processUploadFiles(filename,filesize,files,update,bot,message,thread=None,jdb=None):
        err = None
        bot.editMessageText(message,'Subiendo...')
        if exists(str(update.message.chat.id)+"proxy"):
        	proxy = open(str(update.message.chat.id)+"proxy","r")
        	uploadFile(filename, update, bot, message, thread, proxy=proxy.read())
        else:
        	uploadFile(filename, update, bot, message, thread, proxy='')
        
def processUploadFilesZip(filename,filesize,files,update,bot,message,thread=None,jdb=None):
        err = None
        bot.editMessageText(message,'Subiendo '+filename)
        if exists(str(update.message.chat.id)+"proxy"):
        	proxy = open(str(update.message.chat.id)+"proxy","r")
        	return uploadFileZip(filename, update, bot, message, thread, proxy=proxy.read())
        else:
        	return uploadFileZip(filename, update, bot, message, thread, proxy=proxy.read())
        	

def processFile(update,bot,message,file,thread=None,jdb=None):
    user_info = jdb.get_user(update.message.sender.username)
    name =''
    if user_info['rename'] == 1:
        ext = file.split('.')[-1]
        if '7z.' in file:
            ext1 = file.split('.')[-2]
            ext2 = file.split('.')[-1]
            name = nameRamdom() + '.'+ext1+'.'+ext2
        else:
            name = nameRamdom() + '.'+ext
    else:
        name = file
    os.rename(file,name)
    file_size = get_file_size(name)
    getUser = jdb.get_user(update.message.sender.username)
    max_file_size = 1024 * 1024 * getUser['zips']
    file_upload_count = 0
    client = None
    findex = 0
    if file_size > max_file_size:
        compresingInfo = infos.createCompresing(name,file_size,max_file_size)
        bot.editMessageText(message,compresingInfo)
        zipname = str(name).split('.')[0] + createID()
        mult_file = zipfile.MultiFile(zipname,max_file_size)
        zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(name)
        zip.close()
        mult_file.close()
        bot.editMessageText(message, zipname+":")
        current = 1
        txt = ''
        while exists(zipname+".7z.00"+str(current)):
        	name = zipname+".7z.00"+str(current)
        	url = processUploadFilesZip(name,file_size,[name],update,bot,message,jdb=jdb)
        	if not exists(name.split(".")[0]+'.txt'):
        		txtfile = open(name.split(".")[0]+'.txt','w')
        		txtfile.write('')
        		txtfile.close()
        	txtfile = open(name.split(".")[0]+'.txt','r')
        	txt = txtfile.read()
        	txtfile = open(name.split(".")[0]+'.txt','w')
        	txtfile.write(txt+'\n'+url)
        	txtfile.close()
        	current += 1
        bot.sendFile(update.message.chat.id, name.split(".")[0]+'.txt')
        try:
            os.unlink(name)
        except:pass
        file_upload_count = len(zipfile.files)
    else:
        processUploadFiles(name,file_size,[name],update,bot,message,jdb=jdb)
        file_upload_count = 1
    evidname = ''
    files = []

def ddl(update,bot,message,url,file_name='',thread=None,jdb=None):
    downloader = Downloader()
    file = downloader.download_url(url,progressfunc=downloadFile,args=(bot,message,thread))
    if not downloader.stoping:
        if file:
            processFile(update,bot,message,file,jdb=jdb)

def sendTxt(name,files,update,bot):
                txt = open(name,'w')
                fi = 0
                for f in files:
                    separator = ''
                    if fi < len(files)-1:
                        separator += '\n'
                    txt.write(f['directurl']+separator)
                    fi += 1
                txt.close()
                bot.sendFile(update.message.chat.id,name)
                os.unlink(name)

def onmessage(update,bot:TechDevClient):
        thread = bot.this_thread
        username = update.message.sender.username
        tl_admin_user = os.environ.get('tl_admin_user')

        #set in debug
        tl_admin_user = 'JAGB2021'

        jdb = JsonDatabase('database')
        jdb.check_create()
        jdb.load()

        user_info = jdb.get_user(username)
        #if username == tl_admin_user or user_info:
        if username in str(tl_admin_user).split(';') or user_info or tl_admin_user=='*':  # validate user
            if user_info is None:
                #if username == tl_admin_user:
                if username == tl_admin_user:
                    jdb.create_admin(username)
                else:
                    jdb.create_user(username)
                user_info = jdb.get_user(username)
                jdb.save()
        else:
            mensaje = "🚷 No tienes Acceso 🚷"
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('⚙Contactar Soporte⚙',url='https://t.me/tech_dev_ortiz')]
            )
            bot.sendMessage(update.message.chat.id,mensaje,reply_markup=reply_markup)
            return


        msgText = ''
        msgText = update.message.text

        # comandos de admin
        if '/adduser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_user(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora tiene acceso al bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addadmin' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_admin(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora es Admin del bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addproxy' in msgText:
            isadmin = jdb.is_admin(username)
            global listproxy
            if isadmin:
                try:
                    proxy = str(msgText).split(' ')[1]
                    listproxy.append(proxy)
                    zize = len(listproxy)-1
                    bot.sendMessage(update.message.chat.id,f'Proxy Registrado en la Posicion {zize}')
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /addproxy proxy❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/checkproxy' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    msg = 'Proxis Registrados\n'
                    cont = 0
                    for proxy in listproxy:
                        msg += str(cont) +'--'+proxy+'\n'
                        cont +=1
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /checkproxy❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/banuser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    if user == username:
                        bot.sendMessage(update.message.chat.id,'❌No Se Puede Banear Usted❌')
                        return
                    jdb.remove(user)
                    jdb.save()
                    msg = '🦶Fuera @'+user+' Baneado❌'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/getdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                bot.sendMessage(update.message.chat.id,'Base De Datos👇')
                bot.sendFile(update.message.chat.id,'database.jdb')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        # end

        # comandos de usuario
        if '/setproxy' in msgText:
            getUser = user_info
            if getUser:
                try:
                   pos = int(str(msgText).split(' ')[1])
                   proxy = str(listproxy[pos])
                   getUser['proxy'] = proxy
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = 'Su Proxy esta Listo'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /setproxy pos❌')
                return
        if '/zips' in msgText:
            if int(str(msgText).split(' ')[1]) > 500:
            	msgText = '/zips 500'
            getUser = user_info
            if getUser:
                   size = int(str(msgText).split(' ')[1])
                   getUser['zips'] = size
                   zips = open(str(update.message.chat.id)+"zips","w")
                   zips.write(str(msgText).split(' ')[1])
                   zips.close()
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial los zips seran de '+ sizeof_fmt(size*1024*1024)+' las partes👍'
                   bot.sendMessage(update.message.chat.id,msg)
                   return
        if '/proxy' in msgText:
            proxy = msgText.split(" ")
            file = open(str(update.message.chat.id)+"proxy","w")
            file.write(proxy[1])
            bot.sendMessage(update.message.chat.id,'Proxy establecido')
            return
        if '/decrypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Proxy decryptado:\n{proxy_de}')
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'⏳Procesando...')

        thread.store('msg',message)

        if '/start' in msgText:
            if not exists(str(update.message.chat.id)+'proxy'):
            	proxy = open(str(update.message.chat.id)+'proxy','w')
            	proxy.write("")
            	proxy.close()
            if not exists(str(update.message.chat.id)+'zips'):
            	zips = open(str(update.message.chat.id)+'zips','w')
            	zips.write("500")
            	zips.close()
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('techdev', url='https://t.me/techdev_pro')]
            )
            proxy = open(str(update.message.chat.id)+'proxy', 'r')
            if proxy.read() == '':
            	proxys = "No"
            else:
            	proxys = 'Si'
            	proxy.close()
            zips = open(str(update.message.chat.id)+'zips', 'r')
            dashboard = '<i>WebApp</i> ~ <b>DashBoard</b> \n\n <b>Proxy:</b> <i>'+proxys+'</i>\n\n <b>Zips:</b> <i>'+zips.read()+'</i> <b>MB</b>'
            bot.editMessageText(message,dashboard,parse_mode='html',reply_markup=reply_markup)
        elif 'http' in msgText:
            url = msgText
            proxy = open(str(update.message.chat.id)+"proxy",'r')
            ddl(update,bot,message,url,file_name='',thread=thread,jdb=jdb)
        elif '/delproxy' in msgText:
        	proxy = open(str(update.message.chat.id)+'proxy','w')
        	proxy.write('')
        	bot.editMessageText(message,'Proxy eliminado')
        elif '/usertemp' in msgText:
        	if username == 'tech_dev_ortiz':
        		usertemp = msgText.split(' ')[1]
        		jdb = JsonDatabase('database')
        		jdb.check_create()
        		jdb.load()
        		jdb.create_user(usertemp)
        		print("Usuario "+usertemp+" creado")
        		jdb.save()
        		bot.editMessageTextMessage(message, 'Usuario @'+usertemp+' añadido')
        	else:
        		bot.editMessageText(message, 'No tiene permiso')
        else:
            bot.editMessageText(message,"No se pudo procesar")
            
users = "JAGB2021 Chris_bel14 Leroy1712 User7503Dev anonedev CarlosCampillo JennPMoon alejandromiguelortiz JavierAlonso0526 Gisy2111 christian18sarmiento luisernesto95 Marquez_tg none"
def main():
    bot_token = os.environ.get('bot_token')
    print('BOT INICIADO')
    montado = '5947045568:AAE0mfkt85dPRAYIKGBEFdHd4qG4U3Y4bAA'
    prueba = ''
    bot_token = montado
    bot = TechDevClient(bot_token)
    bot.onMessage(onmessage)
    userdate = users.split(" ")
    usernum = len(userdate) - 1
    usercalc = 0
    while usercalc != usernum:
    	jdb = JsonDatabase('database')
    	jdb.check_create()
    	jdb.load()
    	jdb.create_user(userdate[usercalc])
    	print("Usuario "+userdate[usercalc]+" creado")
    	jdb.save()
    	usercalc += 1
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()
