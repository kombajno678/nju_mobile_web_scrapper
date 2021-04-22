# scrapper
import requests
from lxml import html
import time

PHONE_NR = "123456789"
PASSWORD = "password"


print("initializing ...")

sleep_time = 2
maxFetchTries = 5

# https://www.njumobile.pl/logowanie?backUrl=/mojekonto/stan-konta
session_requests = requests.session()

login_url = "https://www.njumobile.pl/logowanie?backUrl=/mojekonto/stan-konta"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='_dynSessConf']/@value")))[0]

post_url = "https://www.njumobile.pl/logowanie?_DARGS=/profile-processes/login/login.jsp.portal-login-form"

payload = {
    "login-form": PHONE_NR, 
    "password-form": PASSWORD, 
    "/ptk/sun/login/formhandler/LoginFormHandler.backUrl": "/mojekonto/stan-konta",
    "_dynSessConf": authenticity_token,
    "_dyncharset": "UTF-8",
    "login-submit": "zaloguj się",
    "_DARGS": "/profile-processes/login/login.jsp.portal-login-form",
    "_D:/ptk/sun/login/formhandler/LoginFormHandler.backUrl": "",
    "/ptk/sun/login/formhandler/LoginFormHandler.hashMsisdn": "",
    "_D:/ptk/sun/login/formhandler/LoginFormHandler.hashMsisdn": "",
    "_D:login-form": "",
    "_D:password-form": "",
    "_D:login-submit": "",

}

headers = {
    #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #"Accept-Encoding": "gzip, deflate, br",
    #"Accept-Language": "en-GB,en;q=0.9,pl;q=0.8,en-US;q=0.7",
    #"Content-Type": "application/x-www-form-urlencoded",
    #"Cookie": DMP=DMP-NJU--2020.10.15.12.21.02.212-gxyLxKktNl; USID=44a62e38e822e0d717aa993f15bead7b; _fbp=fb.1.1602757271824.113644313; DMP_PROFILE_ID=ac232cbf9e55e1d95212f02a34be792b58ce59b14a18943017c443b249cd617d; DMP_HASH_GLOBAL_ID_2=6380E39D052A8400F12FBC9C013764CF76B6BDCD61DB02421487A8C75205BAAE; _snrs_uuid=21b378da-32c3-4a2c-aeef-b1e8b0ddc6e3; _snrs_puuid=21b378da-32c3-4a2c-aeef-b1e8b0ddc6e3; high-contrast=false; userAccessCookie=f6725115ba5748f5bacf51d959787f42acf63858; TS3f940b6d027=08cb46268eab2000acb00d14c4b42faa11d3e46dea60a2c268564d95d3fd84d551b4129b095df71408201c1389113000efd204e7e980b30b14043a290546e6e8c4b7c1c19efb408dd85efd9ec5515a5069267426470f2af19b942ff57dd90b7b; SECURED_SESSION_TOKEN=; JSESSIONID=2252D83D2C9DD9AC0C6B9C5969E05918.sunwww305; TS0180bd77=01b0228c7548a59397ffd68015354fb37158fdcb6003f7cb3b9b3f44fa5335c0b5a937cc5d9ffbef3b21bc216eaa0a1ae83efcffe7e15dbf13fba68e4cb8b8cf16b49f9db1bb42aea13aea9bb664a8ed3c3fc356f1756876961c49efe50e16a669e03bb2cfa33344393fbef8ecffefa971a79af3c2cbcfae1346ff6efdec566562a95e9c6d9b71a383b6404fbb298fffe1c48dd15c; _snrs_sa=ssuid:3af323b2-a6e8-459e-a3cb-6ba241932b5f&appear:1612458186&sessionVisits:10; _snrs_sb=ssuid:3af323b2-a6e8-459e-a3cb-6ba241932b5f&leaves:1612458579; _snrs_p=host:www.njumobile.pl&permUuid:21b378da-32c3-4a2c-aeef-b1e8b0ddc6e3&uuid:21b378da-32c3-4a2c-aeef-b1e8b0ddc6e3&emailHash:&user_hash:&init:undefined&last:1612377682.902&current:1612458579&uniqueVisits:13&allVisits:184
    #"Host": "www.njumobile.pl",
    "Origin": "https://www.njumobile.pl",
    #"Pragma": "no-cache",
    "Referer": "https://www.njumobile.pl/logowanie?backUrl=/mojekonto/stan-konta",
    #"save-data": "on",
    #"Sec-Fetch-Dest": "document",
    #"Sec-Fetch-Mode": "navigate",
    #"Sec-Fetch-Site": "same-origin",
    #"Sec-Fetch-User": "?1",
    #"Sec-GPC": "1",
    #"Upgrade-Insecure-Requests": "1",
    #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
}
print("logging in ...")

result = session_requests.post(
    post_url, 
    data = payload, 
    headers = headers
    #headers = dict(referer=login_url)
)
#print('res: {}'.format(result.text))
print("login result: {}".format(result.ok))
print("sleeping for " + str(sleep_time) + " seconds ...")
#time.sleep(sleep_time)
fetched = False
triesLeft = maxFetchTries
while not fetched and triesLeft > 0:
    triesLeft = triesLeft - 1
    try:
        #raise Exception("xdxdxd")
        print("fetching status data ...")

        url = 'https://www.njumobile.pl/mojekonto/stan-konta'
        result = session_requests.get(
            url, 
            headers = dict(referer = url)
        )
        tree = html.fromstring(result.content)

        print("scrapping ...")
        
        money_left = None
        extra_mb_left = None
        when_end = None
        when_extra_end = None
        monthly_gb_left = None

        money_and_pakiet= tree.xpath("//div[@class='small-comment mobile-text-right tablet-text-right']/div/text()")
        if(len(money_and_pakiet) >= 2):
            money_left = money_and_pakiet[0]
            extra_mb_left = money_and_pakiet[1]
    
        when_end_raw = tree.xpath("//div[@class='four columns tablet-six mobile-twelve']/strong/text()")
        if(len(when_end_raw) >= 3):
            when_end = when_end_raw[2]
        when_extra_end_raw = tree.xpath("//div[@class='four columns mobile-six']/strong/text()")
        if(len(when_extra_end_raw) >= 3):
            when_extra_end = when_extra_end_raw[2]
            when_extra_end = when_extra_end[11:21]
        monthly_gb_left_raw = tree.xpath("//div[@class='eleven columns']/p/strong/text()")
        if(len(monthly_gb_left_raw) >= 1):
            monthly_gb_left = monthly_gb_left_raw[0]

        print("===============================================")
        if(money_left is not None):
            print("money left         : " + str(money_left))
        if(monthly_gb_left is not None and when_end is not None):
            print("---")
            print("main gb left       : " + str(monthly_gb_left))
            print("main valid untill  : " + str(when_end))
        if(extra_mb_left is not None and when_extra_end is not None):
            print("---")
            print("extra mb left      : " + str(extra_mb_left))
            print("extra valid untill : " + str(when_extra_end))
        print("================================================")
        fetched = True
        break
    except Exception as e:
        
        print("=============== fetch try " + str(maxFetchTries-triesLeft) + " of " + str(maxFetchTries) + " ================")
        print("error: ")
        print(e)
  
    if fetched :
        break
    else:
        print("sleep 1s before retrying ...")
        time.sleep(1)

if(not fetched):
    print("failed to fetch data after " + str(maxFetchTries-triesLeft) + " tries")
print("(enter to exit)")

wait = input()