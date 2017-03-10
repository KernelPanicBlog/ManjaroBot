# -*- coding: utf-8 -*-
import telebot # Library of API bot.
from telebot import types # Types from API bot
import codecs
import sys
from os.path import exists
import os
import token
import user
import feedparser
import owners
import logging
import commands
import subprocess
import requests

TOKEN = token.token_id
bot = telebot.TeleBot(TOKEN) # Creating our bot object.
bot.skip_pending=True

#######################################
#Function for feedparser
#CODE TAKEN FROM:
#https://gist.github.com/Jeshwanth/99cf05f4477ab0161349
def get_feed(url):
    try:
        feed = feedparser.parse(url)
    except:
        return 'Invalid url.'
    y = len(feed[ "items" ])
    y = 5 if y > 5 else y
    if(y < 1):
        return 'Nothing found'
    lines = ['*Feed:*']
    for x in range(y):
        lines.append('- [{}]({})'.format(feed['items'][x]['title'].replace(']', ':').replace('[', '').encode('utf-8'), feed['items'][x]['link']))
    return '\n'.join(lines)
#    for x in range(y):
#        lines.append(
#        u'-&gt <a href="{1}">{0}</a>.'.format(
#        u'' + feed[ "items" ][x][ "title" ],
#        u'' + feed[ "items" ][x][ "link" ]))
#    return u'' + '\n'.join(lines)

#######################################

#Functions
@bot.message_handler(content_types=['new_chat_member'])
def command_new_user(m):
    cid = m.chat.id
    grupo = m.chat.title
    if (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + '!! ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'No tenés nombres, podrías completar los datos. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + '!!' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.last_name) + '!!' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' A ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' a ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + '!! ' + ' a ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')

@bot.message_handler(content_types=['left_chat_member'])
def command_left_user(m):
    cid = m.chat.id
    bot.send_message(cid, '@' + unicode(m.left_chat_member.username) + ' Gracias por pasar!! Bye!! ')

@bot.message_handler(commands=['help'])
def command_ayuda(m):
    cid = m.chat.id
    bot.send_message( cid, "Comandos Disponibles:\n /blog\n /neofeed\n /manjarofeed\n /kdefeed\n /id\n /mirrors\n /keys\n /update\n /orphans\n /listpkg\n /last_update_changes\n /telegram\n /virtualbox\n /youtubedl\n /mpis\n /github\n /about\n /support\n /isos\n /help\n") #

@bot.message_handler(commands=['about'])
def command_about(m):
    cid = m.chat.id
    bot.send_message( cid, 'Acerca de @ManjaroGroupBot: Creado por NeoRanger - www.neositelinux.com')

@bot.message_handler(commands=['id'])
def command_id(m):
    cid = m.chat.id
    username = m.from_user.username
    uid = m.from_user.id
    bot.send_message(cid, "You are: @" + str(username)+ " " + "And your Telegram ID is: " + str(uid))

@bot.message_handler(commands=['support'])
def command_support(m):
    markup = types.InlineKeyboardMarkup()
    itembtnneo = types.InlineKeyboardButton('NeoRanger', url="telegram.me/NeoRanger")
    itembtnblog = types.InlineKeyboardButton('URL Blog', url="http://www.neositelinux.com")
    itembtnrepo = types.InlineKeyboardButton('Repo Github', url="http://github.com/kernelpanicblog/manjarobot")
    markup.row(itembtnneo)
    markup.row(itembtnblog)
    markup.row(itembtnrepo)
    bot.send_message(m.chat.id, "Choose an option:", reply_markup=markup)

