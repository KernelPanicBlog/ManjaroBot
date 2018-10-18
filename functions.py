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
@bot.message_handler(content_types=['new_chat_members'])
def command_new_user(m):
    cid = m.chat.id
    grupo = m.chat.title
    uid = m.from_user.id
    
#    name = m.new_chat_members.first_name
#    check_name = name.find("VX.QQ")
#    check_name2 = name.find("[VX.QQ")

#    if (len(m.new_chat_members.first_name) > 30): #Filtro AntiSpam 1
#	bot.kick_chat_member(cid,uid)
#	bot.delete_message(cid)
#    elif (check_name == 0): #Filtro AntiSpam 2 (temporal)
#        bot.kick_chat_member(cid,uid)
#        bot.delete_message(cid)
#    elif (check_name2 == 0): #Filtro AntiSpam 3 (temporal)
#        bot.kick_chat_member(cid,uid)
#        bot.delete_message(cid)
#    else:
    if (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, u"Bienvenido {0} {1} !! A.K.A. @{2} a {3}. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.first_name, m.new_chat_member.last_name, m.new_chat_member.username, grupo))
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name == None):
        bot.send_message(cid, u"Bienvenido!! @{0} a {1}. No tenés nombres, podrías completar los datos. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.username, grupo))
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, u"Bienvenido {0} A.K.A. @{1} a {2}. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.first_name,m.new_chat_member.username, grupo))
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, u"Bienvenido {0}!! A.K.A. @{1} a {2}. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.last_name,m.new_chat_member.username, grupo))
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, u"Bienvenido {0} {1} a {2}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.first_name,m.new_chat_member.last_name,grupo))
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, u"Bienvenido {0}!! a {1}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.last_name, grupo))
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, u"Bienvenido {0} a {1}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.".format(m.new_chat_member.first_name, grupo))

#@bot.message_handler(content_types=['left_chat_member'])
#def command_left_user(m):
#    cid = m.chat.id
#    bot.send_message(cid, u"@{0} Gracias por pasar!! Bye!!".format(left_chat_member.username))

# Elimina al usuario que manda el mensaje en el chat en que se ha enviado
#def kickFromMessage(m):
#  bot.kickChatMember(m.chat.id, m.from_user.id)

@bot.message_handler(commands=['help'])
def command_ayuda(m):
    cid = m.chat.id
    bot.send_message( cid, u"Comandos Disponibles:\n /blog\n /neofeed\n /manjarofeed\n /kdefeed\n /id\n /mirrors\n /keys\n /update\n /orphans\n /listpkg\n /aurman\n /yay_install\n /manjaro_uefi\n /dd\ /last_update_changes\n /telegram\n /virtualbox\n /youtubedl\n /blackscreen\n /firefoxmaia\n /steam\n /command_line_tutorial\n /mpis\n /github\n /about\n /support\n /isos\n /help\n") #

@bot.message_handler(commands=['about'])
def command_about(m):
    cid = m.chat.id
    bot.send_message( cid, u'Acerca de @ManjaroGroupBot: Creado por NeoRanger - www.neositelinux.com')

@bot.message_handler(commands=['id'])
def command_id(m):
    cid = m.chat.id
    username = m.from_user.username
    uid = m.from_user.id
    bot.send_message(cid, u"You are: @" + str(username)+ " " + "And your Telegram ID is: " + str(uid))

@bot.message_handler(commands=['support'])
def command_support(m):
    markup = types.InlineKeyboardMarkup()
    itembtnneo = types.InlineKeyboardButton('NeoRanger', url="telegram.me/NeoRanger")
    itembtnblog = types.InlineKeyboardButton('URL Blog', url="https://www.neositelinux.com")
    itembtnrepo = types.InlineKeyboardButton('Repo Github', url="http://github.com/kernelpanicblog/manjarobot")
    markup.row(itembtnneo)
    markup.row(itembtnblog)
    markup.row(itembtnrepo)
    bot.send_message(m.chat.id, "Choose an option:", reply_markup=markup)

