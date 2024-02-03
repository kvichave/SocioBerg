import requests,json
def accountsel(ACCESS_TOKEN,forApp):
    
    if forApp=='instagram':
        pagesid='https://graph.facebook.com/v18.0/me/accounts?fields=name,id,picture&access_token='+ACCESS_TOKEN
        data=requests.get(pagesid).json()
        return data
        