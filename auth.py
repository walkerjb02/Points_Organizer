from __future__ import print_function
from google.oauth2 import service_account


SCOPESSHEETS = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

SCOPESFORMS = [
'https://www.googleapis.com/auth/drive',
'https://www.googleapis.com/auth/forms',
]

SCOPESDRIVE = [
'https://www.googleapis.com/auth/drive',
'https://www.googleapis.com/auth/drive.file'
]

####Needs to be updated with each new copy####

credentialssheets = service_account.Credentials.from_service_account_file('accounting-society-points-8d4040109cab.json', scopes=SCOPESSHEETS) #Sheets json key
credentialforms = service_account.Credentials.from_service_account_file('accounting-society-points-399ffc5a6f83forms.json', scopes=SCOPESFORMS) #Forms json key
credentialdrive = service_account.Credentials.from_service_account_file('accounting-society-points-8710f6b2821f.json', scopes=SCOPESDRIVE) #Forms json key
