import progressbar
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

progress_bar = None

top_page_url = "http://m.apk.tw/top"
content = urllib.request.urlopen(top_page_url)
html_code = content.read().decode("utf-8")

soup = BeautifulSoup(html_code, "html.parser")


def getInformationFromAPk(url):

    try:
        information_content = urllib.request.urlopen(url)
        information_html_code = information_content.read().decode("utf-8")
        soup = BeautifulSoup(information_html_code, "html.parser")

        apk_url = soup.find(
            "div", attrs={
                'class': 'download'
            }).find(
                "a", href=True)['href']

        apk_name = soup.find("h3", attrs={'class': 'mt-10'}).string

        # get property from web
        apk_property = soup.find(
            "div", attrs={
                'class': 'property'
            }).find_all('li')
        prolist = []

        for li in apk_property:
            prolist.append(str(li))

        # slice string from ':' and end with '</'

        version = prolist[0][prolist[0].index("：") + 1:prolist[0].index("</")]
        filesize = prolist[1][prolist[1].index("：") + 1:prolist[1].index("</")]
        download_times = prolist[2][prolist[2].index("：") +
                                    1:prolist[2].index("</")]
        classification = prolist[3][prolist[3].index("\">") +
                                    2:prolist[3].index("</")]
        system = prolist[4][prolist[4].index("：") + 1:prolist[4].index("</")]
        package_name = prolist[5][prolist[5].index("：") +
                                  1:prolist[5].index("</")]
        date = prolist[6][prolist[6].index("：") + 1:prolist[6].index("</")]

        return {
            'apk_url': apk_url,
            'apk_name': apk_name,
            'version': version,
            'filesize': filesize,
            'download_times': download_times,
            'classification': classification,
            'system': system,
            'package_name': package_name,
            'date': date
        }
    except urllib.error.URLError as e:
        print("URL ERROR given that you provide wrong app url")
        print(e.reason)
        return None


# download apk file from m.apk.tw/top


# 從提供的網址下載檔案下來
def downloadApkFromUrl(url_to_download, filename, total_size):
    try:
        print("Downloading  %s  file , total size : %s" % (filename , total_size))
        urllib.request.urlretrieve(url_to_download, filename,
                                   callback_download_complete)
        print("Finish donloading")
    except urllib.error.HTTPError as e:
        print("HTTP ERROR")
        print(e.reason, e.code)
    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason, e.code)


#   callback function for urlretrieve to generate progressbar
def callback_download_complete(block_num, block_size, total_size):
    global progress_bar
    if progress_bar is None:
        progress_bar = progressbar.ProgressBar(maxval=total_size).start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        progress_bar.update(downloaded)
    else:
        progress_bar.finish()
        progress_bar = None


def download_all_app(sub_url):
    # Usage:
    # 取得單一APP資訊
    result_information = getInformationFromAPk(sub_url)
    # 開始下載
    if (result_information is not None):
        downloadApkFromUrl(result_information['apk_url'],
                           result_information['apk_name'] + '.apk',
                           result_information['filesize'])


def Main():

    # 取得全部要下載的APP url
    for cat in range(0, 6):
        # category
        w240 = soup.findAll("div", {"class": "w240 mt-12 mr-15"})[cat]
        category = w240.find("div", {"class": "title"}).h3.string
        # print category

        for ts in range(0, 2):
            # sub-category
            tab = w240.findAll("div", {"class": "tab"})
            spans = w240.findAll('span')
            # print subcategory
            subcategory = spans[ts].string
            # print subcategory
            cat_sub = category + "-" + subcategory

            # download list
            toplist = w240.findAll("div", {"class": "toplist ami"})

            rank = 1

            for url in toplist[ts].find_all("a"):
                if (url.get('class') == ['down']):
                    each_apk_url = url.get('href')

                    # print(getInformationFromAPk(each_apk_url)) 輸出排行榜中app的url 
                    # usage :
                    download_all_app(each_apk_url)# 開始查詢資訊並下載
                    # print(each_apk_url, rank) 輸出排名
                    #rank += 1


if __name__ == '__main__':
    Main()
