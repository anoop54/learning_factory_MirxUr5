#Learning Factory 2018.
#Author: Simran Nijjar

import requests
import pprint

	#MiR Position Names:
		# KanBan_Pickup
		# Conveyor
		# ABB_YuMi
		# Packaging
		# Solenoid_Assembly

#Connect to MiR REST
host = '10.0.2.90'
port = '8080'
version = 'v1.0.0'

#Construct General URL
url = 'http://' + str(host) + ':' + str(port) + '/' + str(version) + '/'
#print(url)


def move_to_pos(destination):
	position = 0
	
	while (position == 0):
                #destination = input("Please enter the MiR's destination: ")

		if (destination == "KanBan_Pickup"):
			KanBan_Pickup = "e2f963bf-a14d-11e8-8fcf-f44d306b784b"
			move_mir_to_position(KanBan_Pickup)
			position = 1
			
		elif (destination == "Conveyor"):
			Conveyor = ""
			move_mir_to_position(Conveyor)
			position = 1
			
		elif (destination == "ABB_YuMi"):
			ABB_YuMi = ""
			move_mir_to_position(ABB_YuMi)
			position = 1
			
		elif (destination == "Packaging"):
			Packaging = ""
			move_mir_to_position(Packaging)
			position = 1
			
		elif (destination == "Solenoid_Assembly"):
			Solenoid_Assembly = ""
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
	print(battery_percentage)

	
#GET Register Values
def register_get(register):
	get_robot_status = requests.get(url + 'registers/' + str(register))
	status_json = get_robot_status.json()
	#pprint.pprint(status_json)

	register_value = status_json['value']
	print(register_value)
	
	return register_value
        
        
#GET Current State
def current_mode():
	get_robot_status = requests.get(url + 'status')
	status_json = get_robot_status.json()
	#pprint.pprint(status_json)
	
	state_result = status_json['state_text']
	print(state_result)

	
#POST Move MiR To Position
def move_mir_to_position(destination):		
	position_url = (url + 'mission_queue')
	move = "{\"taxi\": \"" + str(destination) + "\"}"
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}
	#print(destination)
	#print(move)
	#print(position_url)
	
	post = requests.request("POST", position_url, data=move, headers=header)
	continue_robot()
	
	
#POST Append Mission to Queue
def append_mission():
	mission_url = (url + 'mission_queue')
	mission = "{\"mission\": \"f2845ea0-a485-11e8-9ad7-f44d306b784b\"}"
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}
        #print(mission_url)
	#print(mission)
        
	post = requests.request("POST", mission_url, data=mission, headers=header)
	continue_robot()
	
	
#POST Continue MiR Operation
def continue_robot():
	continue_url = (url + 'state')
	state = "{\"state\": \"3\"}"
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}
	#print(continue_url)
	#print(state)
	
	put = requests.request("PUT", continue_url, data=state, headers=header)
	#return self._client.put(url), data=data, allow_insert=False)

	
#POST Pause the MiR
def pause_robot(self):
        pause_url = (url + 'state')
        state = "{\"state\": \"4\"}"
        header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}
	#print(pause_url)
	#print(state)

        put = requests.request("PUT", pause_url, data=state, headers=header)
	#return self._client.put(url), data=data, allow_insert=False)
        
	
def register_write(register,value):
	register_url = (url + 'registers/'+str(register))
	state = "{\"value\": " + str(value) + "}"
	header = {'accept': 'application/json', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.8', 'content-type': 'application/json'}
	print(register_url)
	print(state)
	
	put = requests.request("PUT", register_url, data=state, headers=header)
	#return self._client.put(url), data=data, allow_insert=False)
        
	
