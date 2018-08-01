# -*- coding: utf-8 -*-
import functions

#Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        title = 'm.chat.title'
        if m.content_type == 'text':
            print (("[" + title.encode("utf-8") + "]: " + m.text))
        if m.content_type == "new_chat_members":
            if len(new_chat_member.first_name) > 30:
               bot.kick_chat_member(m.chat.id, new_chat_member.id)

functions.bot.set_update_listener(listener)

#############################################
#Bot starts here
print('Bot Started')
print('Please visite kernelpanicblog.wordpress.com')
functions.bot.polling(none_stop=True)
