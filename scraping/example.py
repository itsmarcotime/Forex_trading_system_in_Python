from bs4 import BeautifulSoup

with open("index.html", "r") as f:
    data = f.read()

#print(data)
    
soup = BeautifulSoup(data, 'html.parser')

#print(soup)

divs = soup.select("div")

# print(len(divs), "divs found")

# for d in divs:
#     print()
#     print(d)

print("Content: ", divs[0].get_text())

div2 = divs[1]

pps = div2.select("p")

print("PPS:")

for p in pps:
    print(p.get_text())

print("dailies:")

dailies = soup.select(".daily")
for d in dailies:
    print(d.get_text())

print(dailies[1].attrs["data-value"])