@bot.message_handler(commands=['isos'])
def command_isos(m):
    markup = types.InlineKeyboardMarkup()
    xfce64 = types.InlineKeyboardButton('XFCE 64 Bits', url="https://osdn.net/dl/manjaro/manjaro-xfce-17.1.12-stable-x86_64.iso.torrent")
    kde64 = types.InlineKeyboardButton('Plasma 64 Bits', url="https://osdn.net/dl/manjaro/manjaro-kde-17.1.12-stable-x86_64.iso.torrent")
    gnome64 = types.InlineKeyboardButton('Gnome 64 Bits', url="https://osdn.net/dl/manjaro/manjaro-gnome-17.1.12-stable-x86_64.iso.torrent")
    net64 = types.InlineKeyboardButton('Manjaro-Architect 64 Bits', url="https://osdn.net/dl/manjaro/manjaro-architect-17.1.11-stable-x86_64.iso.torrent")
    markup.row(xfce64)
    markup.row(kde64)
    markup.row(gnome64)
    markup.row(net64)
    bot.send_message(m.chat.id, "Choose an ISO file for download - 32bits are deprecated:", reply_markup=markup)


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
        bot.send_message( cid, "Falta un argumento - Ejemplo: /feed http://www.example.com" )

@bot.message_handler(commands=['neofeed'])
def neo_feed(m):
    cid = m.chat.id
    url = str("https://neositelinux.com/feed.xml")
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
`$ sudo pacman-mirrors -f`
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
`$ sudo pacman -Rsn $(pacman -Qdtq)`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")


@bot.message_handler(commands=['youtubedl'])
def command_youtubedl(m):
    cid = m.chat.id
    mensaje = '''
Uso de `youtube-dl`
Para buscar todos los formatos disponibles del vídeo:
`$ youtube-dl -F URL`

Para descargar el formato elegido del vídeo:
`$ youtube-dl -f ID URL`

Para descargar el vídeo con subtitulos (descargara todos los subtitulos existentes):
`$ youtube-dl -f ID --write-sub --all-subs URL`

Para Descargar solo los subtitulos del vídeo (descargara todos los subtitulos existentes):
`$ youtube-dl --all-subs --skip-download URL`
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
`# pacman -Sy`   #Sincroniza repositorios.
`# pacman -Syy`  #Fuerza la sincronización de repositorios incluso para paquetes que parecen actualizados.
`# pacman -Syu`  #Sincroniza repositorios y actualiza paquetes.
`# pacman -Syyu` #Fuerza sincronización y actualiza paquetes.
`# pacman -Su`   #Actualiza paquetes sin sincronizar repositorios.

# Buscar paquetes
`# pacman -Ss “paquete”` #Busca un paquete.
`# pacman -Si “paquete”` #Muestra información detallada de un paquete.
`# pacman -Sg “grupo”`   #Lista los paquetes que pertenecen a un grupo.
`# pacman -Qs “paquete”` #Busca un paquete YA instalado.
`# pacman -Qi “paquete”` #Muestra información detallada de un paquete YA instalado.
`# pacman -Qdt`          #Muestra paquetes huerfanos.

# Eliminar paquetes
`# pacman -R “paquete”`  #Borra paquete sin sus dependencias.
`# pacman -Rs “paquete”` #Borra paquete y sus dependencias no utilizadas.
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
    mensaje = '''
