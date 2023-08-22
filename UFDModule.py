#Cellebrite UFD Module

import os
from datetime import date

def ParseUFD(ufdFile, savefName, caseNum, evNum):
    
    caseNumber = caseNum
    evNumber = evNum
    todayDate = date.today()
    make = ""     
    model = "" 
    modelNumber = ""
    operatingSystem = ""
    imei = ""
    extractionDate = ""
    extractionType = ""
    ufedVersion = ""
    sha256 = ""     
    deviceType = ""
    exType = ""
    
    if 'ffs' in ufdFile.lower():
        exType = 'Full File System'
    
    with open(ufdFile, 'r') as openUfd:   #Open UFD file 
        lines = openUfd.readlines() 
        for i, line in enumerate(lines):
            line.replace(r'\n', '')    #Remove newline characters
            if 'Vendor' in line:
                make = line.split('=')[1].strip()  #Select value after the equals sign   
                continue
            if 'FullName' in line:
                model = line.split('=')[1].strip()   
                continue
            if 'DeviceModel' in line:
                modelNumber = line.split('=')[1].strip()
                continue
            if 'OS='in line:
                operatingSystem = line.split('=')[1].strip()   
                continue
            if 'IMEI' in line:
                imei = line.split('=')[1].strip()
                continue
            if 'Date' in line:
                extractionDate= line.split('=')[1].strip()
                continue
            if 'Version=' in line:
                ufedVersion = line.split('=')[1].strip()  
                continue
            if 'SHA256' in line:
                if i + 1 < len(lines):    #Select next line after SHA256 keyword located
                    sha256 = lines[i + 1].split('=')[1].strip()
    
    if 'SIM' in make:
        deviceType = "SIM Card"
        make = ""
        model = ""
        
    def SaveFile(reportName):

        with open (reportName, "a") as f:
            
            f.write('Case Number: ' + caseNumber + '\n')
            f.write('Evidence Number: ' + 'evNumber' +'\n') 
            f.write('Date: ' + str(todayDate) + '\n')
            if ufedVersion:   
                f.write('UFED Version: ' + ufedVersion + '\n')        
            f.write('\n')
            if deviceType:
                f.write('Device Type:  ' + deviceType + '\n')
            if make:
                f.write('Make: ' + make + '\n')
            if model:
                f.write('Model: ' + model + '\n') 
            if operatingSystem:
                f.write('Operating System: ' + operatingSystem + '\n')              
            if imei:   
                f.write('IMEI: ' + imei + '\n')  
            if extractionDate:    
                f.write("Extraction Date: " + extractionDate + '\n')  
            if exType:
                f.write('Extraction Type: ' + exType + '\n')
            if sha256:   
                f.write('SHA256 Hash:  ' + sha256 + '\n\n')                
          
      
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
      
