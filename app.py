# -*- coding: utf-8 -*-

import json
#import bot
#import commands
#import message
from multiprocessing import Pool, TimeoutError
from blocks import Block
from user import User
import requests
from pprint import pprint
from flask import Flask, request, make_response, render_template
import asyncio
import threading

true=True
false=False
#pyBot = bot.Bot()
#slack = pyBot.client
global eventList
eventList=[]
app = Flask(__name__)
option=Block.option
releaseSelectionDialog=Block.releaseSelectionDialog
processSelectionDialog=Block.processSelectionDialog
authDialog=Block.authDialog

using open("key.txt","r") as file:
	slackToken=file.read()

@app.route("/install", methods=["GET"])
def pre_install():
	"""This route renders the installation page with 'Add to Slack' button."""


@app.route("/interact", methods=["GET", "POST"])
def interact():
	requestObj=json.loads(request.form['payload'])
	source=requestObj["view"]["private_metadata"]
	userId=requestObj["user"]["id"]
	print ("source:\n"+source)
	#authentication
	if source=="auth":
		SaveCredentials(requestObj)
		return "",200

	#select environemnt release
	elif source=="release":
		user=User(userId)
		data=requestObj["view"]["state"]["values"]
		processID=data["envProcess"]["envProcess"]["selected_option"]["text"]["text"]
		key=user.CreateJob(processID)
		t=threading.Thread(target=user.StartJob, args=(key))
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
	else:
		return "",200

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

def SaveCredentials(requestObj):
	data=requestObj["view"]["state"]["values"]
	tenant=data["tenant"]["tenant"]["value"]
	email=data["emailOrUsername"]["emailOrUsername"]["value"]
	environment=data["environment"]["environment"]["value"]
	password=data["password"]["password"]["value"]
	robot=data["robot"]["robot"]["value"]
	with open("userLib.json",'r') as userLib:
		userData=json.load(userLib)
	userData[requestObj["user"]["id"]] = {"email":email,"password":password,"tenant":tenant, "environment":environment, "robot":robot}
	open("userLib.json",'w').close()
	print(json.dumps(userData))
	with open("userLib.json",'w') as userLib:
		json.dump(userData, userLib)

@app.route("/run", methods=["GET", "POST"])
def startProcess():
	userId=request.form['user_id']
	user=User(userId)
	if request.form["text"]:
		return SearchProcess(request, user)
	else:
		return FavoriteProcesses(request, user)

def SearchProcess(request, user):
	trigger=request.form['trigger_id']
	searchTerm=request.form["text"]
	processes=user.FilterProcess(searchTerm)
	filteredProcesses=[]
	if len(processes)<1:
		return 	"No processes found",200
	for x in processes:
		filteredProcesses.append({
			"text": {
				"type": "plain_text",
				"text": x["Id"],
				"emoji": true
			},
			"value": str(x["Key"])
		})
	currentDialog=processSelectionDialog
	currentDialog["blocks"][-1]["element"]["options"]=filteredProcesses
	response=requests.post('https://slack.com/api/views.open',data={
			"token" : slackToken,
			"trigger_id" : trigger,
			"view" : str(currentDialog)
			})
	return "",200

def FavoriteProcesses(request, user):
	trigger=request.form['trigger_id']
	envProcessObj=user.GetEnvProcesses()
	envProcesses=[]
	for x in envProcessObj:
		
		envProcesses.append({
			"text": {
				"type": "plain_text",
				"text": x["Name"],
				"emoji": true
			},
			"value": str(x["Id"])
		})
	print (str(len(envProcessObj)))
	if (len(envProcessObj)<1):
		envProcesses.append({
			"text": {
				"type": "plain_text",
				"text": "no processes found",
				"emoji": true
			},
			"value": ""
		})
	currentDialog=releaseSelectionDialog
	currentDialog["blocks"][-1]["element"]["options"]=envProcesses
	response=requests.post('https://slack.com/api/views.open',data={
			"token" : slackToken,
			"trigger_id" : trigger,
			"view" : str(currentDialog)
			})
	return "",200

@app.route("/auth", methods=["GET", "POST"])
def auth():
	trigger=request.form['trigger_id']
	user=request.form['user_id']
	domain=request.form['team_domain']
	channel=request.form['channel_id']
	response=requests.post('https://slack.com/api/views.open',data={
			"token" : slackToken,
			"trigger_id" : trigger,
			"view" : str(authDialog)
			})
	return "",200

	
@app.route("/thanks", methods=["GET", "POST"])
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
	app.run(debug=True)