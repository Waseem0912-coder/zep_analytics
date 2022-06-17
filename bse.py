import requests

from bs4 import BeautifulSoup
import time
import pandas as pd
page = requests.get("https://finance.yahoo.com/screener/predefined/undervalued_growth_stocks")

content = page.content

soup = BeautifulSoup(content,"html.parser")

#Prior data : Collected from the main page
yahooFinanceUrl = []
symbols = []
names = []
current_Price = []
volume = []
avg_Volume = []
market_cap = []
PE_Ratio = []
listOfInfo=[]
index=0

 

start = time.time()

for url in soup.find_all("a",attrs={"class":"Fw(600)"}):
	yahooFinanceUrl.append("https://finance.yahoo.com"+str(url.get('href')))

for symb in soup.find_all("a",attrs={"class":"Fw(600)"}):
	symbols.append(symb.text)

for name in soup.find_all("td",attrs={"aria-label":"Name"}):
	names.append(name.text)

for price in soup.find_all("td",attrs={"aria-label":"Price (Intraday)"}):
	current_Price.append(price.text)

for vol in soup.find_all("td",attrs={"aria-label":"Volume"}):
	volume.append(vol.text)

for avg in soup.find_all("td",attrs={"aria-label":"Avg Vol (3 month)"}):
	avg_Volume.append(avg.text)

for market in soup.find_all("td",attrs={"aria-label":"Market Cap"}):
	market_cap.append(market.text)

for pe in soup.find_all("td",attrs={"aria-label":"PE Ratio (TTM)"}):
	PE_Ratio.append(pe.text)



for url in yahooFinanceUrl:
	
	page = requests.get(url)
	content = page.content
	newSoup = BeautifulSoup(content,"html.parser")
	
	statistics_url = newSoup.find("a",attrs={"data-reactid":"11"})
	print(statistics_url.get('href'))
	
	newPage = requests.get("https://finance.yahoo.com"+str(statistics_url.get('href')))
	newContent = newPage.content
	SoupForStatistics = BeautifulSoup(newContent,"html.parser")
	
	CompleteDict={}
	Priordata={}
	Remainingdata={}

	for ev in SoupForStatistics.find_all("tr",attrs={"class":"Bxz(bb)"}):
		
		if ev.find("td",attrs={'class':'Pos(st)'}).text.strip() in ["52 Week High 3","52 Week Low 3","Return on Equity (ttm)","Profit Margin","Operating Margin (ttm)","Diluted EPS (ttm)"]:
			Remainingdata[ev.find("td",attrs={'class':'Pos(st)'}).text] = ev.find("td",attrs={'class':'Fw(500)'}).text

	
	Priordata["symbols"] = symbols[index]
	Priordata["name"] = names[index]
	Priordata["Current Price"] = current_Price[index]
	Priordata["volume"] = volume[index]
	Priordata["Average volume"] = avg_Volume[index]
	Priordata["Market Cap"] = market_cap[index]
	Priordata["PE Ratio"] = PE_Ratio[index]
	#Merging the data(in the form of dictionaries)
	Priordata.update(Remainingdata)
	listOfInfo.append(Priordata)
	index+=1
                    
end = time.time()

#Creating dataframe of list of dictionaries represented by 'listOfInfo'
df = pd.DataFrame(listOfInfo)               
#Storing dataframe in the form of .csv file 
df.to_csv("stocks.csv")
print("Time taken in the whole process of extracting information:",end-start)