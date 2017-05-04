ECHO OFF
CLS
:MENU

ECHO.
ECHO ..........................................................
ECHO PRESS 1, 2, or 3 to choose the gateway you want to manage
ECHO ..........................................................
ECHO.
ECHO 1 - Gateway 'Etienne'
ECHO 2 - Gateway 'Laurent'
ECHO 3 - Gateway 'GSM'
ECHO 0 - EXIT
ECHO.

SET /P M=Type 1, 2, 3, or 0 then press ENTER: 
IF %M%==1 GOTO ETI
IF %M%==2 GOTO LAU
IF %M%==3 GOTO GSM
IF %M%==0 exit

:ETI
cd C:\Users\connecsens-zatu\Desktop\Scripts\For Gateway 'Etienne'
netsh interface ipv4 set address name="Connexion au r‚seau local 2" static 192.168.2.5 255.255.255.0
ECHO WAIT FOR IP ADDRESS TO BE CHANGED
timeout /t 3
start menuetienne.bat
exit
:LAU
cd C:\Users\connecsens-zatu\Desktop\Scripts\For Gateway 'Laurent'
netsh interface ipv4 set address name="Connexion au r‚seau local 2" static 192.168.3.5 255.255.255.0
ECHO WAIT FOR IP ADDRESS TO BE CHANGED
timeout /t 3
start menulaurent.bat
exit
:GSM
cd C:\Users\connecsens-zatu\Desktop\Scripts\For Gateway 'GSM'
netsh interface ipv4 set address name="Connexion au r‚seau local 2" static 192.168.4.5 255.255.255.0
ECHO WAIT FOR IP ADDRESS TO BE CHANGED
timeout /t 3
start menugsm.bat
exit