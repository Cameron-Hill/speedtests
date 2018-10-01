temp = """

<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/export-data.js"></script>

<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Internet Speed Tests'
    },
    subtitle: {
        text: 'Internet Speeds per room'
    },
    xAxis: {
        categories: {{data.location}},
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Speed (Mbps)'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} Mbps</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Downloads',
        data: {{data.download}}

    }, {
        name: 'Uploads',
        data: {{data.upload}}

    }]
});
</script>
"""

print("initialising",end="")
import speedtest
print(".",end="")
import sys
print(".")
import pickle
import os
from jinja2 import Template

if len(sys.argv) <2:
	print("Supply a location")
	sys.exit(1)

s= speedtest.Speedtest()

print("Finding best server...")
s.get_best_server()

print("downloading ...")
s.download()

print("upload ...")
s.upload()

location = sys.argv[1]

keys=["download","upload",]
d = {x:y for x,y in s.results.dict().items() if x in keys}
d["upload"] = round(d["upload"] /1024**2,3)
d["download"] = round(d["download"] /1024**2,3)
d["location"] = location
path = os.path.dirname(os.path.abspath(__file__))

try:
	data =pickle.load(open("location_data.p","rb"))
except:
	data = {"upload":[],"download":[],"location":[]}

for k,v in d.items():
	data[k].append(v)

template = Template(temp)
x = template.render(data = data)

with open("location_results.html","w") as f:
	f.write(x)

pickle.dump(data,open("location_data.p","wb"))