@bot.message_handler(commands=['isos'])
def command_isos(m):
    markup = types.InlineKeyboardMarkup()
    xfce32 = types.InlineKeyboardButton('XFCE 32 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-xfce-17.0-stable-i686.iso.torrent")
    xfce64 = types.InlineKeyboardButton('XFCE 64 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-xfce-17.0-stable-x86_64.iso.torrent")
    kde32 = types.InlineKeyboardButton('Plasma 32 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-kde-17.0-stable-i686.iso.torrent")
    kde64 = types.InlineKeyboardButton('Plasma 64 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-kde-17.0-stable-x86_64.iso.torrent")
    net32 = types.InlineKeyboardButton('Net 32 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-net-16.08-i686.iso.torrent")
    net64 = types.InlineKeyboardButton('Net 64 Bits', url="https://downloads.sourceforge.net/manjarotorrents/manjaro-net-16.08-x86_64.iso.torrent")
    markup.row(xfce32)
    markup.row(xfce64)
    markup.row(kde32)
    markup.row(kde64)
    markup.row(net32)
    markup.row(net64)
    bot.send_message(m.chat.id, "Choose an ISO file for download:", reply_markup=markup)


@bot.message_handler(commands=['blog'])
def command_blog(m):
    cid = m.chat.id
    busqueda = 'https://kernelpanicblog.wordpress.com/search/%s/feed/rss'    
    if len(m.text.split()) >= 2:
        palabras = m.text.split()
        palabras.pop(0)
        a_buscar = '+'.join(palabras)
        url = (busqueda % a_buscar)
        bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")
    else:
        bot.send_message( cid, "Missing Argument" )
        
# @bot.message_handler(commands=['wiki'])
# def command_wiki(m):
#     cid = m.chat.id
#     busqueda = 'https://wiki.manjaro.org/index.php?search=%s'
#     if len(m.text.split()) >= 2:
#         palabras = m.text.split()
#         palabras.pop(0)
#         a_buscar = '+'.join(palabras)
#         url = (busqueda % a_buscar)
#         r = requests.head(url)
#         if r.status_code != 200:
#             return bot.send_message( cid, "Missing Argument" )
#         else:
#             return bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['feed'])
def command_feed(m):
    cid = m.chat.id
    url = str(m.text).split(None,1)
    try:
        print (url)
        bot.send_message(cid, get_feed(url[1]),disable_web_page_preview=True,parse_mode="markdown")
    except IndexError:
        bot.send_message( cid, "Missing Argument - Example: /feed http://www.example.com" )

@bot.message_handler(commands=['neofeed'])
def neo_feed(m):
    cid = m.chat.id
    url = str("https://neositelinux.com/feed/")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")
    
@bot.message_handler(commands=['kdefeed'])
def kde_feed(m):
    cid = m.chat.id
    url = str("https://www.kdeblog.com/feed/")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['manjarofeed'])
def manjaro_feed(m):
    cid = m.chat.id
    url = str("https://manjaro.org/feed/")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['mirrors'])
def command_mirrors(m):
    cid = m.chat.id
    mensaje = '''
Para tener los mirrors actualizados y poder elegir los mejores hay que usar el siguiente comando:
`sudo pacman-mirrors -g`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['keys'])
def command_keys(m):
    cid = m.chat.id
    mensaje = '''
Para refrescar las llaves necesarias (como root):
`# pacman-key --init`
`# pacman-key --populate archlinux manjaro`
`# pacman-key --refresh-keys`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['update'])
def command_update(m):
    cid = m.chat.id
    mensaje = '''
Pasos para la actualización completa del sistema (como root):
`# pacman -Sy`   (Sincroniza solo Base de Datos)
`# pacman -Syu`  (Sincronización forzosa solo de Base de Datos)
`# pacman -Syyu` (Sincronización forzosa y actualización de paquetes)
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")
    
@bot.message_handler(commands=['orphans'])
def command_huerfanos(m):
    cid = m.chat.id
    mensaje = '''
Para consultar si hay huerfanos usar:
`$ pacman -Qdtq`
Si desea remover los paquetes huerfanos puede usar:
`sudo pacman -Rsn $(pacman -Qdtq)`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")


@bot.message_handler(commands=['youtubedl'])
def command_youtubedl(m):
    cid = m.chat.id
    mensaje = '''
Uso de #youtube-dl
Para buscar todos los formatos disponibles del vídeo:
`youtube-dl -F URL`

Para descargar el formato elegido del vídeo:
`youtube-dl -f ID URL`

Para descargar el vídeo con subtitulos (descargara todos los subtitulos existentes):
`youtube-dl -f ID --write-sub --all-subs URL`

Para Descargar solo los subtitulos del vídeo (descargara todos los subtitulos existentes):
`youtube-dl --all-subs --skip-download URL`
'''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")
    
@bot.message_handler(commands=['basic_commands'])
def command_basic(m):
    cid = m.chat.id
    mensaje = '''
Comandos basicos para el manejo del sistema (como root):

#Instalar paquetes
`pacman -S “paquete”`  #Instala un paquete.
`pacman -Sy “paquete”` #Sincroniza repositorios e instala el paquete.
 
# Actualizar paquetes
`pacman -Sy`   #Sincroniza repositorios.
`pacman -Syy`  #Fuerza la sincronización de repositorios incluso para paquetes que parecen actualizados.
`pacman -Syu`  #Sincroniza repositorios y actualiza paquetes.
`pacman -Syyu` #Fuerza sincronización y actualiza paquetes.
`pacman -Su`   #Actualiza paquetes sin sincronizar repositorios.
 
# Buscar paquetes
`pacman -Ss “paquete”` #Busca un paquete.
`pacman -Si “paquete”` #Muestra información detallada de un paquete.
`pacman -Sg “grupo”`   #Lista los paquetes que pertenecen a un grupo.
`pacman -Qs “paquete”` #Busca un paquete YA instalado.
`pacman -Qi “paquete”` #Muestra información detallada de un paquete YA instalado.
`pacman -Qdt`          #Muestra paquetes huerfanos.
 
# Eliminar paquetes
`pacman -R “paquete”`  #Borra paquete sin sus dependencias.
`pacman -Rs “paquete”` #Borra paquete y sus dependencias no utilizadas.
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['blogfeed'])
def blog_feed(m):
    cid = m.chat.id
    url = str("https://kernelpanicblog.wordpress.com/feed/")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['mpis'])
def command_mpis(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtnmpis = types.InlineKeyboardButton('Blog', url="http://kernelpanicblog.wordpress.com")
    markup.row(itembtnmpis)
    bot.send_message(m.chat.id, 'MPIS Manjaro Post Installation Script es una herramienta desarrollada por algunos usuarios de este grupo, cuyo objetivo es brindar una utilidad y apoyo a un usuario novel como experto, permitiendo automatizar algunas tareas tediosas o consecutivas puedes instalarla en tu Manjaro con el comando [yaourt -S mpis --noconfirm]. Algun comentario o sugerencia puedes hacerla en el grupo.',reply_markup=markup)

@bot.message_handler(commands=['github'])
def command_github(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtngit = types.InlineKeyboardButton('Repo Github', url="http://github.com/kernelpanicblog/mpis")
    markup.row(itembtngit)
    bot.send_message(m.chat.id, 'Contamos con el repositorio del Grupo en GITHUB donde puedes colaborar y ayudar a mejorarme o aportar con /MPIS',reply_markup=markup)
    
@bot.message_handler(commands=['virtualbox'])
def command_virtualbox(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtnvbox = types.InlineKeyboardButton('Solución', url="http://telegra.ph/Instalaci%C3%B3n-de-VirtualBox-02-09")
    markup.row(itembtnvbox)
    bot.send_message(m.chat.id, 'Como instalar VirtualBox en Arch-Manjaro-Antergos',reply_markup=markup)
    
@bot.message_handler(commands=['listpkg'])
def command_listpkg(m):
    cid = m.chat.id
    mensaje = '''
Para listar los paquetes instalados omitiendo los de
base y base-devel, copia y pega éste comando en una terminal:
`pacman -Qei | awk '/^Nombre/ { name=$3 } /^Grupos/ { if ( $3 != "base" && $3 != "base-devel" ) { print name } }'`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")
    
@bot.message_handler(commands=['last_update_changes'])
def command_last_changes(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtnchanges = types.InlineKeyboardButton('Ir al Documento', url="https://gist.github.com/philmmanjaro/7982edda35d9a38cd31f6912c25a0cb1")
    markup.row(itembtnchanges)
    bot.send_message(m.chat.id, 'Ver los cambios en la ultima update',reply_markup=markup)
    
@bot.message_handler(commands=['telegram'])
def command_telegram(m):
    cid = m.chat.id
    mensaje = '''
Como instalar Telegram desde la web oficial:

1a) `wget https://telegram.org/dl/desktop/linux (64 Bits)`
1b) `wget https://telegram.org/dl/desktop/linux32 (32 Bits)`
2) `tar -xvf linux`
3a) `mkdir /home/USUARIO/.TelegramDesktop`
3b) `mv Telegram\ Desktop /home/USUARIO/.TelegramDesktop`
4) `./Telegram`
5) Se cierra la aplicación desde Quit Telegram y se ejecuta normalmente
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

###############################################################################
#Specials functions
def send_message_checking_permission(m, response):
    cid = m.chat.id
    uid = m.from_user.id
    if uid != user.user_id:
        bot.send_message(cid, "You can't use the bot")
        return
    bot.send_message(cid, response)

###############################################################################
print('Functions loaded')
