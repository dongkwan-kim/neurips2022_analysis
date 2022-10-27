import pickle

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

page = requests.get("https://nips.cc/Conferences/2022/Schedule?type=Poster")
soup = BeautifulSoup(page.text, "html.parser")

url_id = []
for link in tqdm(soup.find_all("div", {"class": "maincard narrower poster"}),
                 desc="maincard narrower poster"):
    url_id.append(link.get("id").split("_")[1])

pp_names = []
pp_authors = []
for id in tqdm(url_id,
               desc="Schedule?showEvent="):
    pp_soup = BeautifulSoup(
        requests.get("https://nips.cc/Conferences/2022/Schedule?showEvent=" + id).text, "html.parser"
    )
    pp_name = pp_soup.find("div", {"class": "maincardBody"})
    pp_names.append(pp_name.get_text())
    authors = []

    for author in pp_soup.find_all("button", {"class": "btn btn-default"}):
        at_id = author.get("onclick")
        at_id = at_id[at_id.find("('") + 2: at_id.find("')")]
        at_soup = BeautifulSoup(
            requests.get("https://neurips.cc/Conferences/2022/Schedule?showSpeaker=" + at_id).text, "html.parser"
        )
        at_name = at_soup.find("h3").get_text()
        ins_name = at_soup.select("h3+h4")[0].get_text()
        authors.append(at_name + " (" + ins_name + ")")

    pp_authors.append(authors)
    print(authors)

with open("pp_names.txt", "wb") as fp:  # Pickling
    pickle.dump(pp_names, fp)

with open("pp_authors.txt", "wb") as fp:  # Pickling
    pickle.dump(pp_authors, fp)
