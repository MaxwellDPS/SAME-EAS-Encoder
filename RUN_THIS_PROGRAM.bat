@echo off

set "VOICE=Paul"
set "LOCAL=000000"

:top
cls

title EAS Creator

if not exist "%cd%\Output\" mkdir "%cd%\Output\"

echo Thank you for using the EAS Genorator by A-c0rN and MazariFox.
echo ==============================================================
echo.
echo Specify TTS voice and LOCAL by right-clicking this file, and
echo selecting Edit. Should be Isolated.
echo.
echo Leave blank for Defaults.
echo Defaults: EAS, DMO, LOCAL, 0015, SFTENCDR
echo.
set /p "mmm=Set Originator (Options: EAS, CIV, WXR): "
set /p "eee=Set Event (Three letter event, EX: DMO): "
set /p "lll=Set SAME Locations (Space Seperated): "
set /p "ddd=Duration (Use NWR Specifications): "
set /p "bbb=Set Callsign (Max 8 Characters): "
echo.
echo ==============================================================

if "%mmm%"=="" set "mmm=EAS"
if "%eee%"=="" set "eee=DMO"
if "%lll%"=="" set "lll=%LOCAL%"
if "%ooo%"=="" set "ooo=ALERT"
set "nnn=%ooo%-EOM"
set "ttt=now"
if "%ddd%"=="" set "ddd=0015"
if "%bbb%"=="" set "bbb=SFTENCDR"


echo.
echo ENCODING ALERT NOW!
echo.
echo.
easencode.py -o %mmm% -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" -x yes "%cd%\Output\%ooo%.wav"
echo.
easencode.py -o %mmm% -e %eee% -f %lll% -d %ddd% -t %ttt% -c "%bbb%" "%cd%\Output\%nnn%.wav"
echo.
echo ==============================================================

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

echo.
set /p "TEXT=Please enter any text you would like the application to say: "
echo.
echo ==============================================================
echo.
rem echo Muting Audio...
rem timeout 1 /nobreak >nul
rem Static\nircmd.exe muteappvolume Music.UI.exe 1 >nul
rem echo Done.
rem echo.

timeout 1 /nobreak >nul

echo Sending Headers...
start /wait Output\sound.vbs "Static\autoclose.bat" >nul
echo Done.
echo.

if not "%TEXT%"=="" (
	echo Sending Audio Message...
	Static\balcon.exe -n %VOICE% -s -8 -t "%TEXT%" >nul
	echo Done.
	echo.
)

echo Sending EOMs...
start /wait Output\sound2.vbs "Static\autoclose.bat" >nul
echo Done.
echo.

rem echo Unmuting Audio...
rem timeout 1 /nobreak >nul
rem Static\nircmd.exe muteappvolume Music.UI.exe 0 >nul
rem echo Done.
rem echo.
echo ==============================================================
echo.
pause
goto top