MPIS: Manjaro Post Installation Script es una herramienta desarrollada por 
algunos usuarios de este grupo, cuyo objetivo es brindar una utilidad y 
apoyo a un usuario novel como experto, permitiendo automatizar algunas 
tareas tediosas o consecutivas puedes instalarla en tu Manjaro con el 
comando `aurman -S mpis --noconfirm` . 
NOTA: Usá el helper que más se adapta a vos porque yaourt está
discontinuado, nosotros preferimos aurman.
Algun comentario o sugerencia puedes hacerla en el grupo.
'''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['github'])
def command_github(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtngit = types.InlineKeyboardButton('Repo Github', url="http://github.com/kernelpanicblog/mpis")
    markup.row(itembtngit)
    bot.send_message(m.chat.id, 'Contamos con el repositorio del Grupo en GITHUB donde puedes colaborar y ayudar a mejorar o aportar con /MPIS',reply_markup=markup)

@bot.message_handler(commands=['virtualbox'])
def command_virtualbox(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtnvbox = types.InlineKeyboardButton('Solución', url="http://telegra.ph/Instalacion-de-VirtualBox-en-Manjaro-07-21")
    markup.row(itembtnvbox)
    bot.send_message(m.chat.id, 'Como instalar VirtualBox en Arch-Manjaro-Antergos',reply_markup=markup)

@bot.message_handler(commands=['listpkg'])
def command_listpkg(m):
    cid = m.chat.id
    mensaje = '''
Para listar los paquetes instalados omitiendo los de
base y base-devel, copia y pega éste comando en una terminal:
`$ pacman -Qei | awk '/^Nombre/ { name=$3 } /^Grupos/ { if ( $3 != "base" && $3 != "base-devel" ) { print name } }'`
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
**Como instalar Telegram desde la web oficial:**

1a. `$ wget https://telegram.org/dl/desktop/linux` (64 Bits)
1b. `$ wget https://telegram.org/dl/desktop/linux32` (32 Bits)
2. `$ tar -xvf linux`
3. `$ mv Telegram  home/USUARIO/.local/share/applications`
4. `$ cd home/USUARIO/.local/share/applications/Telegram`
4a. `$ ./Telegram`
5. Se cierra la aplicación desde Quit Telegram y se ejecuta normalmente. Esto es para que se genere el ícono correctamente en el menú.

**Instalación desde los repositorios de Manjaro:**
`sudo pacman -S telegram-desktop`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['blackscreen'])
def command_blackscreen(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtnblckscr = types.InlineKeyboardButton('Solución', url="http://telegra.ph/Pantalla-negra-al-iniciar-Manjaro-04-05")
    markup.row(itembtnblckscr)
    bot.send_message(m.chat.id, 'Solución a la pantalla negra en logueo del sistema.',reply_markup=markup)

#@bot.message_handler(commands=['reset'])
#def command_reset(m):
#    cid = m.chat.id
#    mensaje = '''
#Volver Manjaro a su configuración original(usar bajo tu propio riesgo):
#`$ sudo pacman -R $(comm -23 <(pacman -Qq | sort) <((for i in $(pacman -Qqg base); do pactree -ul "$i"; done) | sort -u))`
#Esto borra todo a excepción del sistema base.
#        '''
#    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['aur_manual'])
def command_aurmanual(m):
    cid = m.chat.id
    mensaje = '''
Instalación Manual de paquetes del AUR, como se hacía antes de los aur helpers(yaourt, pacaur, etc), por si tienen problemas con alguno.
https://wiki.archlinux.org/index.php/Arch_User_Repository

Descarga del snapshot desde aur por web browser o asi por consola (tambien se puede clonar el git en su lugar)
`$ curl -L -O https://aur.archlinux.org/cgit/aur.git/snapshot/package_name.tar.gz`
`$ tar -xvf package_name.tar.gz`
`$ cd package_name`
Si Se quiere verificar el PKGBUILD y el install para evitar sorpresas:
`$ less PKGBUILD`
`$ less package_name.install`
Instalación con dependencias, recomendado ver ayuda del comando para otras opciones.
`$ makepkg -si`
Al finalizar se pueden eliminar los archivos.
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['firefoxmaia'])
def command_firefoxmaia(m):
    cid = m.chat.id
    mensaje = '''
Por defecto Manjaro posee un tema gráfico que lo integra al tema propio Maia. Logran un buen trabajo pero se debe remover si se desea cambiar el tema y mantener la uniformidad.
`$ rm -rf ~/.mozilla/firefox/*.default/chrome/*`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")


@bot.message_handler(commands=['steam'])
def command_steam(m):
    cid = m.chat.id
    mensaje = '''
Para solucionar problemas con Steam:
`$ sudo pacman -S steam-manjaro`
`$ steam_install_workaround`
`$ steam`
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['manjaro_uefi'])
def command_manjaro_uefi(m):
    cid = m.chat.id
    bot.send_message( cid, 'https://www.youtube.com/watch?v=QDOsILoHn7Q&')

@bot.message_handler(commands=['command_line_tutorial'])
def command_line_tutorial(m):
    cid = m.chat.id
    bot.send_message( cid, 'https://www.youtube.com/playlist?list=PLS1QulWo1RIb9WVQGJ_vh-RQusbZgO_As')

@bot.message_handler(commands=['dd'])
def command_dd(m):
    cid = m.chat.id
    mensaje = '''
Lo que tenés que hacer es ir a la terminal:
1) `sudo fdisk -l`

 Ahí tenés que ver cuál es el pendrive donde lo querés instalar.
 Ejemplo: /dev/sdb

