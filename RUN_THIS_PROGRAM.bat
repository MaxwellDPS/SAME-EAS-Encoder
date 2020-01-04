@echo off

set "VOICE=Paul"

:top
cls

title EAS Creator

if not exist "%cd%\Output\" mkdir "%cd%\Output\"


set /p "mmm=Set Originator (Default EAS): "
set /p "eee=Set Event (Default DMO): "
set /p "lll=Set SAME Locations (Space Seperated) (Default LOCAL): "
set /p "ddd=Duration (Default 0015): "
set /p "bbb=Set Callsign (Default WACN): "

if "%mmm%"=="" set "mmm=EAS"
if "%eee%"=="" set "eee=DMO"
if "%eee%"=="RWT" (
	if "%lll%"=="" set "lll=005000 006000 012000 013000 017000 020000 022000 028000 029000 040000 042000 047000 051000 005007 005143 040041"
)
if "%lll%"=="" set "lll=005007 005143 040041"
if "%ooo%"=="" set "ooo=ALERT"
set "nnn=%ooo%-EOM"
set "ttt=now"
if "%ddd%"=="" set "ddd=0015"
if "%bbb%"=="" set "bbb=WACN"

cls

echo ENCODING ALERT NOW!
echo.
echo.
echo.
easencode.py -o %mmm% -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" -x yes "%cd%\Output\%ooo%.wav"
echo.
echo.
echo.
easencode.py -o %mmm% -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" "%cd%\Output\%nnn%.wav"

(
	echo Set Sound = CreateObject^("WMPlayer.OCX.7"^)
	echo Sound.URL = "%cd%\Output\%ooo%.wav"
	echo Sound.Controls.play
	echo do while Sound.currentmedia.duration = 0
	echo wscript.sleep 100
	echo loop
	echo wscript.sleep ^(int^(Sound.currentmedia.duration^)+1^)*1000
) > "%cd%\Output\sound.vbs"

(
	echo Set Sound = CreateObject^("WMPlayer.OCX.7"^)
	echo Sound.URL = "%cd%\Output\%nnn%.wav"
	echo Sound.Controls.play
	echo do while Sound.currentmedia.duration = 0
	echo wscript.sleep 100
	echo loop
	echo wscript.sleep ^(int^(Sound.currentmedia.duration^)+1^)*1000
) > "%cd%\Output\sound2.vbs"

cls
set /p "TEXT=Please enter any text you would like the application to say: "
if "%TEXT%"=="RWT" set "TEXT=%cd%\Static\RWT.txt"
cls

echo Muting Audio...
timeout 1 /nobreak >nul
Static\nircmd.exe muteappvolume Music.UI.exe 1 >nul
echo Done.
echo.

timeout 1 /nobreak >nul

echo Sending Headers...
start /wait Output\sound.vbs "Static\autoclose.bat" >nul
echo Done.
echo.

echo Sending Audio Message...
Static\balcon.exe -n %VOICE% -s -8 -t "%TEXT%" >nul
echo Done.
echo.

echo Sending EOMs...
start /wait Output\sound2.vbs "Static\autoclose.bat" >nul
echo Done.
echo.

echo Unmuting Audio...
timeout 1 /nobreak >nul
Static\nircmd.exe muteappvolume Music.UI.exe 0 >nul
echo Done.
echo.
echo.
pause
goto top
