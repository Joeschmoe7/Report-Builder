#Module for DeviceInfo.txt files created by Cellebrite Premium.

import os
from datetime import date
        
def ParseTXT(txtFile, savefName, caseNum, evNum):
    
    caseNumber = caseNum
    evNumber = evNum
    todayDate = date.today()   #Get todays date.   
    acqDate = ""
    deviceType = ""
    deviceMake = ""
    deviceModel = ""
    opSys = ""   
    
    with open(txtFile, 'r') as openTXT:   #Open TXT file from Cellebrite Premium
        lines = openTXT.readlines()
        for line in lines:
            if 'Date and time' in line:
                acqDate = line.split(':')[1]            
            if 'Vendor' in line:
                deviceMake = line.split(':')[1].strip()              
            if 'Model' in line:
                deviceModel = line.split(':')[1].strip()  
            if 'OS Version' in line:
                if 'samsung' or 'motorola' or 'lg' in deviceMake.lower():
                    opSys = 'Android ' + line.split(':')[1].strip()
                if 'apple' in deviceMake.lower():
                    opSys = 'Apple ' + line.split(':')[1].strip()
                    
    def SaveFile(reportName):
            
        with open (reportName, "a") as f:
            
            f.write('Case Number: ' + caseNumber + '\n')
            f.write('Evidence Number: ' + evNumber + '\n')
            f.write('Date: ' + str(todayDate) + '\n')  
            f.write('\n')  
            if deviceType:
                f.write('Device Type' + deviceType + '\n')
            if deviceMake:
                f.write('Make: ' + deviceMake + '\n')
            if deviceModel:
                f.write('Model: ' + deviceModel + '\n') 
            if opSys:
                f.write('Operating System: ' + opSys + '\n')
            if acqDate:
                f.write('Acquisition Date: ' + str(acqDate) + '\n')    
            f.write('\n')
                
                
    if os.path.exists(savefName):                             #Test if there is already a report with the same name.
        appendFile = input('A report with this name already exists.  Would you like to append to that report? Y/N: ')
        if appendFile.lower() == 'y' or appendFile.lower() == 'yes':  
            try:
                SaveFile(savefName)
                print('Report successfully appended')
            except:
                print('There was a problem appending the report')
                            
        elif appendFile.lower() == 'n' or appendFile.lower() == 'no':
            newName = input('Enter a new report name: ')
            if not newName.endswith('.txt'):                  #Make sure the new name has the TXT extension.
                newName = newName + '.txt'  
            SaveFile(newName)
            
            if os.path.exists(newName):
                print('Success!')
            else:
                print('Error creating a new file')
        else:
            print('You chose... poorly.  The report file will be appended')
            try:
                SaveFile(savefName)
                print('Report successfully appended!')
            except:
                print('There was a problem appending the report')
                    
    else: 
        SaveFile(savefName)
        if os.path.exists(savefName):
            print('Success!')      