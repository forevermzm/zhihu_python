# requirements.
import requests

try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup

class SoupRequester:
    @classmethod
    def get_soup(cls, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/"
        }
        page = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(page.content, "lxml")
        return soup
