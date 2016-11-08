from bs4 import BeautifulSoup
import urllib
url = "http://www.intellicast.com/Local/Weather.aspx?location=NUXX0001"
f = urllib.urlopen(url).read()
soup = BeautifulSoup(str(f),"html.parser")
mydivs = soup.findAll(True, {'class':['fctText', 'row']})
 

for d in soup.findAll(True, {'class':['fctDetails', 'ui-tabs-panel', 'ui-widget-content', 'ui-corner-bottom']}):
	print(d)