2) Usando el comando dd (data duplicator):
 `sudo dd if=/home/$USER/Escritorio/distro_gnu_linux.iso of=/dev/sdb bs=4M status=progress`
 
  **ASUMIENDO QUE LA IMAGEN ESTÁ EN EL ESCRITORIO**, si no cambialo por la ruta donde lo tengas, al igual que el nombre de la iso.

 **CUIDADO: SI NO PONÉS BIEN EL DESTINO, en éste caso /dev/sdb, NO VA A DUDAR EN DESTRUIR LA INFO QUE TENGAS AHÍ.**
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")


@bot.message_handler(commands=['aurman'])
def command_aurman(m):
    cid = m.chat.id
    mensaje = '''
Para instalar aurman:

(ejecuta los comandos que necesites uno tras otro y si tienes alguna duda manda foto con el problema respondiendo a este mensaje)

Si aún tienes yaourt instalado puedes hacer esto ahora o al finalizar la instalación:

`sudo pacman -Rns yaourt --noconfirm`

Ahora a instalar aurman:

`gpg --recv-keys 4C3CE98F9579981C21CA1EC3465022E743D71E39`

`git clone https://aur.archlinux.org/aurman.git` (chequear el directorio donde estás)

`cd aurman`

`makepkg -si`

Al acabar se quedará una carpeta llamada aurman en tu home o en la carpeta donde estuviera trabajando la terminal que abriste, puedes borrar esa carpeta

#aurman #yaourt #instalar #desinstalar #pacman #aur

Colaboración de @Jinkros
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")


@bot.message_handler(commands=['yay_install'])
def command_keys(m):
    cid = m.chat.id
    mensaje = '''
Como instalar yay en Manjaro (AUR Helper):

Primera opción (ultima versión):

1. `$ git clone https://aur.archlinux.org/yay.git`
2. `$ cd yay`
3. `$ makepkg -si`

Segunda opción (repo oficial de Manjaro versión menos actualizada):

1. `$ sudo pacman -S yay`

Si quieres que yay tenga colores, hay que habilitar la funcion en pacman descomentando la linea **Color** en `/etc/pacman.conf`

#pacman #aur #aurhelper #helper #yay

Colaboración de @rirschach
        '''
    bot.send_message( cid, mensaje,disable_web_page_preview=True,parse_mode="markdown")

###############################################################################
#Specials functions
def send_message_checking_permission(m, response):
    cid = m.chat.id
    uid = m.from_user.id
    if uid != user.user_id:
        bot.send_message(cid, "You don't have permissions for use this bot")
        return
    bot.send_message(cid, response)

###############################################################################
print('Functions loaded')
