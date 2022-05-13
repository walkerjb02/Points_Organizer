from __future__ import print_function
from googleapiclient.discovery import build
from auth import credentialforms
import json


drive_service = build('drive', 'v3', credentials=credentialforms) #TODO make generalized keys before send out
forms_service = build('forms', 'v1', credentials=credentialforms) #TODO make generalized keys before send out


def callback(response, exception):
    if exception:
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


def add_email():
    batch = drive_service.new_batch_http_request(callback=callback)
    with open('Storage.json', 'r') as mail:
        jon = json.load(mail)["emails"]
        m = 0
        while m < len(jon):
            with open('FormStorage1.json', 'r') as mfile:
                mfile = json.load(mfile)["files"]
                user_permission = {
                    "type": "user",
                    "role": "writer",
                    "emailAddress": f"{jon[m]}",
                }
                i = 0
                while i < len(mfile):
                    for j in mfile[i].values():
                        batch.add(drive_service.permissions().create(
                            fileId=f"{j}",
                            body=user_permission,
                            fields="id",
                            sendNotificationEmail=True))
                    i += 1
            batch.execute()
            m += 1


def createform(title, description):
    form = {"info": {"title": f"{title}", 'documentTitle': f'{description}'}, }
    createResult = forms_service.forms().create(body=form).execute()
    return createResult['formId']


def result():
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    with open('FormStorage1.json', 'r+') as file:
        fle = json.load(file)["files"]
        indexer = 0
        while indexer < len(fle):
            service = build('forms', 'v1', credentials=credentialforms, discoveryServiceUrl=DISCOVERY_DOC,
                            static_discovery=False)
            iDform = list(fle[indexer].values())[indexer]
            forminfo = service.forms().get(formId=iDform).execute()
            results = service.forms().responses().list(formId=iDform).execute()
            def get_IDdx():
                try:
                    main = results["responses"][0]["answers"]
                    qidlst = (list(main.keys()))
                    i = 0
                    while i < len(qidlst):
                        answer = main[qidlst[i]]["textAnswers"]["answers"][0]["value"]
                        if '' in str(answer[0:3]):
                            try:
                                int(answer[-4::])
                            except ValueError:
                                continue
                            return i
                        i += 1

                except KeyError:
                    pass
            try:
                desc = forminfo["info"]["description"]
            except KeyError:
                indexer += 1
                continue
            with open('Pointtotals.json', "r+") as rfile:
                unfilterpoint = json.load(rfile)
                points = unfilterpoint["pointtotals"]
                i = 0
                try:
                    while i < len(points):
                        point = str(points[i].keys())[12:-3:]
                        if str(point) in desc or str(
                                point).lower() in desc or f"{point[0]}{point[point.index(' ') + 1]}" in desc or f"{point[0]}.{point[point.index(' ') + 1]}." in desc or f"{point[0].lower()}{point[point.index(' ') + 1].lower()}" in desc or f"{point[0]}{point[point.index(' ') + 1].lower()}" in desc or f"{point[0]}.{point[point.index(' ') + 1].lower()}." in desc:
                            finalpoint = point
                            lst = [desc[desc.index(point[0]) - (n + 1)] for n in range(6)[::-1]]
                            numlst = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
                            indexernum = 0
                            while indexernum < len(numlst):
                                if numlst[indexernum] in ''.join(lst)[::].lower():
                                    amount = numlst.index(numlst[indexernum]) + 1
                                    if numlst.index(numlst[indexernum]) > 10:
                                        amount = numlst.index(numlst[indexernum]) - 9
                                    break
                                else:
                                    indexernum += 1
                            idx = get_IDdx()
                            nexer = 0
                            while nexer < len(results["responses"]):
                                main = results["responses"][nexer]["answers"]
                                timestamp = results["responses"][nexer]["lastSubmittedTime"]
                                psuiD = main[list(main.keys())[idx]]["textAnswers"]["answers"][0]["value"]
                                for categories in points:
                                    for keys in categories:
                                        if finalpoint in keys:
                                            ptdct = points[finalpoint.index(finalpoint)][f"{finalpoint}"][1]
                                            if psuiD not in list(ptdct.keys()):
                                                ptdct[psuiD] = [[str(timestamp)], int(amount)]
                                            elif psuiD in list(ptdct.keys()):
                                                if timestamp in ptdct[psuiD][0]:
                                                    pass
                                                else:
                                                    ptdct[psuiD][0].append(timestamp)
                                                    ptdct[psuiD][1] += amount
                                    with open('Pointtotals.json', 'w') as ffile:
                                        ffile.write(json.dumps(unfilterpoint))
                                nexer += 1
                        i += 1
                except ValueError:
                    pass
            indexer += 1
