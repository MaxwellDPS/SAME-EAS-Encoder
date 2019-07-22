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
set /p "ain=y/n: "
if "%ain%"=="n" goto NoAudioIn
if "%ain%"=="y" goto AudioIn
if "%ain%"=="N" goto NoAudioIn
if "%ain%"=="Y" goto AudioIn
goto top



:NoAudioIn
set /p "rrr=Set Originator (WXR, EAS): "
set /p "eee=Set 3 Digit Event Code: "
set /p "lll=Set SAME Locations (Space Seperated, National Disabled): "
set /p "ooo=Set Output Name: "

if "%eee%"=="" set "eee=DMO"
set "ttt=now"
set "bbb=TESTALRT"
if "%ooo%"=="" set "ooo=Output"

echo ================
easencode.py -e %eee% -o %rrr% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" %ooo%.wav
echo ================
goto spa

:AudioIn
set /p "rrr=Set Originator (WXR, EAS): "
set /p "eee=Set 3 Digit Event Code: "
set /p "lll=Set SAME Locations (Space Seperated, National Disabled): "
set /p "aaa=Audio In Directory: 
set /p "ooo=Set Output Name: "

if "%eee%"=="" set "eee=DMO"
set "ttt=now"
set "bbb=TESTALRT"
if "%ooo%"=="" set "ooo=Output"

echo ================
easencode.py -e %eee% -o %rrr% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" -a "%aaa%" %ooo%.wav
echo ================
goto spa

:spa
set /p Play="Play Audio? (y/n): "
echo.
set /p mrr="Play using default player? (y/n): "

if %play%==y goto cont
if %play%==Y goto cont

pause
cls
goto top

:cont
if %mrr%==y goto skrp
if %mrr%==Y goto skrp
echo Set Sound = CreateObject("WMPlayer.OCX.7") > %cd%\sound.vbs
echo Sound.URL = "%cd%\%ooo%.wav" >> %cd%\sound.vbs
echo Sound.Controls.play >> %cd%\sound.vbs
echo do while Sound.currentmedia.duration = 0 >> %cd%\sound.vbs
echo wscript.sleep 100 >> %cd%\sound.vbs
echo loop >> %cd%\sound.vbs
echo wscript.sleep (int(Sound.currentmedia.duration)+1)*1000 >> %cd%\sound.vbs
start %cd%\sound.vbs
pause
del %cd%\sound.vbs
cls
goto top

:skrp
start %ooo%.wav
pause
cls
goto top
