rem Install one job(pooling data) to system Shedule
rem set OLDDIR=%CD%
python -c "import sys; print (sys.executable)" > tmpFile 
set /p pyth= < tmpFile 
del tmpFile 
echo %CD:~0,2%>Task.bat
echo cd %CD% >> Task.bat
echo %pyth% -m rtb.cron >> Task.bat
echo %CD%Task.bat
schtasks /Create /SC HOURLY /TN "Python rtb tasks" /TR %CD%\Task.bat