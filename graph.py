import matplotlib.pyplot as plt
import pandas as pd
import sys
import seaborn as sns

def build_df(fname):
	df = pd.read_csv(fname)
	df.drop(columns=["Server ID","Sponsor","Server Name", "Share","IP Address", "Distance"], inplace=True)
	df["Timestamp"] = df["Timestamp"].apply(lambda x: "-".join(x.split("T")[0].split("-")[1:]))
	df[["Download","Upload"]] = df[["Download","Upload"]].apply(lambda x: x/(1024**2))
	return df

def build_graph(df):
	sns.set_style("white")
	dfg = df.groupby("Timestamp").mean()
	fig, ax1 = plt.subplots(figsize=(12,6))
	
	x=list(range(len(dfg.index)))
	focus_point = list(dfg.index).index("09-11")
	ax1.plot([focus_point,focus_point],[0.5,15], color="black")
	ax1.annotate('Changed ISP',xy=(focus_point, 14), xycoords='data', 
		xytext=(-15, 25), textcoords='offset points',
        arrowprops=dict(facecolor='black', shrink=0.05),
        horizontalalignment='right', verticalalignment='bottom')

	lns1 = ax1.plot(x,dfg["Download"],color="b",label="Download")
	lns2 = ax1.plot(x,dfg["Upload"],color="g",label="Upload")
	ax1.set_ylabel("Up/Download Speed(Mb/S)")
	ax1.set_xlabel("(month-day)")

	ax2 = ax1.twinx()
	lns3 = ax2.plot(list(range(len(dfg.index))),dfg["Ping"],'r--',label="ping")
	ax2.set_ylabel("Ping ms (lower is better)")
	ax2.tick_params('y',colors='r')

	avg_y = dfg["Download"][:focus_point].apply(lambda x: dfg["Download"][:focus_point].mean())
	avg_y=avg_y.append(dfg["Download"][focus_point:].apply(lambda x: dfg["Download"][focus_point:].mean()))
	fill1=ax1.fill_between(x,avg_y, label = "avg down" ,color="skyblue", alpha=0.4)

	avg_y = dfg["Upload"][:focus_point].apply(lambda x: dfg["Upload"][:focus_point].mean())
	avg_y=avg_y.append(dfg["Upload"][focus_point:].apply(lambda x: dfg["Upload"][focus_point:].mean()))
	fill2=ax1.fill_between(x,avg_y, label = "avg up" ,color="greenyellow", alpha=0.4)

	avg_y = dfg["Ping"][:focus_point].apply(lambda x: dfg["Ping"][:focus_point].mean())
	avg_y=avg_y.append(dfg["Ping"][focus_point:].apply(lambda x: dfg["Ping"][focus_point:].mean()))
	fill3=ax2.fill_between(x,avg_y, label="avg ping" ,color="lightsalmon", alpha=0.3)


	fills =[fill1,fill2,fill3]
	labs = [l.get_label() for l in fills]
	fill_leg = plt.legend(fills, labs, loc=2)
	plt.gca().add_artist(fill_leg)

	lns = lns1+lns2+lns3
	labs = [l.get_label() for l in lns]
	plt.legend(lns, labs, loc=0)

	plt.xticks(x,dfg.index)
	plt.title("2018 internet up/down speeds")
	plt.tight_layout()
	plt.savefig("results.png")

if __name__=="__main__":
	df = build_df(sys.argv[1])
	build_graph(df)