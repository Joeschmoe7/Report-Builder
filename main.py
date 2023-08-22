# Forensic Report Builder v.05

# The purpose of this script is to pull information from report files created by forensic tools,
# format that information and save the results to a text file. This script was created to save
# time for investigators who have to complete written reports in addition to the tool created
# reports.  I write several forensic reports a day and this will save time and prevent some 
# typing mistakes.  Individual modules were created for each type of tool report to make
# future updates easier.

# To from the main.py script, input the file to parse using the -f argument, and select the
# type of tool report, --cellbrite, --graykey or --ftk.

# The script will request the case number and evidence name and use those as the report name.


import UFDModule
import PDFModule
import UFDXModule
import FTKModule
import TXTModule
import os
import argparse

class ProcessFiles:
    
    def __init__(self):
        
        args = self.ParseCommandLine()        
        self.toolReport = args.f       
        self.gkExtraction = False
        self.cbExtraction = False
        self.ftkExtraction = False
               
        if args.graykey:
            self.gkExtraction = True
        elif args.cellebrite:
            self.cbExtraction = True     
        elif args.ftk:
            self.ftkExtraction = True                       
                
        self.caseNumber = input('Enter the case number: ')
        self.evNumber = input('Enter the evidence number: ')
        self.reportName = self.caseNumber + '_' + self.evNumber + '.txt'
              
    def ValidateFilePath(self,theFile):

        if not os.path.exists(theFile):
            raise argparse.ArgumentTypeError('File does not exist')
    
        if os.access(theFile, os.R_OK):
            return theFile
        else:
            raise argparse.ArgumentTypeError('File is not readable')
    
    
    def ParseCommandLine(self):
    
        parser = argparse.ArgumentParser('Report Builder v.01')
    
        parser.add_argument('-f', type= self.ValidateFilePath,required=True, help="Specify the file path of the tool report.")
    
        group = parser.add_mutually_exclusive_group(required=True)
        
        group.add_argument('--graykey',      help = 'specifies a GrayKey extraction',   action='store_true')
        group.add_argument('--cellebrite',     help = 'specifies a Cellebrite extraction',   action='store_true')
        group.add_argument('--ftk',   help = 'specifies an FTK Imager image',   action='store_true')   
    
        parsedArguments = parser.parse_args()   
        
        return parsedArguments
  
    def ProcessPDF(self):
        
        if self.gkExtraction:
            if '.pdf' in self.toolReport:
                PDFModule.ParsePDF(self.toolReport, self.reportName, self.caseNumber, self.evNumber)
            else:
                print('GrayKey reports should be PDF files')
                
 
    def ProcessCB(self):       
        
        if self.cbExtraction:
            
            if '.ufdx' in self.toolReport:
                UFDXModule.ParseUFDX(self.toolReport, self.reportName, self.caseNumber, self.evNumber)
            elif '.ufd' in self.toolReport:
                UFDModule.ParseUFD(self.toolReport, self.reportName, self.caseNumber, self.evNumber) 
            elif '.txt' in self.toolReport:
                TXTModule.ParseTXT(self.toolReport, self.reportName, self.caseNumber, self.evNumber) 
            else:
                print('Pick a UFD, UFDX or TXT from a Cellebrite extraction.')
                
    def ProcessFTK(self):
        if self.ftkExtraction:
            if '.txt' in self.toolReport:
                FTKModule.ParseFTK(self.toolReport, self.reportName, self.caseNumber, self.evNumber)
            else:
                print('FTK Imager reports should be TXT files')        

if __name__ ==  '__main__':
    
    reportObj = ProcessFiles()
    if reportObj.gkExtraction == True:
        reportObj.ProcessPDF()
        
    if reportObj.cbExtraction == True:
        reportObj.ProcessCB()
    
    if reportObj.ftkExtraction == True:
        reportObj.ProcessFTK()
