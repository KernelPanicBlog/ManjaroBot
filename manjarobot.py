# -*- coding: utf-8 -*-
import functions
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Listener
def printUser(msg): #debug function (will print every message sent by any user to the console)
	print str(msg.chat.first_name) + " [" + str(msg.chat.id) + "]: " + msg.text

def listener(messages):
	for m in messages:
		cid = m.chat.id
		if m.content_type == 'text':
			text = m.text
			printUser(m) #print the sent message to the console

functions.bot.set_update_listener(listener)

#############################################
#Bot starts here                            #
#############################################
print('Bot Started')
print('Please visite kernelpanicblog.wordpress.com')
functions.bot.polling(none_stop=True)
