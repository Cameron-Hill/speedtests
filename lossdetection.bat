:D
ping -n 30 127.0.0.1 > nul
echo %date% %time% >> packetmonitor.csv
ping -n 30 8.8.8.8 >> packetmonitor.csv
goto D

