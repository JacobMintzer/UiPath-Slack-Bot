# -*- coding: utf-8 -*-

import json
from multiprocessing import Pool, TimeoutError
from blocks import Block
from slack import Slack
from user import User
import requests
from pprint import pprint
from flask import Flask, request, make_response, render_template
import asyncio
import threading

app = Flask(__name__)
releaseSelectionDialog=Block.releaseSelectionDialog

global slackClient

#@app.route("/install", methods=["GET"])
def pre_install():
	"""This route renders the installation page with 'Add to Slack' button."""


@app.route("/auth", methods=["GET", "POST"])
def auth():
	slackClient.OpenAuthDialog(request.form)
	return "",200

@app.route("/interact", methods=["GET", "POST"])
def interact():
	requestObj=json.loads(request.form['payload'])
	source=requestObj["view"]["private_metadata"]
	userId=requestObj["user"]["id"]
	print ("source:\n"+source)
	#authentication
	if source=="auth":
		SaveCredentials(requestObj)
		t=threading.Thread(target=slackClient.AddRobot, args=[requestObj])
		t.start()
		return "",200
	#select environemnt release
	elif source=="release":
		user=User(userId)
		data=requestObj["view"]["state"]["values"]
		processID=data["envProcess"]["envProcess"]["selected_option"]["text"]["text"]
		key=user.CreateJob(processID)
		print (str(type(key)))
		t=threading.Thread(target=User.StartJob, args=(user,key))
		t.start()
		print("assume start job ran")
		return "",200
	#process not in environment
	elif source=="process":
		user=User(userId)
		t=threading.Thread (target=processSelected, args=(requestObj, user))
		t.start()
		print("assume process selected ran")
		return "",200
	elif source=="RobotAdd":
		print("Robot add:\n"+json.dumps(requestObj))
		SaveRobot(requestObj)
		return "",200
	else:
		return "",200

@app.route("/run", methods=["GET", "POST"])
def startProcess():
	userId=request.form['user_id']
	print (json.dumps(request.form))
	user=User(userId)
	if (not user.isComplete):
		print ("user is none")
		return "please authenticate using `/auth`", 200
	if request.form["text"]:
		return SearchProcess(request, user, slackClient)
	else:
		return FavoriteProcesses(request, user, slackClient)

def SaveRobot(requestObj):
	user=requestObj["user"]["id"]
	data=requestObj["view"]["state"]["values"]
	robot=data["robot"]["robot"]["value"]
	environment=data["environment"]["environment"]["value"]
	with open("userLib.json",'r') as userLib:
		userData=json.load(userLib)
	if "robots" in userData[user].keys():
		userData[user]["robots"]=[{"robotName":robot,"environment":environment}]
	else:
		userData[user]["robots"].append({"robotName":robot,"environment":environment})
	open("userLib.json",'w').close()
	with open("userLib.json",'w') as userLib:
		json.dump(userData, userLib)

def SaveCredentials(requestObj):
	data=requestObj["view"]["state"]["values"]
	tenant=data["tenant"]["tenant"]["value"]
	email=data["emailOrUsername"]["emailOrUsername"]["value"]
	password=data["password"]["password"]["value"]
	with open("userLib.json",'r') as userLib:
		userData=json.load(userLib)
	userData[requestObj["user"]["id"]] = {"email":email,"password":password,"tenant":tenant}
	open("userLib.json",'w').close()
	with open("userLib.json",'w') as userLib:
		json.dump(userData, userLib)


def processSelected(requestObj, user):
	print("selected")
	data=requestObj["view"]["state"]["values"]
	environmentId=user.GetEnvironment()
	process=data["foundProcess"]["foundProcess"]["selected_option"]["value"]
	envProcessObj=user.GetEnvProcesses()
	for x in envProcessObj:
		if x["ProcessKey"]==process.split(":")[0]:
			key=user.CreateJob(int(x["Id"]))
			user.StartJob(key)
			return
	releaseKey=user.CreateRelease(process, environmentId)
	user.StartJob(releaseKey)


def SearchProcess(request, user, slackClient):
	trigger=request.form['trigger_id']
	searchTerm=request.form["text"]
	processes=user.FilterProcess(searchTerm)
	filteredProcesses=[]
	if len(processes)<1:
		return 	"No processes found",200
	slackClient.SendProcessSelection(processes, trigger)
	return "",200

def FavoriteProcesses(request, user, slackClient):
	trigger=request.form['trigger_id']
	envProcessObj=user.GetEnvProcesses()
	slackClient.SendEnvProcesses(envProcessObj, trigger)
	return "",200

	

#@app.route("/thanks", methods=["GET", "POST"])
def thanks():
	"""
	This route is called by Slack after the user installs our app. It will
	exchange the temporary authorization code Slack sends for an OAuth token
	which we'll save on the bot object to use later.
	To let the user know what's happened it will also render a thank you page.
	"""
	# Let's grab that temporary authorization code Slack's sent us from
	# the request's parameters.
	code_arg = request.args.get('code')
	# The bot's auth method to handles exchanging the code for an OAuth token
	#pyBot.auth(code_arg)
	return render_template("thanks.html")


if __name__ == '__main__':
	slackClient=Slack()
	app.run(debug=True)