#! /usr/bin/python
# -*- coding: UTF-8 -*-

# name : abosloh
# Email : abosloh.654@gmail.com
# homepage : https://github.com/abosloh

import sys,string , os.path , re
from PyQt4 import QtGui, QtCore
import urllib2
import xml.etree.ElementTree as ET


class FindTextAtURL():
    
    FileXML = "FindTextAtURL.xml" # path file xml
    
    def __init__(self):
        
        
        
        app = QtGui.QApplication(sys.argv)
        
        app.setLayoutDirection(QtCore.Qt.RightToLeft)
        
        #########################
        # open file xml for history regex
        
        if os.path.isfile(self.FileXML) == False:
            print "there is no file at : " , self.FileXML
            return None
        
        self.treeXML = ET.parse(self.FileXML)
        self.rootXML = self.treeXML.getroot()
         
        
        #########################
        # create window
        self.win = QtGui.QWidget()
        self.win.resize(400,500)
        self.win.setWindowTitle(u"البحث داخل الروابط")
        
        #########################
        # create GridLayout
        Grid = QtGui.QGridLayout()
        self.win.setLayout(Grid)
        
        #########################
        # Label textURL (the links to search within)
        label_textURL = QtGui.QLabel(u"الروابط المراد البحث ضمنها (افصل بينها بسطر جديد ) : ")
        Grid.addWidget(label_textURL)
        #text (set of links like "http://www.goog.com\nhttp://www.goog.com" )
        self.textURL = QtGui.QTextEdit()
        self.textURL.setFont(QtGui.QFont('ubuntu mono', 11))
        Grid.addWidget(self.textURL)
        
        #########################
        # label command Regex
        label_regex = QtGui.QLabel( (u"النص المراد البحث عنه بترميز (Regex) :") )
        Grid.addWidget(label_regex)
        #########################
        # Hbox Regex1
        hbox_regex1 = QtGui.QHBoxLayout()
        Grid.addLayout(hbox_regex1 , 3 , 0)
        # Hbox Regex2
        hbox_regex2 = QtGui.QHBoxLayout()
        Grid.addLayout(hbox_regex2 , 4 , 0)
        
        # combobox the history
        self.history = QtGui.QComboBox()
        hbox_regex1.addWidget(self.history)
        
        self.history_list = QtCore.QStringList()
        
        self.history_list.append(u"الذاكرة")
        # read from XML file and add itme in history list
        for child in self.rootXML.findall("regex"):
            self.history_list.append(QtCore.QString(child.text))
        
        self.history.addItems(self.history_list)
        
        self.history.connect(self.history , QtCore.SIGNAL("activated(QString)") , self.activatedHistory)
        
        # button remove history
        button_remove_history = QtGui.QPushButton((u"حذف"))
        button_remove_history.setToolTip(QtCore.QString((u"حذف الذاكرة")))
        button_remove_history.connect(button_remove_history, QtCore.SIGNAL("clicked()") , self.removeHistory)
        button_remove_history.setMaximumWidth(50)
        hbox_regex1.addWidget(button_remove_history)  
        
        # lineEdit for Regex
        self.line_regex = QtGui.QLineEdit()
        hbox_regex2.addWidget(self.line_regex)
        
        # button "بحث" to do that regex
        button_regex = QtGui.QPushButton((u"بحث") )
        hbox_regex2.addWidget(button_regex)
        button_regex.connect(button_regex, QtCore.SIGNAL("clicked()") , self.getContentURL)
        
        #########################
        # Label textURL (the links to search within)
        label_result = QtGui.QLabel((u"ناتج البحث : ") )
        Grid.addWidget(label_result)
        #text (set of links like "http://www.goog.com\nhttp://www.goog.com" )
        self.result = QtGui.QTextEdit()
        self.result.setFont(QtGui.QFont('ubuntu mono', 11))
        Grid.addWidget(self.result)
        
        
        #########################
        self.win.show()
        
        sys.exit(app.exec_())
    
    def getContentURL(self):
        
        self.addLineRegexIntoXMLFile()
        
        stringURL = str( self.textURL.toPlainText() ) # get string from textURL
        
        # check if textURL is empty 
        if stringURL == "":
            return False
        
        self.listURL = string.split(stringURL,  "\n" ) # change stringURL into listURL,separated by new line
        
        self.list_result = [] # all result as list
        
        # loop and open all URL in listURL
        # find the regex and add it into 
        for url in self.listURL:
            
            
            try:
                open = urllib2.urlopen(url) # open
                read = open.read()          # read
                self.list_result.append( self.getTextByRegex(read) )   # find the regex
                close = open.close()        # close
            except:
                print "Error"
            
        #########
        # set text into result box
        result_text = "\n".join(self.list_result) # change list_result into result_text
        
        self.result.setText(result_text) # set result text in result box
        
        
        
    def getTextByRegex(self , theCodeHTML):
        
        # Find all lineRegex in codeHTML by (re.findall)
        # remove all duplicate items by (set)
        list = set( re.findall(str( self.line_regex.text() ), theCodeHTML) ) 
        
        # change from type(set) into list
        list_result = "" # the result list
        for item in list:
            list_result  = item
        
        return list_result
    
    ###################################
    # add content line regex into combobox history
    # add the regex into XML file for history
    def addLineRegexIntoXMLFile(self):
        
        if self.line_regex.text() == "" or self.history_list.indexOf( self.line_regex.text() , 0) > -1:
            return False        
        
        # add value of regex line into history combobox
        self.history_list.append(QtCore.QString(self.line_regex.text() ))
        
        ################
        # add the regex into XML file for history
        
        regex = ET.SubElement(self.rootXML, "regex" )
        regex.text = str(self.line_regex.text())
        
        self.treeXML.write(self.FileXML)
        
    ###################
    # when select itme from list history
    # do that
    def activatedHistory(self , text):
        if str(text) == u"الذاكرة":
            self.line_regex.setText("")
            return 
        self.line_regex.setText(text)
    
    ####################
    # remove all history from file XML
    def removeHistory(self):
        
        # find all element regex and remove them
        for sub in self.treeXML.findall("regex"):
            self.rootXML.remove(sub)
        
        # write the chages
        self.treeXML.write(self.FileXML)

# run the programe
if __name__ == "__main__":
    
    FindTextAtURL = FindTextAtURL()
