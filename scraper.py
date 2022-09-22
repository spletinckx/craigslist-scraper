from bs4 import BeautifulSoup
import requests

keywords = ["no couple", "lompoc", "ventura", "carpinteria", "single occupancy"]

potential_houses = []

def scrape_page(initial_link):
    html = requests.get(initial_link).text

    soup = BeautifulSoup(html, "html.parser")

    #print(soup.body.section.form)

    listings = soup.find_all("li", {"class": "result-row"})
    print("Found {} listings.".format(len(listings)))

    c = 0
    matches = 0
    for listing in listings:
        c += 1
        print("Scraping {}/{} houses...".format(c, len(listings)))

        link = listing.find_all("a")[0]["href"]
        if "/off/" in link:
            continue
        if "/prk/" in link:
            continue

        new_html = requests.get(link).text.lower()
        new_soup = BeautifulSoup(new_html, "html.parser")
        discard = False

        money = new_soup.find_all("span", {"class": "price"})
        if len(money) < 1:
            continue

        price = str(money[0]).split("$")[1].split("<")[0]
        price = int(price.replace(",", ""))

        if price > 2000:
            continue

        for word in keywords:
            if word in new_html:
                discard = True
                break

        if not discard:
            print("Possible house: {}".format(link))
            potential_houses.append(link)
            matches += 1

    print("Found {} matches!".format(matches))
    return len(listings)


start_link = "https://santabarbara.craigslist.org/search/hhh"
current_link = start_link
offset = 0
done = False
while not done:
    print("Finding listings in {}".format(current_link))
    num_of_listings = scrape_page(current_link)
    if num_of_listings < 120:
        done = True
    offset += num_of_listings
    current_link = start_link + "?s={}".format(offset)

print("Found {} matches total over whole Craigslist.".format(len(potential_houses)))
outfile=open("potential_houses_2022-07-12.txt", "w")
for house in potential_houses:
    outfile.write("{}\n".format(house))
