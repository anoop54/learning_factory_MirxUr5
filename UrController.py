import socket
import time
import struct


class MyUr:
    HOST = "172.16.1.141" # The remote host
    PORT = 30003
    
    Ur_Home =     ("movej([-3.1258847, -1.5767304, 1.5449655, 1.58825, 1.57 , 0.04468043], a=1.0, v=1)" + "\n")
    Ur_TakePic =  ("movej([-0.6937, -2.04, 1.753, 0.06, 2.51, -0.178], a=1.0, v=1)" + "\n")
    
    Ur_DropOff =  ("movej([-2.295108, -1.158375, 1.81409522, -0.6578146, 0.84735735, 0.03752458], a=1.0, v=0.1)" + "\n")


    Picturetrig = "set_digital_out(0,True)"+"\n"
    Picturetrig1 = "set_digital_out(0,False)"+"\n"

    count = 0
    home_status = 0
    program_run = 0


    def getCurrentPos(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((self.HOST, self.PORT))
            time.sleep(1.00)
            print("")
            packet_1 = s.recv(4)
            packet_2 = s.recv(8)
            packet_3 = s.recv(48)
            packet_4 = s.recv(48)
            packet_5 = s.recv(48)
            packet_6 = s.recv(48)
            packet_7 = s.recv(48) 
            packet_8 = s.recv(48)
            packet_9 = s.recv(48)
            packet_10 = s.recv(48)
            packet_11 = s.recv(48)

            packet_12 = s.recv(8)
            x = struct.unpack('!d', packet_12)[0]
            print ("X = ", x * 1000)

            packet_13 = s.recv(8)
            y = struct.unpack('!d', packet_13)[0]
            print ("Y = ", y * 1000)

            packet_14 = s.recv(8)
            z = struct.unpack('!d', packet_14)[0]
            print ("Z = ", z * 1000)

            packet_15 = s.recv(8)
            Rx = struct.unpack('!d', packet_15)[0]
            print ("Rx = ", Rx)

            packet_16 = s.recv(8)
            Ry = struct.unpack('!d', packet_16)[0]
            print ("Ry = ", Ry)

            packet_17 = s.recv(8)
            Rz = struct.unpack('!d', packet_17)[0]
            print ("Rz = ", Rz)

            home_status = 1
            program_run = 0
            s.close()
            return(x,y,z,Rx,Ry,Rz)
        
        except socket.error as socketerror:
            print("Error: ", socketerror)
            print("Unable to connect to Ur")
        
    #s = speed
    def MoveDelta(self,x,y,z,s=1,rx=0,ry=0,rz=0):
        
        xo,yo,zo,rxo,ryo,rzo = self.getCurrentPos()
        x = xo*1000+x
        y = yo*1000+y
        z = zo*1000+z
        rx = rxo+rx
        ry = ryo+ry
        rz = rzo+rz    
        Ur_Move = "movel(p["+str(x/1000.0)+ ", "+ str(y/1000.0) + ", "+ str(z/1000) + ", "+ str(rx)+", "+str(ry)+", "+str(rz)+"], a="+str(s)+", v=1)" + "\n"
        print(Ur_Move)
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST,self.PORT))
            s.send(Ur_Move.encode())
            data= s.recv(1024)
            s.close()
            
        except socket.error as socketerror:
            print("Error: ", socketerror)
            print("Unable to connect to Ur")
        print("UrAction: Move Complete")
        
    def MoveAbs(self,x,y,z,rx=0,ry=0,rz=0):
   
        Ur_Move = "movej(p["+str(x/1000.0)+ ", "+ str(y/1000.0) + ", "+ str(z/1000) + ", "+ str(rx)+", "+str(ry)+", "+str(rz)+"], a=1.0, v=1)" + "\n"
        print(Ur_Move)
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST,self.PORT))
            s.send(Ur_Move.encode())
            data= s.recv(1024)
            s.close()
            
        except socket.error as socketerror:
            print("Error: ", socketerror)
            print("Unable to connect to Ur")
        print("UrAction: Move Complete")

        
    def MoveCommand(self, command):
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST,self.PORT))
            s.send(command.encode())
            data= s.recv(1024)
            s.close()
            
        except socket.error as socketerror:
            print("Error: ", socketerror)
            print("Unable to connect to Ur")            
        print("UrAction: Move Complete")

    def TakePic(self):
        self.MoveCommand(self.Ur_TakePic)

    def Home(self):
        self.MoveCommand(self.Ur_Home)

    def dropOff(self):
        self.MoveCommand(self.Ur_DropOff)

    def basket_down(self):
        self.MoveCommand(("movej([-0.6937, -2.04, 1.753, 0.06, 2.51, -0.178], a=1.0, v=1)" + "\n"))
        



        
    def PicTrigger(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST,self.PORT))
        s.send(self.Picturetrig.encode())
        time.sleep(1)
        s.send(self.Picturetrig1.encode())
        data= s.recv(1024)
        s.close()
        print("UrAction: Picture triggered")
