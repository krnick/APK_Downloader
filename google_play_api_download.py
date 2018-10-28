from google_play_api.googleplay import GooglePlayAPI
from core.config import *
import sys

#########################################################################
# need email and password
# need to login on https://accounts.google.com/b/0/DisplayUnlockCaptcha
# if show up SecurityCheckError when you modify the code
#########################################################################
api = GooglePlayAPI(LOCALE, TIMEZONE)
#api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD )
api.login( gsfId = ANDROID_ID, authSubToken=AUTH_TOKEN)


def downloadApkByPackageName(packagename):

    print('\nDownloading apk\n')
    download = api.download(packagename, expansion_files=False)
    with open(download['docId'] + '.apk', 'wb') as apkfile:
        for chunk in download.get('file').get('data'):
            apkfile.write(chunk)

    print('\nDownload successful\n')


#if (len(sys.argv) == 2):
#    downloadApkByPackageName(sys.argv[1])
#else:
#    print("usage : python3 DownloadApk.py com.apkfordownload.tw")
