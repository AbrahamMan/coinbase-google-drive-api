from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import xml.etree.ElementTree as et
from urllib.parse import urlparse, parse_qs
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/drive.appdata']

class QueueHandler(BaseHTTPRequestHandler):
    def printFiles(self,query_components):
        self.sent = False
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=3000)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            message = et.Element("Error")
            message.text = "Sorry File can't be found contact us. "
            message = et.tostring(message, encoding="utf-8")
            self.set_response(content_type="application/json", data_to_send=message) 
        else:
            print('Files:',query_components['fileName'][0])
            for item in items:

                if ((query_components['fileName'] == item['name']) & (not self.sent)):
                    self.sent = True
                    print(u'{0} ({1})'.format(item['name'], item['id']))
                    file_id = item['id']#'1wCXgJuI_8W1Va7997iBRpOKNtfyra31XsjwShd8v5y8'
                    def callback(request_id, response, exception):
                        if exception:
                            # Handle error
                            print (exception)
                        else:
                            print ("Permission Id: %s" % response.get('id'))

                    batch = service.new_batch_http_request(callback=callback)
                    user_permission = {
                        'type': 'user',
                        'role': 'writer',
                        'emailAddress': query_components['email']
                    }
                    batch.add(service.permissions().create(
                            fileId=file_id,
                            body=user_permission,
                            fields='id',
                    ))
                    domain_permission = {
                        'type': 'domain',
                        'role': 'reader',
                        'domain': 'example.com'
                    }
                    batch.add(service.permissions().create(
                            fileId=file_id,
                            body=domain_permission,
                            fields='id',
                    ))
                    batch.execute()
                    message = et.Element("Success")
                    message.text = "The File "+ query_components['fileName'] + " is sent check your email"
                    message = et.tostring(message, encoding="utf-8")
                    self.set_response(content_type="application/json", data_to_send=message) 
 

    # def do_GET(self): 
    #     if self.path.startswith("/sendFile"):
    #         query_components = parse_qs(urlparse(self.path).query)
    #         self.printFiles(query_components)
    
    def do_POST(self): 
        if self.path.startswith("/sendFile"):
            content_length = int(self.headers['Content-Length']) 
            post_data = json.loads(self.rfile.read(content_length).decode("utf-8")) 
            data_obj = {
                'email': post_data["event"]["data"]['support_email'],
                'fileName': "share me",
                }
            if(post_data["event"]["type"] == 'charge:confirmed' or post_data["event"]["type"] == 'charge:delayed'):    
                self.printFiles(data_obj)
            else:
                message = et.Element("Error")
                message.text = "Waiting for Payment"
                message = et.tostring(message, encoding="utf-8")
                self.set_response(content_type="application/json", data_to_send=message) 
 
                
            
    def set_response(self, content_type="text/plain", data_to_send=b""):

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(data_to_send)


if __name__ == "__main__":
    port = 8000
    with HTTPServer(("127.0.0.1", port), QueueHandler) as httpServer:
        try:
            print("Listening to port " + str(port))
            httpServer.serve_forever()
        except KeyboardInterrupt:
            httpServer.server_close()
            print("Server stopped")
