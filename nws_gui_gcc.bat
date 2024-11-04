cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --windows-console-mode=disable ^
    --enable-plugin=tk-inter ^
    --windows-icon-from-ico=weather.ico ^
    nws_gui.py
pause

