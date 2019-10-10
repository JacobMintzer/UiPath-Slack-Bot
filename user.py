import requests
import json

class User:
	def __init__(self, userID):
		self.isComplete=False
		with open("userLib.json",'r') as userLib:
			userData=json.load(userLib)
		if (userID not in userData.keys()):
			print ("none")
			self=None
			return None
		self.UserID=userID
		self.Email=userData[userID]["email"]
		self.Password=userData[userID]["password"]
		self.Tenant=userData[userID]["tenant"]
		self.Environment=userData[userID]["environment"]
		self.Robot=userData[userID]["robot"]
		self.token=self.GetToken()
		if self.token is "":
			return
		self.isComplete=True

	def GetToken(self):
		authResponse=requests.post("https://platform.uipath.com/api/account/authenticate",headers={"Accept":"application/json"},data={"tenancyName":self.Tenant,"usernameOrEmailAddress":self.Email,"password":self.Password})
		if "result" in authResponse.json().keys():
			token=authResponse.json()["result"]
			return token
		else:
			return ""

	def GetRobot(self):
		robotResponse=requests.get("https://platform.uipath.com/odata/Robots?$filter=Name eq '{0}'".format(self.Robot),headers={"Authorization":"Bearer "+self.token})
		return robotResponse.json()["value"][0]["Id"]

	def GetEnvironment(self):
		robotResponse=requests.get("https://platform.uipath.com/odata/Environments?$filter=Name eq '{0}'".format(self.Environment),headers={"Authorization":"Bearer "+self.GetToken()})
		print(json.dumps(robotResponse.json()))
		return robotResponse.json()["value"][0]["Id"]
	
	def FilterProcess(self, searchTerm):
		processResponse=requests.get("https://platform.uipath.com/odata/Processes?$filter=contains(tolower(Id)%20%2C%20tolower('{0}'))&$top=100".format(searchTerm),
			headers={"Authorization":"Bearer "+self.token})
		return processResponse.json()["value"]
		
	def CreateRelease(self,process,environment):
		body={
			"ProcessKey": process.split(':')[0],
			"EnvironmentId": environment,
			"ProcessVersion": process.split(':')[-1],
			"Name" : process
		}
		releaseResponse=requests.post("https://platform.uipath.com/odata/Releases", headers={"Authorization":"Bearer "+self.token},data=body)
		return releaseResponse.json()["Key"]

	def StartJob(self,releaseKey):
		token=self.GetToken()
		robot=self.GetRobot()
		jobParams={}
		jobParams['startInfo']={}
		jobParams['startInfo']['Strategy']='Specific'
		jobParams['startInfo']['ReleaseKey']=releaseKey
		jobParams['startInfo']['RobotIds']=[]
		jobParams['startInfo']['RobotIds'].append(int(robot))
		jobParams['startInfo']['NoOfRobots']=0
		jobResponse=requests.post("https://platform.uipath.com/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",
			headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},json=jobParams)
		print ("starting job\n")

	def CreateJob(self, process):
		if type(process) is int:
			resp=requests.post("http://platform.uipath.com/odata/Releases?$filter=Id eq {0}".format(process),headers={"Authorization":"Bearer "+self.token})
		else:
			resp=requests.get("http://platform.uipath.com/odata/Releases?$select=Key&$filter=(Name eq '{0}')".format(process),headers={"Authorization":"Bearer "+self.token}) 
		#i cahnged this from post so if it breaks thats it
		key=resp.json()["value"][0]["Key"]
		return key

	def GetEnvProcesses(self):
		return requests.get("https://platform.uipath.com/odata/Releases?$filter=EnvironmentName%20eq%20'{0}'".format(self.Environment),headers={"Authorization":"Bearer "+self.token}).json()["value"]
	
	