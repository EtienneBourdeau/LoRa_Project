ECHO OFF
CLS
:MENU

ECHO.
ECHO			GATEWAY 'LAURENT'
ECHO.
ECHO ..........................................................
ECHO PRESS 1, 2, 3, 4, 5, or 6 to select your task.
ECHO PRESS 0 to return to MAIN MENU
ECHO ..........................................................
ECHO.
ECHO 1 - Open Session on Gateway
ECHO 2 - Launch Client, Append Data File
ECHO 3 - Launch Client, Overwrite Data File
ECHO 4 - Copy Data File from Gateway to Computer
ECHO 5 - Run Python Decodeb64 and Map_Generator (already existing data file)
ECHO 6 - Copy Data File AND Run Python Programs
ECHO 0 - Return to Main Menu
ECHO.

SET /P M=Type 1, 2, 3, 4, 5, 6 or 0, then press ENTER: 
IF %M%==1 GOTO SESS
IF %M%==2 GOTO APPEND
IF %M%==3 GOTO WRITE
IF %M%==4 GOTO COPY
IF %M%==5 GOTO PYTH
IF %M%==6 GOTO COPYTH
IF %M%==0 GOTO MAIN

:SESS
cd C:\Users\%USERNAME%\Desktop\Scripts\For Gateway 'Laurent'
start Opensession.bat
GOTO MENU
:APPEND
cd C:\Users\%USERNAME%\Desktop\Scripts\For Gateway 'Laurent'
start Appenddata.bat
GOTO MENU
:WRITE
cd C:\Users\%USERNAME%\Desktop\Scripts\For Gateway 'Laurent'
start Writedata.bat
GOTO MENU
:COPY
cd C:\Users\%USERNAME%\Desktop\Scripts\For Gateway 'Laurent'
start Getdatafile.bat
GOTO MENU
:PYTH
cd C:\Users\%USERNAME%\Desktop\Scripts
start runpython.bat
GOTO MENU
:COPYTH
cd C:\Users\%USERNAME%\Desktop\Scripts\For Gateway 'Laurent'
start Getdatafile.bat
cd C:\Users\%USERNAME%\Desktop\Scripts
start /wait runpython.bat
GOTO MENU
:MAIN
cd C:\Users\%USERNAME%\Desktop\Scripts
start MENU.bat
exit