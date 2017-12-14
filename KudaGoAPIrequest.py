import requests
import time

def getDigest(city, event_id, *kwargs):
    datetime = int(time.time() // 1)

    print(kwargs)
    ids=''
    if(len(kwargs)>0):
        ids = ','.join(*kwargs)

    url = """https://kudago.com/public-api/v1.3/events/?location=%s&text_format=plain&&actual_since=%s
            &fields=id,short_title,description,site_url&categories=%s&ids=%s
           """ % (city, datetime, event_id, ids)
    headers = {'Content-Type': 'application/json'}
    r = requests.get(url, '', headers=headers)
    dic = r.json()
    return(dic['results'])

