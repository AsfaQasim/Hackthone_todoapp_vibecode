@echo off
echo Opening CORS test in browser...
start test_cors_browser.html
echo.
echo Instructions:
echo 1. Click the "Test Backend Connection" button
echo 2. Check the output on the page
echo 3. Open DevTools (F12) and check Console for any CORS errors
echo.
echo If you see "CORS is working!" then the fix is successful!
echo.
pause
