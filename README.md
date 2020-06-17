# Integration coinbase with Google Drive API integration 

Welcome to Integration coinbase with Google Drive API integration repository. This repository will be used to send different Google drive files using email that I will be guiding you through. and in about five minutes you'll have a simple Python server application that listen and send
requests to the Google People API.

## From Google Developer Console activate Google Drive API and download credentials.json file which looks like this 👇.

```
{
    "web": {
        "client_id": "CLIENT_ID",
        "project_id": "PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "CLIENT_SECRET"
    }
}
```

## create an account https://commerce.coinbase.com and it will automatically create a wallet for you.


Oh! I haven't introduced this is Abraham ✋😀


## how to use it in coinbase
then coinbase Dashboard go to Settings > Webhook subscriptions add your url use ⭐ngrok ⭐to access you localhost globally. ngrok will generate a link for you example 👉 [https://c189f880d352.ngrok.io/sendFile]

```
./ngrok http 8000
```

Oh! I haven't introduced this is Abraham ✋😀

## Install

```
pip install -r requirements.txt
```

## Run

After following the quickstart setup instructions, run the sample:

```
python3 server.py
```