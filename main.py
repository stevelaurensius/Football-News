import feedparser
from datetime import datetime, timedelta

class bbcRssReader:
    def __init__(self):
        self.team = ''
        self.url = ''
        self.feed = feedparser.parse(self.url)
        self.compiled_list = []
        self.no_of_output = 1


    def take_user_input(self):
        while True:
            self.team = input('Enter Team Name (or type "exit"):\n').lower().replace(' ', '-')
            if self.team == 'exit':
                exit()
            else:
                self.url = f"https://feeds.bbci.co.uk/sport/football/teams/{self.team}/rss.xml"
                self.feed = feedparser.parse(self.url)
                if self.feed.status == 404:
                    print('Team Not Found. Please Check Your Input\n')
                    print()
                elif self.feed.status == 200:
                    print()
                    break
        while True:
            try:
                how_many = int(input('Number of News (or type "0" to show all):\n'))
            except ValueError:
                print('Insert Number')
            else:
                if how_many < 1 or how_many > len(feedparser.parse(self.url)): 
                    self.no_of_output = len(feedparser.parse(self.url))
                    print()
                    break
                else:
                    self.no_of_output = how_many
                    print()
                    break
                

    def gmt_to_wib(self, gmt_time):
            timestamp_str = gmt_time
            gmt_offset = timedelta(hours=0)
            wib_offset = timedelta(hours=7)
            dt_gmt = datetime.strptime(timestamp_str, '%a, %d %b %Y %H:%M:%S GMT')
            dt_utc = dt_gmt - gmt_offset
            dt_wib = dt_utc + wib_offset
            return dt_wib.strftime('%a, %d %b %Y %H:%M:%S WIB')
    

    def compile_data(self):
        for i in range(self.no_of_output):
            if self.feed.entries[i].title != 'Football Daily':
                self.compiled_list.append([self.feed.entries[i].title, self.feed.entries[i].description, self.gmt_to_wib(self.feed.entries[i].published), self.feed.entries[i].link])
        return self.compiled_list
    

    def print_compiled_list(self):
        self.compile_data()
        for line in self.compiled_list:
            print(f'{"#" * 80}\n')
            print(f'Title:\n{line[0]}\n')
            print(f'Description:\n{line[1]}\n')
            print(f'Published On:\n{line[2]}\n')
            print(f'Read More:\n{line[3]}\n')
        print('#' * 80)

    
    def welcome_header(self):
        print(f'Here are latest news for {self.team.replace("-", " ").title()}.')
        print(f'There {"is" if len(self.feed.entries) == 1 else "are"} total {len(self.feed.entries)} news and here {"is" if self.no_of_output == 1 else "are"} {self.no_of_output} of them:\n')
        print(f'Data build date: {self.gmt_to_wib(self.feed.feed.updated)}')


    def menu(self):
        self.take_user_input()
        self.welcome_header()
        self.print_compiled_list()


if __name__ == '__main__':
    reader = bbcRssReader()
    reader.menu()
