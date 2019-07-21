@echo off
title EAS Gen
:top
cls
echo ============== - + - ==============
echo SAME-EAS-Encoder
echo by eas-alert on Github
echo https://github.com/eas-alert
easencode.py -v
echo Read the README file before cont.
echo ============== - + - ==============
echo Audio In?
set /p "ain=y/n "
if "%ain%"=="n" goto NoAudioIn
if "%ain%"=="y" goto AudioIn
goto top



:NoAudioIn
set /p "eee=Set 3 Digit Event Code: "
set /p "lll=Set SAME Locations (Space Seperated): "
set /p "ddd=Set Duration: "
rem set /p "ttt=Set Start Time: "
rem set /p "rrr=Originator (PEP, EAS, WXR): "
rem set /p "bbb=Set Callsign: "
set /p "ooo=Set Output Name: "

if "%eee%"=="" set "eee=DMO"
if "%ttt%"=="" set "ttt=now"
if "%rrr%"=="" set "rrr=wxr"
if "%bbb%"=="" set "bbb=TSTALRT"
if "%ooo%"=="" set "ooo=Output"

echo ================
easencode.py -e %eee% -o %rrr% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" %ooo%.wav
echo ================
goto spa

:AudioIn
set /p "eee=Set Event: "
set /p "lll=Set SAME Locations (Space Seperated): "
set /p "ddd=Set Duration: "
rem set /p "ttt=Set Start Time: "
rem set /p "rrr=Originator (PEP, EAS, WXR): "
rem set /p "bbb=Set Callsign: "
set /p "aaa=Audio In Directory (MUST BE WAV): 
set /p "ooo=Set Output Name: "

if "%eee%"=="" set "eee=DMO"
if "%ttt%"=="" set "ttt=now"
if "%rrr%"=="" set "rrr=wxr"
if "%bbb%"=="" set "bbb=TSTALRT"
if "%ooo%"=="" set "ooo=Output"

echo ================
easencode.py -e %eee% -o %rrr% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" -a "%aaa%" %ooo%.wav
echo ================
goto spa

:spa
set /p Play="Play Audio? (y/n): "

if %play%==y goto cont

pause
cls
goto top

:cont
echo Set Sound = CreateObject("WMPlayer.OCX.7") > %cd%\sound.vbs
echo Sound.URL = "%cd%\%ooo%.wav" >> %cd%\sound.vbs
echo Sound.Controls.play >> %cd%\sound.vbs
echo do while Sound.currentmedia.duration = 0 >> %cd%\sound.vbs
echo wscript.sleep 100 >> %cd%\sound.vbs
echo loop >> %cd%\sound.vbs
echo wscript.sleep (int(Sound.currentmedia.duration)+1)*1000 >> %cd%\sound.vbs
start %cd%\sound.vbs
pause
cls
goto top