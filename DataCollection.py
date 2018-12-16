from riotwatcher import RiotWatcher
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import xlsxwriter
from tempfile import TemporaryFile
import time
book = xlsxwriter.Workbook("SummonerData.xlsx")
sheet1 = book.add_worksheet()


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """km
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


ranks = []
winrates = []
wins = []
loses = []
summonerids = []

for i in range(2,8700):
#for i in range(2,5):
#for i in range(118,120):
    print(i)
    #gets the raw html page
    raw_html = simple_get('http://na.op.gg/ranking/ladder/page=' + str(i))

    html = BeautifulSoup(raw_html,'html.parser')

    #gets the summoners information for entire page
    rankingtable = html.find("table", {"class" : "ranking-table"})
    #gets rank information for summoners
    rank = html.find_all("td", {"class": "ranking-table__cell ranking-table__cell--tier"})
    #gets winrate information for summoners
    winrate = html.find_all("span", {"class": "winratio__text"})
    #gets win information for summoners
    win = html.find_all("div", {"class": "winratio-graph__text winratio-graph__text--left"})
    #gets lose information for summoners
    lose = html.find_all("div", {"class": "winratio-graph__text winratio-graph__text--right"})
    #get summoner name
    summonerid = html.find_all("td",{"class": "ranking-table__cell ranking-table__cell--summoner"})
    #print(rankingtable)


    for j in range(0,99):
        try:
            #print(j)
            winratestr = winrate[j].text
            location = winratestr.find('%')
            winpercent = int(winratestr[0:location])

            #ensures that winpercent is between 47-53% and that the player has atleast 100 games of ranked played. If player does
            #then the data for the summoner will be stored.
            if (int(win[j].text) + int(lose[j].text)) >= 100 and winpercent > 46 and winpercent < 54:
                winrates.append(winrate[j].text)
                wins.append(win[j].text)
                loses.append(lose[j].text)
                rankfix1 = rank[j].text.replace('\n\t\t\t\t\t\t\t\t\t\t','')
                rankfix2 = rankfix1.replace('\n\t\t\t\t\t\t\t\t\t','')
                ranks.append(rankfix2)
                summonerids.append(summonerid[j].text)
        except IndexError:
            pass
    #print(ranks)
    #print(winrates)
    #print(wins)
    #print(loses)
    print(len(wins))
    #print(summonerids)
    #time.sleep(1)
for i in range(0,len(wins)):
    sheet1.write(i,1,summonerids[i])
    sheet1.write(i, 2, ranks[i])
    sheet1.write(i, 3, wins[i])
    sheet1.write(i, 4, loses[i])
    sheet1.write(i, 5, winrates[i])


book.close()