import requests
from bs4 import BeautifulSoup
import datetime

TODAY = str(datetime.date.today())
URL = r"https://mfn.se/all/s?filter=(and(or(.properties.tags%40%3E%5B%22sub%3Areport%22%5D))(or(.properties.lang%3D%22sv%22))(or(a.list_id%3D35207)(a.list_id%3D35208)(a.list_id%3D35209)(a.list_id%3D919325)(a.list_id%3D35198)(a.list_id%3D29934)(a.list_id%3D5700306)(a.list_id%3D4680265)))"

def print_reports(reports):
    for report in reports:
        res = f"{report['company']}: {report['title']}\nArticle: {report['title-link']}\nReport link(s): {report['report-links']}\n"
        print(res)

def main():
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="content-body")

    elements = results.find_all("div", class_="short-item")

    reports = []
    for element in elements:
        report = {}
        date = element.find("span", class_ = "compressed-date")
        if (date.text != TODAY):
            continue
        
        name = element.find("span", class_ = "compressed-author")
        report['company'] = name.text.strip('\n')
        
        title = element.find("span", class_ = "compressed-title")
        report['title'] = title.text.strip('\n')
        for a in title.find_all('a', href=True):
            title_link = a['href']
            report['title-link'] = "mfn.se" + title_link
        
        link_span = element.find("span", class_ = "attachment-wrapper")
        links = []
        for a in link_span.find_all('a', href=True):
            links.append(a['href'])
        report['report-links'] = links
        
        reports.append(report)
    
    print(f"Reports for {TODAY}:")
    print_reports(reports)

if __name__ == "__main__":
    main()