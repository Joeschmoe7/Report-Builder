#PDF Module for Graykey reports

import PyPDF2
import os
from datetime import date

def ParsePDF(pdfFile, savefName, caseNum, evNum):
    
    caseNumber = caseNum
    evNumber = evNum
    examiner =  ""         #Declare blank variables so they are easier to skip if empty.
    gkSoftware = ""
    extractionDate = ""
    deviceType = ""
    deviceMake = ""
    deviceModel = ""
    serialNumber = ""
    opSys = ""
    imei = ""
    imei2 = ""
    passcode = ""
    msisdn = ""
    udid = ""
    deviceOwner = ""
    accounts = ""
    exType = ""
    exHash = ""
    keychainHash = ""    
    ffsHash = ""
    afuHash = ""
    bfuHash = ""
    keystoreHash = ""
    keychainHash = ""
    
    todayDate = date.today()   #Get todays date.

    pdfFileObj = open(pdfFile, 'rb')     #Open PDF file
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    count = len(pdfReader.pages)   #Count the number of pages in PDF
    text = ""
    
    for i in range(count):   #Loop through all of the pages and add the content to the text variable
        pageObj = pdfReader.pages[i]
        text += pageObj.extract_text()
    pdfFileObj.close()
    
    pdfList = text.split('\n')  #Add each line of text to a list.
    
    for i, line in enumerate(pdfList):     #iterate through list, numbering each line
        
        if 'Examiner Name' in line:
            examiner = line.split(':')[1].strip()

        if 'GrayKey Software' in line:
            gkSoftware = line.split(':', 1)[1].strip()
            
        if 'Report generation' in line:
            extractionDate = line.split(':',1)[1].strip()   #Split the line by only the second colon
            
        if 'Model' in line:
            deviceModel = line.split('Model')[1]
            if 'iphone' in deviceModel.lower():
                deviceMake = "Apple"
            elif 'galaxy' in deviceModel.lower():
                deviceMake = 'Samsung'
            
        if 'Software Version' in line:
            opSys = line.split()[2].strip()
            
        if 'Serial Number' in line:
            serialNumber = line.split()[2].strip()
            
        if 'IMEI ' in line:
            imei = line.split()[1].strip()
            
        if 'IMEI(2)' in line:
            imei2 = line.split()[1].strip()
    
        if 'Phone Number' in line:
            msisdn = line.split()[1].strip()
            
        if 'UDID' in line:
            udid = line.split()[4].strip()
            
        if 'mechanism' in line:
            passcode = line.split()[4].strip()
            
        if 'Owner' in line:
            deviceOwner = line.split('Name')[1].strip()

        if 'Accounts' in line:
            accounts = line.split()[1].strip()
            
        if 'Full Filesystem' in line:        #Get the SHA256 hash value two lines after the heading Full File System
            if 'SHA256' in pdfList[i + 2]:
                ffsHash = pdfList[i + 2].split()[1]  
            
        if 'Instant AFU' in line:
            if 'SHA256' in pdfList[i + 2]:
                afuHash = pdfList[i + 2].split()[1] 
                
        if 'BFU' in line:
            if 'SHA256' in pdfList[i + 2]:
                bfuHash = pdfList[i + 2].split()[1]  
                
        if 'Android Keystore' in line:        
            if 'SHA256' in pdfList[i + 1]:
                keystoreHash = pdfList[i + 1].split()[1]  
                
        if 'Keychain' in line:
            if 'SHA256' in pdfList[i + 1]:
                keychainHash = pdfList[i + 1].split()[1]          
            
    def SaveFile(reportName):                    #function to create the report.
        
        with open (reportName, "a") as f:                 
            
            f.write('Case Number: ' + caseNumber + '\n')
            f.write('Evidence Number: ' + evNumber + '\n')
            f.write('Date: ' + str(todayDate) + '\n')
            
            if gkSoftware:                       #skip fields that are empty
                f.write('GrayKey Software: ' + str(gkSoftware) + '\n')
            f.write('\n')
            if deviceType:
                f.write('Device Type: ' + deviceType + '\n')
            if deviceMake:
                f.write('Device Make: ' + deviceMake + '\n')
            if deviceModel: 
                f.write('Device Model: ' + deviceModel + '\n')
            if opSys:
                f.write('Operating System: ' + opSys + '\n')
            if serialNumber:
                f.write('Serial Number: ' + serialNumber + '\n')
            if imei:
                f.write('IMEI: ' + imei + '\n')
            if imei2:
                f.write('IMEI2: ' + imei2 + '\n')        
            if udid:
                f.write('UDID: ' + udid + '\n')
            if passcode:
                f.write('Passcode: ' + passcode + '\n')
            if extractionDate:
                f.write('Extraction Date/Time: ' + extractionDate + '\n')
            if deviceOwner:
                f.write('Device Owner: ' + deviceOwner + '\n')
            if accounts:
                f.write('User Accounts: ' + accounts + '\n')
            f.write('\nHash Values\n\n')
            if ffsHash:
                f.write('Full Filesystem SHA256 Hash: ' + ffsHash + '\n')
            if afuHash:
                f.write('AFU SHA256 Hash: ' + afuHash + '\n')
            if bfuHash:
                f.write('BFU SHA256 Hash: ' + bfuHash + '\n')
            if keystoreHash:
                f.write('Android Keystore SHA256 Hash: ' + keystoreHash + '\n')
            if keychainHash:
                f.write('IOS Keychain SHA256 Hash: ' + keychainHash + '\n')
            f.write('\n\n')        
        
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
    
    
    
