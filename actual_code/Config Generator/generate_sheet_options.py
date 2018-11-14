import toml
import openpyxl

def writeSheetOptions(
  fileObject, name, rows, cols, headerRow, dataStartRow, dataEndRow, skipRows):

    commentString = "\n# Details of the source sheet. Edit in case info is wrong \n\n"
    name = "sheet.name = \"{0}\"\n".format(name)
    rows = "sheet.rows = +{0}\n".format(str(rows))

    # NEW THINGS - NOT IMPLEMENTED ON PARSER
    headerRow = "sheet.headerrow = +{0}\n".format(str(headerRow))
    dataStartRow = "sheet.datastartrow = +{0}\n".format(str(dataStartRow))
    dataEndRow = "sheet.datastartrow = +{0}\n".format(str(dataEndRow))
    skipRows = "sheet.skiprows = +{0}\n".format(str(skipRows))
    # END OF NEW THINGS

    cols = "sheet.cols = \"{0}\"\n".format(
        openpyxl.utils.get_column_letter(cols))

    fileObject.write("{0}{1}{2}{3}".format(commentString, name, rows, cols))
