#!/bin/bash
while true
do
python2 /home/pi/Documents/git/ManjaroBot/manjarobot.py
echo "¡The bot is crashed!"
#echo "ManjaroBot is crashed" | mail -s "Aviso" elgranpote@gmail.com
echo "Rebooting in:"
for i in 1
do
echo "$i..."
done
echo "###########################################"
echo "#Bot is restarting now                    #"
echo "###########################################"
done

#while true
#do
#output=`python2 /home/pi/Documents/git/ManjaroBot/manjarobot.py 2>&1`
#echo "¡The bot is crashed!"
#echo $output | mail -s "Aviso" elgranpote@gmail.com
#echo "Rebooting in:"
#for i in 1
#do
#echo "$i..."
#done
#echo "###########################################"
#echo "#Bot is restarting now                    #"
#echo "###########################################"
#done
