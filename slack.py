from blocks import Block
import requests
import json

class Slack:
	def __init__(self):
		with open("key.txt","r") as file:
			self.token=file.read().strip()

	def SendProcessSelection(self, processes, trigger):
		filteredProcesses=[]
		for x in processes:
			filteredProcesses.append({
			"text": {
				"type": "plain_text",
				"text": x["Id"],
				"emoji": True
			},
			"value": str(x["Key"])
			})
		currentDialog=Block.processSelectionDialog
		currentDialog["blocks"][-1]["element"]["options"]=filteredProcesses
		response=requests.post('https://slack.com/api/views.open',data={
			"token" : self.token,
			"trigger_id" : trigger,
			"view" : str(currentDialog)
			})

	def SendEnvProcesses(self, envProcessObj, trigger):
		envProcesses=[]
		for x in envProcessObj:
			envProcesses.append({
				"text": {
					"type": "plain_text",
					"text": x["Name"],
					"emoji": True
				},
				"value": str(x["Id"])
			})
		if (len(envProcessObj)<1):
			envProcesses.append({
				"text": {
					"type": "plain_text",
					"text": "no processes found",
					"emoji": True
				},
				"value": ""
			})
		currentDialog=Block.releaseSelectionDialog
		currentDialog["blocks"][-1]["element"]["options"]=envProcesses
		response=requests.post('https://slack.com/api/views.open',data={
				"token" : self.token,
				"trigger_id" : trigger,
				"view" : str(currentDialog)
				})
	
	def OpenAuthDialog(self, data):
		trigger=data['trigger_id']
		user=data['user_id']
		domain=data['team_domain']
		channel=data['channel_id']
		response=requests.post('https://slack.com/api/views.open',data={
				"token" : self.token,
				"trigger_id" : trigger,
				"view" : str(Block.authDialog)
				})
	
	def AddRobot(self, requestObj):
		print(json.dumps(requestObj))
		trigger=requestObj['trigger_id']
		response=requests.post('https://slack.com/api/views.open',data={
				"token" : self.token,
				"trigger_id" : trigger,
				"view" : str(Block.RobotDialog)
				})