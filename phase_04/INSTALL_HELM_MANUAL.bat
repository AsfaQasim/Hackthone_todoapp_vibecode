@echo off
echo Downloading Helm...
curl -L https://get.helm.sh/helm-v3.14.0-windows-amd64.zip -o helm.zip

echo.
echo Extracting...
tar -xf helm.zip

echo.
echo Moving helm.exe to C:\Program Files\helm\
mkdir "C:\Program Files\helm" 2>nul
move windows-amd64\helm.exe "C:\Program Files\helm\"

echo.
echo Cleaning up...
rmdir /s /q windows-amd64
del helm.zip

echo.
echo Adding to PATH...
setx PATH "%PATH%;C:\Program Files\helm" /M

echo.
echo ========================================
echo Helm installed successfully!
echo Please RESTART your terminal
echo Then run: helm version
echo ========================================
pause
