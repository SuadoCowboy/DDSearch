@echo off

cd "%~dp0"
rmdir /s /q output
mkdir output
cd output

pyinstaller --noconfirm --onedir --console --icon "..\icon.ico" --paths ddsearch/lib/site-packages --name "DDSearch" "..\DDSearch.py"

cd dist
move DDSearch ../
cd ..
rmdir /s /q build
rmdir /s /q dist
del DDSearch.spec