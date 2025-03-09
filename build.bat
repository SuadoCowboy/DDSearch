@echo off

mkdir %~dp0output
cd %~dp0output

pyinstaller --noconfirm --onedir --console --icon "..\icon.ico" --name "DDSearch" "..\DDSearch.py"

rmdir /s /q DDSearch
cd dist
move DDSearch ../..
cd ../..
rmdir /s /q output