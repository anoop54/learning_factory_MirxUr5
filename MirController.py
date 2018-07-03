# Author: Simran Nijjar
# Learning Factory 2018
import requests
import pprint

	# MiR Position Names:
		# KanBan_Pickup
		# Conveyor
		# ABB_YuMi
		# Packaging
		# Solenoid_Assembly
	
#Connect to MiR REST
host = '172.16.1.168'
port = '8080'
version = 'v1.0.0'
	
#Construct General URL
url = 'http://' + str(host) + ':' + str(port) + '/' + str(version) + '/'
#print(url)
	
	
#Main Function
def move_to_pos(destination):
	position = 0
	
	while (position == 0):
 
		if (destination == "KanBan_Pickup"):
			KanBan_Pickup = "5d41e9a6-6f3e-11e8-8d30-f44d306b784b"
			move_mir_to_position(KanBan_Pickup)
			position = 1
			
		elif (destination == "Conveyor"):
			Conveyor = "816abffe-6b65-11e8-9e1a-f44d306b784b"#####
			move_mir_to_position(Conveyor)
			position = 1
			
		elif (destination == "ABB_YuMi"):
			ABB_YuMi = "816abffe-6b65-11e8-9e1a-f44d306b784b"#####
			move_mir_to_position(ABB_YuMi)
			position = 1
			
		elif (destination == "Packaging"):
			Packaging = "816abffe-6b65-11e8-9e1a-f44d306b784b"#####
			move_mir_to_position(Packaging)
			position = 1
			
		elif (destination == "Solenoid_Assembly"):
			Solenoid_Assembly = "816abffe-6b65-11e8-9e1a-f44d306b784b"#####
			move_mir_to_position(Solenoid_Assembly)
			position = 1
			
		else:
			print("Invalid Entry")
			question = input("Do you wish to try again? (y/n): ")
			if question == "y":
				position = 0
			else:
				position = 1


				
#GET Battery Percentage
def battery_percentage():
	get_robot_status = requests.get(url + 'status')
	status_json = get_robot_status.json()
	
	#pprint.pprint(status_json)

	battery_percentage = status_json['battery_percentage']
	print (battery_percentage)

def register_get(register):
	get_robot_status = requests.get(url + 'registers/'+str(register))
	status_json = get_robot_status.json()
	
	#pprint.pprint(status_json)

	register_value = status_json['value']
	
	print (register_value)
	
	return register_value


def current_mode():
	get_robot_status = requests.get(url + 'status')
	status_json = get_robot_status.json()
	
	#pprint.pprint(status_json)

	battery_percentage = status_json['state_text']
	print (battery_percentage)




#POST Move MiR To Position
def move_mir_to_position(destination):
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}		
	position_url = (url + 'mission_queue')
	move = "{\"taxi\": \"" + str(destination) + "\"}"
	#print(destination)
	#print(move)
	#print(position_url)
	#print(header)
	
	post = requests.request("POST", position_url, data=move, headers=header)
	continue_robot()
	
	
	
	
#POST Append Mission to Queue
def append_mission():
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}		
	mission_url = (url + 'mission_queue')
	mission = "{\"mission\": \"ce2b422d-7880-11e8-94bd-f44d306b784b\"}"

	post = requests.request("POST", mission_url, data=mission, headers=header)
	continue_robot()
	



# Continue MiR operation
def continue_robot():
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}		
	continue_url = (url + 'state')
	state = "{\"state\": \"3\"}"
	
	put = requests.request("PUT", continue_url, data=state, headers=header)
	#return self._client.put(url), data=data, allow_insert=False)

def register_write(register,value):
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}		
	continue_url = (url + 'registers/'+str(register))
	print(continue_url)
	state = "{\"value\": "+str(value)+"}"
	print(state)
	put = requests.request("PUT", continue_url, data=state, headers=header)
	#return self._client.put(url), data=data, allow_insert=False)




#http://172.16.1.168:8080/v1.0.0/registers/	
# # Pause the MiR
# def pause_robot(self):
	# data = ('state': 4)
	# url = 'state'
	# return self._client.put(url), data=data, allow_insert=False)
	
		
		
		
		
		
