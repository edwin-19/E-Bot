# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 01:39:27 2017

@author: Edwin
"""

import datetime
from dateutil.parser import parse

class Utilities:
   def convertDateTime(self, oldDate, previousFormat, currentFormat):
       newDate = ""
       try:
           if oldDate != "":
               if previousFormat != "" and currentFormat != "":
                   newDate = datetime.datetime.strptime(oldDate,previousFormat).strftime(currentFormat)
               else:
                   print("Not previous format or current format")
           else:
               print("No date entered")
       except Exception as ex:
           print("Error: " + str(ex))
          
       return newDate
   
   def is_date(self,string):
        try:
            parse(string)
            return True
        except ValueError:
            return False