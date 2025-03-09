@echo off

mkdir %~dp0output
cd %~dp0output

pyinstaller --noconfirm --onedir --console --icon "..\icon.ico" --name "DDSearch" "..\DDSearch.py"

cd dist
move DDSearch ../..
cd ../..
rmdir /s /q bin
rename DDSearch bin
rmdir /s /q output