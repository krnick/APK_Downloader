# APK_Downloader
use google api download apk via python3


Usage:

* Download project

    ```
    git clone https://github.com/krnick/APK_Downloader.git
    ```

* Envirnment setting:
    ```
    $ pipenv shell
    $ pipenv install
    ```
    1. Replace with your account on config/config.py

    2. Login on https://accounts.google.com/b/0/DisplayUnlockCaptcha



* How to use:
    ```
    $ python3 google_play_api_download.py -download package.name
    $ python3 google_play_api_download.py -detail package.name
    ```

* Problem solved :

    need to login on
    https://accounts.google.com/b/0/DisplayUnlockCaptcha
    if show up SecurityCheckError when you modify the code

* Function_description:

    * Download APK via package name
    
    def downloadApkByPackageName(packagename)


    * Search for the closest apk by searching the string
    
    def searchApkByKeyWord(search_word, maximum_search)


    * Get APK details from package name
    
    def getDetailsByPackName(packagename)


    * Get all categories
    
    def browseCategories()


    * Get subcategories through parent categories
    
    def getSubListByCategory(category)

    * Get the corresponding package name through parent classification and sub-category
    
    def getAppBySubList(category, sub_list)

# Download apk from   ( http://m.apk.tw/top )

    * Usage
    ```
    $ pipenv shell
    $ pipenv install
    $ python newmapkpy3.py
    ```

