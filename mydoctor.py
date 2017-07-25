#!/usr/bin/env python
import requests
import json
import urllib
from flask import Flask, jsonify
from flask import request
from flask import abort
from flask import Response
from datetime import datetime
from datetime import time as newtime
from datetime import date
from flask_cors import CORS, cross_origin
import calendar
import os.path
import re
import random
from pymongo import MongoClient
import sys
import time
from datetime import datetime
from pytz import timezone
from time import sleep
import pytz

AUTHBot = 'Njk1YTMyNWUtNzg5Zi00ZmNmLWE4ZGYtMzkwYjNkMGViNWM4NjVmOWQzODMtYjgw'
HEADERSBot = {'Authorization': 'Bearer ' + AUTHBot}
headersCliniko= {'Content-Type': 'application/json','Accept': 'application/json','User-Agent': 'mydoctor(support@kiduku.io)'}
BASE_URL = "https://api.ciscospark.com/v1/"
ROOMS_URL = BASE_URL + "rooms"
MESSAGES_URL = BASE_URL + "messages"
WEBHOOKS_URL = BASE_URL + "webhooks"
MEMBERSHIP_URL = BASE_URL + "memberships"
PEOPLE_URL = BASE_URL + "people"
clinikoBase_URL= "https://api.cliniko.com/v1/"
clinkoPatients_URL=clinikoBase_URL+"patients"
clinkoPractitioner_URL=clinikoBase_URL+"practitioners"
clinkoAppointment_URL=clinikoBase_URL+"appointments"
myID = 'safs.nec@gmail.com'
BotId = 'Njk1YTMyNWUtNzg5Zi00ZmNmLWE4ZGYtMzkwYjNkMGViNWM4NjVmOWQzODMtYjgw'
uri= 'mongodb://mydoc:mydoc@ds161262.mlab.com:61262/mydoctor'
app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
client = MongoClient(uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
db = client.get_default_database()

def postMessageBotOneToOne(PersonId, message):
    dict = {"toPersonId": PersonId, "markdown": message}
    resp = requests.post(MESSAGES_URL, json=dict, headers=HEADERSBot)
    roomId = json.loads(resp.text)['roomId']
    return roomId

def createPatient(practiceId,firstName, lastName,dob,userAddress):
    if db.practices.find({"practiceId": practiceId}).count() > 0:
        cursor = db.practices.find_one({"practiceId": practiceId}, {"vendorName": 1,"apiKey": 1, "_id": 0})
        vendorName=cursor["vendorName"]
        apiKey=cursor["apiKey"]
        if vendorName == "cliniko":
            dict = {"first_name": firstName, "last_name": lastName,"date_of_birth":dob,"address_1":userAddress}
            resp = requests.post(clinkoPatients_URL, json=dict, headers=headersCliniko,auth=(apiKey,''))
            patientId = json.loads(resp.text)['id']
            return patientId

def getPractitionerDetails(practiceId,first_name):
    if db.practices.find({"practiceId": int(practiceId)}).count() > 0:
        cursor = db.practices.find_one({"practiceId": int(practiceId)}, {"vendorName": 1,"apiKey": 1, "_id": 0})
        vendorName=cursor["vendorName"]
        apiKey=cursor["apiKey"]
        print (apiKey)
        print (vendorName)
        if vendorName == "cliniko":
            resp = requests.get(clinkoPractitioner_URL, headers=headersCliniko,auth=(apiKey,''))
            practitioners = json.loads(resp.text)['practitioners']
            print (practitioners)
            for p in practitioners:
                if p["first_name"]== first_name:
                    practitionerId=p["id"]
                    practitionerFirstname=p["first_name"]
                    practitionerLastname = p["last_name"]
                    practitionerTitle = p["title"]
                    practitionerDesignation  = p["designation"]
                    return practitionerId,practitionerFirstname,practitionerLastname,practitionerTitle,practitionerDesignation

def getPractitionerDetailID(practiceId,practitionerId):
    if db.practices.find({"practiceId": int(practiceId)}).count() > 0:
        cursor = db.practices.find_one({"practiceId": int(practiceId)}, {"vendorName": 1,"apiKey": 1, "_id": 0})
        vendorName=cursor["vendorName"]
        apiKey=cursor["apiKey"]
        if vendorName == "cliniko":
            clinkoPractitionerone_URL=clinkoPractitioner_URL+"/"+practitionerId
            resp = requests.get(clinkoPractitionerone_URL, headers=headersCliniko,auth=(apiKey,''))
            practitionerFirstname=json.loads(resp.text)["first_name"]
            practitionerLastname = json.loads(resp.text)["last_name"]
            practitionerTitle = json.loads(resp.text)["title"]
            practitionerDesignation  = json.loads(resp.text)["designation"]
            return practitionerFirstname,practitionerLastname,practitionerTitle,practitionerDesignation

def getPracticeIdDrName(first_name):
    cursor = db.practices.find({}, {"practiceId":1,"vendorName": 1,"apiKey": 1, "_id": 0})
    for doc in cursor:
        vendorName=doc["vendorName"]
        apiKey=doc["apiKey"]
        practiceId = doc["practiceId"]
        if vendorName == "cliniko":
            resp = requests.get(clinkoPractitioner_URL, headers=headersCliniko,auth=(apiKey,''))
            practitioners = json.loads(resp.text)['practitioners']
            for p in practitioners:
                if p["first_name"]== first_name:
                    return practiceId

def getAvailabletime(practiceId,practitionerId,vendorId,appointmentDate,appointment_type):
    if db.practices.find({"practiceId": practiceId}).count() > 0:
        cursor = db.practices.find_one({"practiceId": practiceId}, {"vendorName": 1,"apiKey": 1, "_id": 0})
        vendorName=cursor["vendorName"]
        apiKey=cursor["apiKey"]
        if vendorName == "cliniko":
            getavailabletimeUrl=clinikoBase_URL+'businesses/'+str(vendorId)+'/practitioners/'+str(practitionerId)+'/appointment_types/'+str(appointment_type)+'/available_times?from='+appointmentDate +'&to='+appointmentDate
            print (getavailabletimeUrl)
            resp = requests.get(getavailabletimeUrl, headers=headersCliniko,auth=(apiKey,''))
            print (resp.text)
            available_times = json.loads(resp.text)["available_times"]
            return available_times

def createAppointment(practiceId,date,patientId, practitioerId,appointment_type_id,vendorId):
    if db.practices.find({"practiceId": practiceId}).count() > 0:
        cursor = db.practices.find_one({"practiceId": practiceId}, {"vendorName": 1,"apiKey": 1, "_id": 0})
        vendorName=cursor["vendorName"]
        apiKey=cursor["apiKey"]
        if vendorName == "cliniko":
            dict = {"appointment_start": date, "patient_id": patientId,"practitioner_id":practitioerId,"appointment_type_id":appointment_type_id,"business_id":vendorId}
            resp = requests.post(clinkoAppointment_URL, json=dict, headers=headersCliniko,auth=(apiKey,''))
            appointmentId = json.loads(resp.text)['id']
            return patientId

def convertAvailabletime(strdatetime):
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    timeonlyfmt="%H:%M:%S"
    sourcetime = datetime.strptime(strdatetime, fmt)
    utcsourcetime = sourcetime.replace(tzinfo=timezone('UTC'))
    convertedlocaltime = utcsourcetime.astimezone(timezone('Australia/Adelaide'))
    return convertedlocaltime.strftime(timeonlyfmt)

def convertTimezone(strdatetime,srctz,dsttz):
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    sourcetime = datetime.strptime(strdatetime, fmt)
    tzsourcetime = sourcetime.replace(tzinfo=timezone(srctz))
    convertedtime = tzsourcetime.astimezone(timezone(dsttz))
    return convertedtime

def toUTC(strdatetime,tz):
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    datetimeinutc= tz.normalize(tz.localize(datetime.strptime(strdatetime, fmt))).astimezone(pytz.utc)
    return datetimeinutc.strftime(fmt)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/fullfillment', methods=['POST'])
def firehosehook():
    if not request.json:
        abort(400)
    else:
        personId = request.json["originalRequest"]["data"]["data"]["personId"]
        try:
            action = request.json["result"]["action"]
        except:
            action =""
            pass
        personidUrl = PEOPLE_URL + '/' + personId
        resp = requests.get(personidUrl, headers=HEADERSBot)
        try:
            firstName = json.loads(resp.text)['firstName']
        except:
            firstName = ""
            pass
        try:
            lastName = json.loads(resp.text)['lastName']
        except:
            lastName = ""
            pass
        if action == "input.welcome" and db.users.find({"personId": personId}).count() == 0:
            postMessageBotOneToOne(personId, "Hello **"+firstName+"**! "+'I am Mydoctor Bot and I can be your personal assistant to help you to:\n\n- Find a GP near to you and book appointments for you \n\n- Remind you about your medical appointments \n\n- Alert you about your appointment recalls\n\n- Book a ride for appointment (not yet but soon..) **')
            data = {
                'speech': 'It looks like I did not serve you before. I know little about yourself, but to become your assistant, I would like to know more about yourself, would you like to proceed?',
                'displayText': 'It looks like I did not serve you before. I know little about yourself, but to become your assistant, I would like to know more about yourself, would you like to proceed?',
                'data':{},
                'contextOut':[{"name":"Welcome-followup", "lifespan":1, "parameters":{}}],
                'source':""
            }
        elif action == "input.welcome" and db.users.find({"personId": personId}).count() > 0:
            cursor = db.users.find_one({"personId": personId},{"firstName": 1, "_id": 0})
            firstName=cursor["firstName"]
            data = {
                'speech': 'Hey '+firstName+'! how can I help you today?',
                'displayText': 'Hey '+firstName+'! how can I help you today?',
                'data': {},
                'contextOut': [{"name": "appointment_booking", "lifespan": 1, "parameters": {}}],
                'source': ""
            }
        elif action == "useronboarding.yes":
            postMessageBotOneToOne(personId, "Thats Awesome!, let me ask few questions now.")
            data = {
                'speech': "",
                'displayText': "",
                'data':{},
                "followupEvent": {"name": "user-data-collection-event", "data": {"firstName":firstName,"lastName":lastName,"dob":"","userAddress":""}},
                'contextOut':[],
                'source':""
            }
        elif action == "userdatacollection.done":
            userData=request.json["result"]["parameters"]
            firstName=userData["firstName"]
            userData.update({"personId":personId,"practices":[]})
            result = db.users.insert_one(userData)
            if result.inserted_id:
                data = {
                    'speech': "Thanks "+firstName+"! I have saved your details, How can I help you today?",
                    'displayText': "Thanks "+firstName+"! I have saved your details, How can I help you today?",
                    'data': {},
                    "followupEvent": {},
                    'contextOut': [{"name": "appointment_booking", "lifespan": 1, "parameters": {}}],
                    'source': ""
                }
            else:
                data = {
                    'speech': "Sorry we are experiencing some technical problems",
                    'displayText': "Sorry we are experiencing some technical problems",
                    'data': {},
                    "followupEvent": {},
                    'contextOut': [],
                    'source': ""
                }
        elif action == "appointment.book":
            #postMessageBotOneToOne(personId, "No problems, I can help you with that.")
            appointmentData = request.json["result"]["parameters"]
            appointmentDate=appointmentData["appointmentDate"]
            practitionerName = appointmentData["practitionerName"]
            time = appointmentData["time"]
            appointment_type=0
            practiceId = getPracticeIdDrName(practitionerName)
            patientId=None
            cursor = db.users.find_one({"personId": personId},{"firstName": 1, "lastName": 1, "dob": 1, "userAddress": 1,"practices":1, "_id": 0})
            praccursor = db.practices.find_one({"practiceId": practiceId}, {"practiceName": 1, "Address": 1, "vendorId":1,"services":1,"_id": 0})
            for prac in praccursor["services"]:
                if prac["name"] == "Generic":
                    appointment_type = prac["appointment_type"]
            for pracs in cursor["practices"]:
                if pracs["practiceId"] ==practiceId:
                    patientId = pracs["patientId"]
            if not patientId:
                #postMessageBotOneToOne(personId, "it seems like you haven't been to any of our registered practices, let me add your details first")
                patientId=createPatient(practiceId, cursor["firstName"], cursor["lastName"], cursor["dob"], cursor["userAddress"])
                result = db.users.update(
                    {"personId": personId},
                    {"$push":{'practices': {"practiceId": practiceId,"patientId":patientId}}}
                )
                #if patientId and result['nModified']>0:
                    #postMessageBotOneToOne(personId, "All good. I have added your details into "+praccursor["practiceName"])
            practitionerId, practitionerFirstname, practitionerLastname, practitionerTitle, practitionerDesignation=getPractitionerDetails(practiceId, practitionerName)
            #postMessageBotOneToOne(personId,"\n\nLet me check **" +practitionerTitle+"."+practitionerFirstname+"**'s availability. Please hang on")
            available_times=getAvailabletime(practiceId, practitionerId, praccursor["vendorId"], appointmentDate,appointment_type)
            convertedAvailabletimes=[]
            message_slot=""
            if len(available_times)>0:
                i=1
                for a_t in available_times:
                    available_time=convertAvailabletime(a_t["appointment_start"])
                    message_slot= message_slot+'\n\n- Slot '+str(i)+' :' +available_time
                    i=i+1
                    convertedAvailabletimes.append(available_time)
                combineddate = appointmentDate + "T" + time + "Z"
                #print ('booking local time is ' + combineddate)
                booking_utc = toUTC(combineddate, timezone('Australia/Adelaide'))

                if time in convertedAvailabletimes:
                    postMessageBotOneToOne(personId, "Yes, **Dr. "+practitionerFirstname+ "** will be able to see you at "+time)
                    print ('booking converted time in UTC is '+booking_utc)
                    data = {
                        'speech': "",
                        'displayText': "",
                        'data': {},
                        "followupEvent": {"name": "booking-confirmation-event","lifespan": 5,"data": {"practiceId": str(practiceId), "appointmentTime": booking_utc, "patientId": str(patientId),"practitionerId": str(practitionerId),"appointmentType": str(appointment_type),"vendorId":str(praccursor["vendorId"])}},
                        'contextOut': [],
                        'source': ""
                    }
                else:
                    postMessageBotOneToOne(personId,
                                           "Sorry, **Dr." + practitionerFirstname + "** is not available at the time you have requested, below are the available timeslots you can book"+message_slot)

                    data = {
                        'speech': '',
                        'displayText': '',
                        'data': {},
                        "followupEvent": {"name": "appointment-selection_event", "lifespan": 5,
                                          "data": {"practitionerName": practitionerName, "appointmentDate": appointmentDate}},
                        'contextOut': [],
                        'source': ""
                    }
            else:
                data = {
                    'speech': "Sorry, there are no free slots available to book. please try again with new dates",
                    'displayText': "Sorry, there are no free slots available to book. please try again with new dates",
                    'data': {},
                    "followupEvent": {},
                    'contextOut': [{"name": "appointment_booking", "lifespan": 1, "parameters": {}}],
                    'source': ""
                }
        elif action == "booking.confirm.yes":
            postMessageBotOneToOne(personId, "Thats Awesome!, let me proceed with your booking now")
            appointmentType = request.json["result"]["parameters"]["appointmentType"]
            appointmentTime = request.json["result"]["parameters"]["appointmentTime"]
            patientId = request.json["result"]["parameters"]["patientId"]
            practiceId = request.json["result"]["parameters"]["practiceId"]
            vendorId = request.json["result"]["parameters"]["vendorId"]
            practitionerId = request.json["result"]["parameters"]["practitionerId"]
            praccursor = db.practices.find_one({"practiceId": int(practiceId)},
                                               {"practiceName": 1, "Address": 1, "vendorId": 1, "services": 1,
                                                "_id": 0})
            practitionerFirstname, practitionerLastname, practitionerTitle, practitionerDesignation=getPractitionerDetailID(practiceId,practitionerId)
            appointmentId = createAppointment(int(practiceId), appointmentTime, int(patientId), int(practitionerId),appointmentType,int(vendorId))
            if appointmentId:
                postMessageBotOneToOne(personId,
                                       "\n\nThank you for your patience. Your booking is confirmed. Your booking details are:\n\n" +"**Booking ID:"+str(appointmentId)+"**\n\n"+"**Practitioner Details :"+practitionerTitle + "." + practitionerFirstname+ " "+practitionerLastname+ "**\n\n**Appointment Time:"+appointmentTime+"**\n\n**Practice Name:"+praccursor["practiceName"]+"**\n\n**Practice address:"+praccursor["Address"]+"**")
                data = {
                    'speech': '',
                    'displayText': '',
                    'data': {},
                    'contextOut': [{"name": "appointment_booking", "lifespan": 1, "parameters": {}}],
                    'source': ""
                }
            else:
                data = {
                    'speech': 'Sorry, I could not book this appointment,Can you please ping me little later?',
                    'displayText': 'Sorry, I could not book this appointment,Can you please ping me little later?',
                    'data': {},
                    'contextOut': [{"name": "appointment_booking", "lifespan": 1, "parameters": {}}],
                    'source': ""
                }
        else:
            data={}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers["Content-Type"] = "application/json"
        return resp

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        print('closing connection....')


