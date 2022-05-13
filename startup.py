import getpass
import sys
import os
import datetime as dt
from googleapiclient.http import MediaIoBaseDownload
from form import result
import json
from googleapiclient.discovery import build,MediaFileUpload
from auth import credentialforms
import uuid
import tkinter as tk
from PIL import ImageTk, Image
import io

def resetsys():
    def initformstorage():
        with open('FormStorage1.json', 'w') as file:
            file.write("""{"files":[]}""")
    initformstorage()
    def initpointtotalstorage():
        with open('Pointtotals.json','w') as file:
            file.write("""{"pointtotals":[]}""")
    initpointtotalstorage()
    def initemail():
        with open('Storage.json','w') as file:
            file.write("""{"emails": []}""")
    initemail()
    def initMAC():
        with open('MAC.json', 'w') as nfile:
            nfile.write("""{"MAC": []}""")
    initMAC()

def get_MAC():
    MACNOW = str(uuid.getnode())
    with open('MAC.json','r') as file:
        ORIMAC = json.load(file)
        maxsupporteddevices = 1
        if len(ORIMAC["MAC"]) < maxsupporteddevices:
            ORIMAC["MAC"].append(str(MACNOW))
            with open('MAC.json', 'w') as nfile:
                nfile.write(json.dumps(ORIMAC))
        elif len(ORIMAC["MAC"]) == 0:
            resetsys()
            ORIMAC["MAC"].append(str(MACNOW))
            with open('MAC.json', 'w') as nfile:
                nfile.write(json.dumps(ORIMAC))
        else:
            if MACNOW in ORIMAC["MAC"]:
                update_results()
            else:
                root = tk.Tk()
                canvas1 = tk.Canvas(root, width=160, height=20, bg='#006df2', relief='groove',
                                    bd=10)
                canvas1.pack()
                image = r'C:\Users\gsbaw\PycharmProjects\PointsOrganizer\background.png'  # TODO FIX FILEPATH
                img = ImageTk.PhotoImage(Image.open(image))
                panel = tk.Label(root, image=img)
                panel.place(x=0, y=0)
                label1 = tk.Label(root, text="Failed Product Verification", bg='#464a4f', fg='white',
                                  font=('Aharoni', 8, 'bold'), width=20)
                canvas1.create_window(90, 20, window=label1)
                root.title("Failed Product Verification")
                root.mainloop()
                sys.exit()

def update_results():
    def get_drive():
        page_token = None
        lst = []
        while 1:
            drive_service = build('drive', 'v3',
                                  credentials=credentialforms)  # TODO make generalized keys before send out
            response = drive_service.files().list(q="mimeType='application/json'",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()
            for file in response.get('files', []):
                lst.append(file.get('id'))
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        file_id = lst[-1]
        print(file_id)
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    result()

    def remove_from_get():
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
        with open('FormStorage1.json', 'r+') as file:
            fal = json.load(file)
            fle = fal["files"][0]
            indexer = 0
            while indexer < len(fle):
                service = build('forms', 'v1', credentials=credentialforms, discoveryServiceUrl=DISCOVERY_DOC,
                                static_discovery=False)
                iDform = list(fle.values())[indexer]
                forminfo = service.forms().get(formId=iDform).execute()
                results = service.forms().responses().list(formId=iDform).execute()
                try:
                    response = results["responses"]
                    lastdate = response[-1]["lastSubmittedTime"][:10:]
                    crntdate = str(dt.date.today())
                    frmname = forminfo["info"]["title"]
                    frmid = forminfo["formId"]
                    responsethreshold = 0
                    if len(response) > responsethreshold:
                        if int(lastdate[-2::]) + 2 < int(crntdate[-2::]) and int(crntdate[5:7]) == int(
                                lastdate[5:7:]) or int(lastdate[-2::]) + 1 > int(crntdate[-2::]) and int(
                                crntdate[5:7]) > int(lastdate[5:7:]):
                            del fle[f"{frmname}"]
                        else:
                            pass
                except KeyError:
                    indexer += 1
                    continue
            fle = json.dumps(fal)
            with open('FormStorage1.json', 'w') as file1:
                file1.write(fle)

    remove_from_get()

    def to_drive(): #TODO fix so it sends out file
        drive_service = build('drive', 'v3', credentials=credentialforms)  # TODO make generalized keys before send out
        file_metadata = {'name': 'FormStorage1.json'}
        media = MediaFileUpload('FormStorage1.json', mimetype='application/json')
        drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()


    def to_sheet():
        pass


def add_to_startup(file_path=""):
    USER_NAME = getpass.getuser()
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_pathwin = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(USER_NAME)
    bat_pathaapl = r"" #TODO make apple compatible version
    with open(bat_pathwin + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" {}'.format(file_path) + '\main.py\n') #TODO ADD SO IT RUNS APPLICATION NOT JUST MAIN.PY


def remove_from_startup():
    USER_NAME = getpass.getuser()
    bat_path = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(USER_NAME)
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write('')
