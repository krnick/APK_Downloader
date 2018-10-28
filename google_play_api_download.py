from Google_play_api.googleplay import GooglePlayAPI
from config.config import LOCALE, TIMEZONE, GOOGLE_PASSWORD , GOOGLE_LOGIN
import sys

#########################################################################
# need email and password
# need to login on https://accounts.google.com/b/0/DisplayUnlockCaptcha
# if show up SecurityCheckError when you modify the code
#########################################################################

#first login need to use account/password
api = GooglePlayAPI(LOCALE, TIMEZONE)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD )

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

    for key,value in details.items():
        print(str(key) +"==="+str(value)+"\n")

def browseCategories():
    categories = api.browse()

    for cate in categories:
        print(cate) 

browseCategories()
