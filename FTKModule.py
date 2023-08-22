#TXT Module for FTK Imager extractions v.01

import os
from datetime import date

ftkVersion = ""
examiner = ""
acqDate = ""
exType = ""
driveModel = ""
serialNumber = ""
driveCapacity = ""
hashMD5 = ""
hashSHA1 = "" 
hashverified = False

def ParseFTK(txtFile, savefName, caseNum, evNum):
    
    caseNumber = caseNum
    evNumber = evNum
    todayDate = date.today()   #Get todays date.
    
    with open(txtFile, 'r') as openUfd:   #Open TXT file from FTK Imager 
        lines = openUfd.readlines()
        for i, line in enumerate(lines):
            if 'Acquired' in line:
                ftkVersion = line.split(':')[1].strip()  #Select value after the equals sign               
            if 'Examiner' in line:
                examiner = line.split(':')[1].strip()              
            if 'Source' in line:
                exType = line.split(':')[1].strip()  
            if 'Drive Model' in line:
                driveModel = line.split(':')[1].strip()
            if 'Serial Number' in line:
                serialNumber = line.split(':')[1].strip()              
            if 'data size' in line:
                driveCapacity = line.split(':')[1].strip()  
            if 'MD5' in line:
                hashMD5 = line.split(':')[1].strip() 
            if 'SHA1' in line:
                hashSHA1 = line.split(':')[1].strip() 
            if 'Acquisition started' in line:
                acqDate = line.split(':', 1)[1].strip()    #Split only on first occurence of :  
            if 'MD5' in line:
                if 'verified' in line:
                    if not 'not' in line:
                        verified = True 
   
    def SaveFile(reportName):
                
        with open (reportName, "a") as f:
            f.write('Case Number: ' + caseNumber + '\n')
            f.write('Evidence Number: ' + evNumber + '\n')
            f.write('Date: ' + str(todayDate) + '\n')  
            if examiner:
                f.write('Examiner: ' + examiner + '\n')
            f.write('\n')
            if exType:
                f.write('Extraction Type: ' + exType + '\n')    
            if driveModel:
                f.write('Drive Model: ' + driveModel + '\n')
            if driveCapacity:
                f.write('Drive Capacity: ' + driveCapacity + '\n')    
            if acqDate:
                f.write('Acquisition Date: ' + str(acqDate) + '\n')  
            if hashMD5:
                f.write('MD5 Hash: ' + hashMD5 + '\n')    
            if hashSHA1:
                f.write('SHA1 Hash: ' + hashSHA1 + '\n')  
            f.write('Hash Verified: ' + str(verified) + '\n') 
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
            