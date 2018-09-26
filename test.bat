cd D:\cambo\Docs\Misc\speedtest
echo "Executing speedtest:"
speedtest-cli --csv --server 10602 >> speedtests.csv
echo "building graph"
python graph.py speedtests.csv
echo "Successfully saved graph"