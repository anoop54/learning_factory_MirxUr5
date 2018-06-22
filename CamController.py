import numpy as np
import cv2
import cv2.aruco as aruco
import glob
from ftplib import FTP
from PIL import Image
import io
import socket
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time

class cam:

    mainimage= b''

    def callback(self, data):
        self.mainimage = self.mainimage + data

    def savImage(self, mainimage):
        image = Image.open(io.BytesIO(mainimage))
        return image
        
    def cv2Conversion(self, image):
        image = image.convert('RGB')
        opencvImage = np.array(image)    
        opencvImage = opencvImage[:, :, ::-1].copy() 
        return opencvImage

    def rotateImage(self,image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    def GetImage(self):
        ftp = FTP('172.16.0.13')
        ftp.login('FTP','Factory1')
        ftp.cwd('MirBasket')
        
        ftp.retrbinary('RETR image.bmp', self.callback)
        image = self.savImage(self.mainimage)
        ftp.quit()

        cvImage = self.cv2Conversion(image)
        
        return cvImage
    
    def doOperation(self):
        self.mainimage= b''

        
        try:
            cv_file = cv2.FileStorage("test.yaml", cv2.FILE_STORAGE_READ)
            mtx = cv_file.getNode("camera_matrix").mat()
            dist = cv_file.getNode("dist_coeff").mat()
            cv_file.release()


            image = self.GetImage()    


            image = cv2.resize(image,(640,480))
  #          cv2.imshow('frame',image)
            frame = self.rotateImage(image,-90)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

            font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

            if np.all(ids != None):
                rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners[0], 37.0 , mtx, dist) #Estimate pose of each marker and return the values rvet and tvec---different from camera coefficients
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
                aruco.drawAxis(frame, mtx, dist, rvec[0], tvec[0], 0.1) #Draw Axis
                aruco.drawDetectedMarkers(frame, corners) #Draw A square around the markers
                ###### DRAW ID #####
                cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
                # Display the resulting frame
            cv2.imshow('frame',frame)
            name= 'trials/'+ str(corners[0][0][0])+'.bmp'
            status = cv2.imwrite(name,frame)
            return ids,corners,rvec,tvec
        except:
            print("Marker not found")
            return 0 
