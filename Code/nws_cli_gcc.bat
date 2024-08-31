cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --windows-icon-from-ico=weather.ico ^
    nws_cli.py
pause