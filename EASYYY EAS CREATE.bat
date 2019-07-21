@echo off

title EAS Creator

:top

set /p ynt="Use Text Audio? (Y/N): "
if "%ynt%"=="y" set /p aaa="Audio Path: "
if "%ynt%"=="y" set /p set="Audio Extension: "

set /p "mmm=Set Originator: "
set /p "eee=Set Event: "
set /p "lll=Set SAME Locations (Space Seperated): "
set /p "ddd=Set Duration: "
set /p "ttt=Set Start Time: "
set /p "bbb=Set Broadcaster: "
set /p "ooo=Set Output Name: "

if "%mmm%"=="" set "eee=WXR"
if "%eee%"=="" set "eee=RWT"
if "%lll%"=="" set "lll=000000"
if "%ddd%"=="" set "ddd=0015"
if "%ttt%"=="" set "ttt=now"
if "%bbb%"=="" set "bbb=KACN/NWS"
if "%ooo%"=="" set "ooo=Test"


if "%ynt%"=="n" easencode.py -o %mmm% -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" %ooo%.wav && goto skipsetaudio

easencode.py -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" -a %aaa%.%set% %ooo%.wav


:skipsetaudio

pause

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