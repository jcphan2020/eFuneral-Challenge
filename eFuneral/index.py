"""
Challenge codes designed for interview at eFuneral. Basic algorithm is as following:
*   Retrieve all contacts with birthday in this month into list
*   Sort out all contacts in list from closest day to farthest day
*   Loop that keep track of date
*   When day arrives, send message to all contacts and remove this contact from list
*   Loop ends when all contacts removed from list

modules
*   twilio  -   for sending messages
*   csv     -   for reading CSV files
*   dotenv  -   for using .env file to for easy access to environment variables
*   datetime-   for retrieving current time
*   os      -   use with dotenv to retrieve environment variables

Codes by Johnson Phan
"""
from twilio.rest import Client
import csv
import dotenv
import datetime
import os

#   allow the use of .env file
dotenv.load_dotenv()

"""
Function to open file and retrieve contacts. Algorithm looks at 'Date of Birth' or index 8
and check if the birthday month matches this month. If so add to list, otherwise skip it.
Returns the list.
"""
def retrieve_data(file):
    #   Open file and store as variable 'csv_file'
    with open(file) as csv_file:
        lst = []
        #   Read CSV file
        csv_reader = csv.reader(csv_file, delimiter=',')
        skip = True
        for row in csv_reader:
            #   Skip the first row
            if skip:
                skip = False
                continue
            #   Confirm if contact birthday is on this month and store in a list
            data_date = row[8].split('/')
            current_date = datetime.datetime.now()
            if int(data_date[0]) == current_date.month:
                lst.append(row)
    return lst

"""
Function based on the mergeSort algorithm. Very common and efficient.
This works with the Merge function.
"""
def mergeSort(lst):
    n = len(lst)
    if n <= 1:
        return lst
    A = []
    for i in range(0, int(n/2)):
        A.append(lst[i])
    B = []
    for i in range(int(n/2), n):
        B.append(lst[i])
    return Merge(mergeSort(A), mergeSort(B))

"""     Used in the mergeSort algorithm     """
def Merge(A, B):
    p = len(A)
    q = len(B)
    arr = []
    i, j = 0, 0
    while i < p and j < q:
        first = int((A[i][8].split('/'))[1])
        second = int((B[j][8].split('/'))[1])
        if first <= second:
            arr.append(A[i])
            i += 1
        else:
            arr.append(B[j])
            j += 1
    if i >= p:
        for k in range(j, q):
            arr.append(B[k])
    else:
        for k in range(i, p):
            arr.append(A[k])
    return arr

"""
Function to send text messages to contact. Using environment variables to access Twilio,
Contact mobile phone or index 3 is used. If mobile phone is not available, then contact is
skipped.
"""
def send_message(contact):
    #   Get stored string from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    #   Set Twilio for messaging and get mobile phone number stored in index 3
    client = Client(account_sid, auth_token)
    contact_phone = contact[3]
    #   If phone number exist, then send message
    if len(contact_phone) == 10:
        message = client.messages.create(
            body='Happy Birthday from eFuneral! {}, I see that it\'s your birthday month. I hope you have an awesome month!'.format(contact[0]),
            from_='+1{}'.format(twilio_phone),
            to='+1{}'.format(contact_phone)
        )
        print(message.sid)

""" Main algorithm """
def operation():
    #   Retrieve all contacts for this month
    result = retrieve_data(os.getenv('DATASET'))
    #   Sort contacts from closest day to furthest
    result = mergeSort(result)
    #   Loop and wait until the contacts birthday and send the message at the registered time then remove contact from list
    while len(result) > 0:
        date = datetime.datetime.now()
        day = int((result[0][8].split('/'))[1])
        if date.day == day and date.hour == int(os.getenv('SEND_HOUR')) and date.minute >= int(os.getenv('SEND_MINUTE')):
            send_message(result[0])
            del result[0]

if __name__ == "__main__":
    operation()