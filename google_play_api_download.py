from Google_play_api.googleplay import GooglePlayAPI
from config.config import LOCALE, TIMEZONE, GOOGLE_PASSWORD, GOOGLE_LOGIN
import sys
import argparse

api = None

#########################################################################
# need email and password
# need to login on https://accounts.google.com/b/0/DisplayUnlockCaptcha
# if show up SecurityCheckError when you modify the code
#########################################################################


def initialize_login():
    global api
    #first login need to use account/password
    api = GooglePlayAPI(LOCALE, TIMEZONE)
    api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD)

    # you can get gsfid and subtoken after login
    gsfId = api.gsfId
    authSubToken = api.authSubToken

    # use id and authSubToken to login

    api.login(None, None, gsfId, authSubToken)


def downloadApkByPackageName(packagename):

    print('\nDownloading apk\n')
    download = api.download(packagename, expansion_files=False)
    with open(download['docId'] + '.apk', 'wb') as apkfile:
        for chunk in download.get('file').get('data'):
            apkfile.write(chunk)

    print('\nDownload successful\n')


def searchApkByKeyWord(search_word, maximum_search):
    """
    search(self, query, nb_result, offset=None):
       
    Search the play store for an app.

    nb_result is the maximum number of result to be returned.

    offset is used to take result starting from an index.
    """

    apps = api.search(search_word, maximum_search)

    print('searching....\n')

    for app in apps:
        print(app['docId'])


def getDetailsByPackName(packagename):

    details = api.details(packagename)

    #print(details['docId'])
    #print(details['permission'])

    for key, value in details.items():
        print(str(key) + "===" + str(value) + "\n")


def browseCategories():
    """
    get all categories in google play store
    """
    categories = api.browse()

    for cate in categories:
        print(cate)


def getSubListByCategory(category):
    """
    get specific sub category  by using categories name
    """
    print("List all app in this category: %s" % category)

    sub_list_app = api.list(category)

    for sub_list in sub_list_app:
        print(sub_list)


def getAppBySubList(category, sub_list):
    """
    get app by specific sub_list name
    """
    #example api.list("apps_topselling_free","MUSIC_AND_AUDIO")
    sub_list_app = api.list(category, sub_list)

    for app in sub_list_app:
        print(app['docId'])


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-download", help="download apk by package name")
    parser.add_argument("-detail", help="get detailds from apk name")
    parser.add_argument("-browse",help="get all categories from google")
    args = parser.parse_args()

    if args.download:
        initialize_login()
        downloadApkByPackageName(args.download)

    if args.detail:
        initialize_login()
        getDetailsByPackName(args.detail)

    if args.browse:
        initialize_login()
        browseCategories()


if __name__ == '__main__':
    Main()
