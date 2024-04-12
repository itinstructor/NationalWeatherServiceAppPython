cd c:\temp

python -m nuitka ^
    --standalone ^
    --windows-icon-from-ico=weather.ico ^
    nws_console.py
pause