import openpyxl
from pathlib import Path

# new dictionary that has headers as keys and the column they output
# to in the output file as their values
fileAndSheetDict = {}
headerDict = {}

# Global variables that keep track of the write pointer in the output sheet
nextWriteRow = 3
nextWriteColumn = 1

def correctExtenstion(someString):
    if (len(someString.split('.')) != 2 or someString.split[1] != 'xlsx'):
        return someString.split('.')[0] + '.xlsx'
    else:
        return someString

def acceptInputAndFormFileDict():
    global fileAndSheetDict

    numberOfFilesToMerge = input(
        'Enter the number of excel files you need to merge: ')

    for i in range(0, int(numberOfFilesToMerge)):
        fileNumber = str(i + 1)
        fileName = input(
            'Enter the name of file {0} :'.format(fileNumber))
        inputSheets = input(
            'Enter the names of the sheets in file {0}'.format(fileNumber)
            + 'to be merged (multiple files can be separated by commas): ')

        # removing whitespace
        inputSheets = inputSheets.replace(', ', ',')

        # correcting the input Name
        fileName = correctExtenstion(fileName)
        fileAndSheetDict[fileName] = inputSheets

# Writes all the contents of a column into the output Sheet
def readAndOutputColumn(inputColumn, inputSheet, outputSheet, maxRow):
    global headerDict
    global nextWriteColumn
    global nextWriteRow

    # assuming that headers are in the first row of the input sheet
    columnHeader = inputSheet.cell(row=1, column=inputColumn).value

    # add a new header to the dictionary
    if not(columnHeader in headerDict):
        headerDict[columnHeader] = nextWriteColumn
        outputSheet.cell(row=1, column=nextWriteColumn, value=columnHeader)
        nextWriteColumn += 1

    outputColumn = headerDict[columnHeader]

    # write all the contents of that column in the corresponding output sheet
    isRowEmpty = True
    for currentRow in range(2, maxRow + 1):
        content = inputSheet.cell(row=currentRow, column=inputColumn).value
        
        # Don't print None in the output sheet, but leave things blank
        if (content == 'None'): content = ''
        elif (isRowEmpty == True): isEmpty = False
       
        outputSheet.cell(row=nextWriteRow, column=outputColumn, value=str(content))
        
        # if the Row is empty, you can overwrite it next time
        if (isEmpty == False): nextWriteRow += 1


def mergeSheet(inputSheet, outputSheet):
    global nextWriteColumn
    global nextWriteRow

    # for every column in the current sheet
    for currentColumn in range(1, inputSheet.max_column + 1):
        readAndOutputColumn(currentColumn, inputSheet, outputSheet, inputSheet.max_row)

    # the next sheet needs to print content below the current sheet
    nextWriteRow += inputSheet.max_row + 1

def main():

    currentDir = Path('./..')

    # accept the Input Files and Sheets
    acceptInputAndFormFileDict()

    outputFile = input('Enter the name of the output file to be generated: ')
    outputSheet = input('Enter the name of the output sheet to be generated: ')

    # auto-correcting the output extension and resolving the Path
    outputFile = currentDir / 'Generated' / correctExtenstion(outputFile)


    outputWorkbook = openpyxl.Workbook()
    writeSheet = outputWorkbook.create_sheet(title=outputSheet)

    # For every file, run through their sheets
    for inputFile, inputSheets in fileAndSheetDict:
        
        fileDir = currentDir / 'Spreadsheets' / inputFile
        sourceWorkbook = openpyxl.load_workbook(fileDir, data_only=True)

        # For every sheet to merge
        for sheet in inputSheets.split(','):
            # TODO: There has to be a better way to do this
            # Putting the contents of the current sheet into the output sheet
            inputSheet = sourceWorkbook[sheet]
            mergeSheet(inputSheet, writeSheet)

    outputWorkbook.save(outputFile)
    print('Sheets have been merged and output file has been generated!')

if __name__ == "__main__":
    main()
