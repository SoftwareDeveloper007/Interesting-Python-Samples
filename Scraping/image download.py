import urllib.request, urllib.error
import shutil
import re
import MySQLdb as mdb
from time import sleep


def download(url, num_retries=3):
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
        print(e.code)
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)

        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                download(url, num_retries-1)

        # ...
        print('URLError')
    else:
        with urllib.request.urlopen(str(url)) as response, open(
                        'C:/Users/Lion/Downloads/' + str(j), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print('good')

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'passion1989'
DB_NAME = 'test'

con = mdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
with con:
    cur = con.cursor()
    #sql = "SELECT DISTINCT longitude, latitude FROM OBIS_occurances WHERE GeoName is null"
    #sql = "SELECT messageID, Body FROM test.newTable ORDER BY Body LIMIT 237, 100000"
    sql = "SELECT messageID, Body FROM test.newTable WHERE messageID=60846"

    cur.execute(sql)
    print(cur._last_executed)

    results = cur.fetchall()
    print(results)
    i = 0
    for rows in results:
        i += 1
        #string ="  1 - $25 gift card to Your Fish Stuff    &nbsp;    [image]http://i693.photobucket.com/albums/vv292/jzech/948f2696-28a8-45f8-a689-13ae7d518e05_zpsloiaznbg.png[/image]    &nbsp;    &nbsp;    1 - $25 gift certificate to Saltwaterfish.com    &nbsp;    [image]http://i693.photobucket.com/albums/vv292/jzech/logo_zpsvbnne5ou.png[/image]    &nbsp;   &nbsp;1 - 4 Stage Value Plus BRS RO system   &nbsp;   [image]https://s3.amazonaws.com/BRS-Banners/BRS_Universal_Series_480x60_v2.gif[/image]&nbsp;"
        try:
            urls = re.findall("https?://\S+?\.(?:jpg|jpeg|gif|png)", str(rows[1]))
            #urls = re.findall("https?://\S+?\.(?:jpg|jpeg|gif|png)", string)
            print(i)
            for url in urls:
                urls = url+"?sort=3&o=0&ref=1"
                print(url)
                sleep(5)
                c = url.split("/", 99)
                d = len(c)
                e = (c[int(d - 2)])
                f = (c[int(d - 1)])
                # print(e)
                # print(f)
                j = str(rows[0]) + "&_#" + str(e) + "#_&" + str(f)
                print("filename: " + j)

                download(url)


        except Exception:
            print("expection"+Exception)
            pass

print('All Done Successfully')

