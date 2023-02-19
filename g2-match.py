import requests
import bs4
import time

class G2():
    def __init__(self,hltv_url='https://www.hltv.org/team/5995/g2',team_name='G2'):
        self.hltv_url = hltv_url
        self.team_name = team_name

    def get_upcoming_matches_table(self):
        team_page = self.hltv_url+"#tab-matchesBox"
        r = requests.get(team_page)
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        headline = soup.find_all('h2',class_="standard-headline")[1]
        upcoming_matches_table = headline.find_next('table',class_='table-container match-table')
        return upcoming_matches_table

    def get_match_details(self, match):
        match_timestamp = match.find_all('td')[0].span['data-unix']
        match_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(match_timestamp)/1000))
        team_against = match.find('td',class_='team-center-cell').find_all('div',class_='team-flex')[-1].a.img['title']
        match_link = match.find('td',class_='matchpage-button-cell').a['href']
        match_link = 'https://www.hltv.org'+match_link
        return { 'datetime': match_datetime, 'team_against': team_against, 'match_link': match_link }

    def get_upcoming_matches(self):
        upcoming_matches_table = self.get_upcoming_matches_table()
        event_name = upcoming_matches_table.find_all('thead')[1].tr.th.a.text
        if event_name:
            upcoming_matches = upcoming_matches_table.find('tbody').find_all('tr')
            matches = []
            for match in upcoming_matches:
                match_details = self.get_match_details(match)
                matches.append(match_details)
            return event_name,matches
        else:
            return []
    
    def beautify_matches(self,title,matches):
        print(f"The next event for {self.team_name} is:  {title}")
        print("----------------------------------")
        print("Date - Team - Match Link")
        for match in matches:
            print(f"{match['datetime']} - {match['team_against']} - {match['match_link']}")
        print("----------------------------------")
        

if __name__ == '__main__':
    g2 = G2("https://www.hltv.org/team/6667/faze","FaZe Clan")
    event_name,matches = g2.get_upcoming_matches()
    g2.beautify_matches(event_name,matches)