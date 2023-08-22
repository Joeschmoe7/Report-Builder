#Cellebrite UFDX module v.01

import xml.etree.ElementTree as ET
import os
from datetime import date


def ParseUFDX(ufdxFile, savefName, caseNum, evNum):
    
    caseNumber = caseNum
    evNumber = evNum
    examiner =  ""         #Declare blank variables so they are easier to skip if empty.
    deviceType = ""
    deviceMake = ""
    deviceModel = ""
    deviceGuid = ""
    exType = ""
    
    todayDate = date.today()   #Get todays date. 

    tree = ET.parse(ufdxFile)  #Open XML file
    root = tree.getroot()      #Get root element of XML
    
    valuesList = {}
    
    for values in root.findall(".//DeviceInfo"):
        valuesList = values.attrib
        
    if 'Apple' in valuesList['Vendor']:    #If extraction is an iPhone
        deviceMake = 'Apple'
        deviceModel = valuesList['Model']
        deviceType = 'Cell Phone'
        deviceGuid = valuesList['Guid']
        for newValues in root.findall(".//Extraction"):
            extractList = newValues.attrib     
            if 'FFS' in extractList['Path']:
                exType = 'Full File System'
            elif 'Password' in extractList['Path']:
                exType = 'Password'

    elif 'SIM' in valuesList['Vendor']:    #If extraction is a SIM card
        
        deviceModel = valuesList['Model']
        deviceType = 'SIM Card'
        deviceGuid = valuesList['Guid']   
        exType = "Logical"
    
    elif 'Memory' in valuesList['Model']:  #If extraction is a micro-SD card
 
        deviceType = 'Memory Card'
        deviceGuid = valuesList['Guid']
        for memValues in root.findall(".//Extraction"):
            memList = memValues.attrib     
            exType = memList['TransferType']
        
    else:
        print('Uh oh... Device type not recognized')
        
        
    def SaveFile(reportName):                           #function to save report
        
        with open (reportName, "a") as f:
                
            f.write('Case Number: ' + caseNumber + '\n')
            f.write('Evidence Number: ' + evNumber + '\n')
            f.write('Date: ' + str(todayDate) + '\n')
            f.write('\n')
            
            if deviceType:
                f.write('Device Type: ' + str(deviceType) + '\n')          
            if deviceMake:
                f.write('Make: ' + deviceMake + '\n')    
            if deviceModel:
                f.write('Model: ' + deviceModel + '\n') 
            if exType:
                f.write('Extraction Type: ' + exType + '\n')  
            if deviceGuid:
                f.write('GUID: ' + deviceGuid + '\n')      
            f.write('\n\n')
            
    if os.path.exists(savefName):                             #Test if there is already a report with the same name.
        appendFile = input('A report with this name already exists.  Would you like to append to that report? Y/N: ')
        if appendFile.lower() == 'y' or appendFile.lower() == 'yes':  
            try:
                SaveFile(savefName)           #Append report file if that filename is already used.
                print('Report successfully appended')
            except:
                print('There was a problem appending the report')
                                    
        elif appendFile.lower() == 'n' or appendFile.lower() == 'no':    #Choose a different name if already exists.
            newName = input('Enter a new report name: ')
            if not newName.endswith('.txt'):                  #Make sure the new name has the TXT extension.
                newName = newName + '.txt'  
            SaveFile(newName)
                    
            if os.path.exists(newName):         #Test is report was created with new file name.
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
    