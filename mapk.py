import re
import logging
from datetime import datetime
# from progress.bar import Bar

from core.db.Mongo import DB
from core.androguard import apk
from common.objects import File
# from common.helpers import sizeof_fmt, print_header_line, print_result_line

import urllib
import BeautifulSoup

dangerous_permission = ["android.permission.READ_CALENDAR",
                        "android.permission.WRITE_CALENDAR",
                        "android.permission.CAMERA",
                        "android.permission.READ_CONTACTS",
                        "android.permission.WRITE_CONTACTS",
                        "android.permission.GET_ACCOUNTS",
                        "android.permission.ACCESS_FINE_LOCATION",
                        "android.permission.ACCESS_COARSE_LOCATION",
                        "android.permission.RECORD_AUDIO",
                        "android.permission.READ_PHONE_STATE",
                        "android.permission.CALL_PHONE",
                        "android.permission.READ_CALL_LOG",
                        "android.permission.WRITE_CALL_LOG",
                        "android.permission.ADD_VOICEMAIL",
                        "android.permission.USE_SIP",
                        "android.permission.PROCESS_OUTGOING_CALLS",
                        "android.permission.BODY_SENSORS",
                        "android.permission.SEND_SMS",
                        "android.permission.RECEIVE_SMS",
                        "android.permission.READ_SMS",
                        "android.permission.RECEIVE_WAP_PUSH",
                        "android.permission.RECEIVE_MMS",
                        "android.permission.READ_EXTERNAL_STORAGE",
                        "android.permission.WRITE_EXTERNAL_STORAGE"]

s1 = "http://m.apk.tw/top"

today = datetime.now().strftime('%Y-%m-%d')

soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(s1))


def insert_into_db(result):
    DB().insert_apk(result)


def generate_apk_info(targetapk, rank):

    result = {}
    result['vt_scan'] = False
    result['submit_date'] = today
    result['source'] = "mapk"
    result['title'] = cat_sub
    result['sub_title'] = subcategory
    result['name'] = unicode(apk_name).encode('utf8')
    result['rank'] = rank
    result['pgname'] = pkg_name
    result['version'] = version
    result['size'] = size
    result['upload_date'] = ""

    # Download APK
    result['apkdata'] = targetapk.read()

    # Calculate file hashes
    result.update(File(result['apkdata']).result)

    # write buffer to apk file
    filename = '/tmp/' + result['pgname'] + '.apk'
    with open(filename, 'wb') as f:
        f.write(result['apkdata'])

    n_permission = []
    d_permission = []

    # retrive permission from apk file
    try:
        a = apk.APK(filename)
        for p in a.get_permissions():
            if p in dangerous_permission:
                d_permission.append(p)
            else:
                n_permission.append(p)

    except:
        logging.warn(
            "androguard can't open the apk: {}".format(result['pgname']))

    result['normal_permission'] = n_permission
    result['danger_permission'] = d_permission

    print ' N ' + result['name']
    print ' V ' + result['version']
    print ' M ' + result['md5']
    print ' S ' + result['size']
    print result['danger_permission']

    return result


def _download_apk(dlink):
    targetapk = urllib.urlopen(dlink)
    return targetapk


def _get_d_url(durl):
    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(durl))
    dclass = soup.find("div", {"class": "download"})
    print " o " + dclass.find("a").get('href')
    dlink = dclass.find("a").get('href')

    return dlink


def _get_apk_name(durl):
    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(durl))
    title = soup.find("div", {"class": "detailInfo mt-5"})
    apk_name = title.find("h3").string

    return apk_name


def _get_apk_attr(durl):
    soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(durl))
    ppt = soup.find("div", {"class": "property mt-10"})
    ppts = ppt.findAll("li")
    v = ppts[0].string
    s = ppts[1].string

    vparser = re.compile('(\d[\.\d]*\d)')
    sparser = re.compile('(\d[\.\d]*[MB|GB])')

    version = vparser.findall(v)[0]
    size = sparser.findall(s)[0]

    return version, size


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

        for url in toplist[ts].findAll("a"):
            if url.get('class') == "down":
                try:
                    # slicing package name
                    pkg_name = url.get('href')[20:][:-1]
                    fakeurl = url.get('href')
                    dlink = _get_d_url(fakeurl)
                    targetapk = _download_apk(dlink)
                    apk_name = _get_apk_name(fakeurl)
                    print apk_name
                    version, size = _get_apk_attr(fakeurl)
                    try:
                        result = generate_apk_info(targetapk, rank)
                    except:
                        print "generate_apk_info goes wrong"
                    insert_into_db(result)
                    rank += 1

                except:
                    print "download failed"
