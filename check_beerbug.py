#!/usr/bin/python

import sys
import json, requests
import pynagios
from pynagios import Plugin, make_option, Response, UNKNOWN

# SETTINGS
apikey=""
bugid=""


class beerbug(Plugin):

        data = make_option("-d","--data", dest="data",type="int", help="1=Battery, 2=sg, 3=plato, 4=al, 5=beerbug temperature, 6=probe temperature, 7=process")
        tempunit = make_option("-u", "--unit", dest="tempunit", type="string", help="c=celcius, f=farenheit")

        def check(self):
          data = self.options.data
          tempunit = self.options.tempunit
          j =  self.apijson()

          #Battery Percentage
          if data == 1:
            unit = "%"
            result = self.response_for_value(j['battPercentage'], message=j['battPercentage'])
            result.set_perf_data("Battery %", j['battPercentage'],uom=unit,warn=self.options.warning,crit=self.options.critical)
            return result

          # Specific Gravity
          elif data == 2:
            unit = ""
            result = self.response_for_value(j['sg'], message=j['sg'])
            result.set_perf_data("SG", j['sg'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Plato
          elif data == 3:
            unit = ""
            result = self.response_for_value(j['plato'], message=j['plato'])
            result.set_perf_data("Plato", j['plato'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Alcohol
          elif data == 4:
            unit = "%"
            result = self.response_for_value(j['al'], message=j['al'])
            result.set_perf_data("Alcohol", j['al'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Progress
          elif data == 7:
            unit = "%"
            result = self.response_for_value(j['progress'], message=j['progress'])
            result.set_perf_data("Progress", j['progress'],uom=unit,warn=self.options.warning,crit=self.options.critical)
            return result

          # Beerbug Temp in F
          elif data == 5 and tempunit == 'f':
            unit = "F"
            result = self.response_for_value(j['t1f'], message=j['t1f'])
            result.set_perf_data("Beerbug Temperature", j['t1f'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Probe Temp in F
          elif data == 6 and tempunit == 'f':
            unit = "F"
            result = self.response_for_value(j['t2f'], message=j['t2f'])
            result.set_perf_data("Probe Temperature", j['t2f'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Beerbug Temp in C
          elif data == 5 and tempunit == 'c':
            unit = "C"
            result = self.response_for_value(j['t1c'], message=j['t1c'])
            result.set_perf_data("Beerbug Temperature", j['t1c'],warn=self.options.warning,crit=self.options.critical)
            return result

          # Probe Temp in C
          elif data == 6 and tempunit in "c":
            unit = "C"
            result = self.response_for_value(j['t2c'], message=j['t2c'])
            result.set_perf_data("Probe Temperature", j['t2c'],warn=self.options.warning,crit=self.options.critical)
            return result

          else:
            print "options are not correct"
            sys.exit()

        def apijson(self):
            r = requests.get('http://www.thebeerbug.com/api/?api_key=%s&beerbug_id=%s' % (apikey, bugid))
            if r.status_code != 200:
              exitmsg = "Unable to contact server, errorcode: %s" % r.status.code
              exitstatus=3

            j = json.loads(r.text)
            exitstatus = 0

            if j['success'] == False:
              exitmsg =  "Failure, Errorcode: %s" % j['reason']
              exitstatus=3

            if exitstatus == 3:
              print exitmsg
              sys.exit(3)
            else:
              result = self.response_for_value(j['battPercentage'], message=j['battPercentage'])
              return j


if __name__ == "__main__":
  beerbug().check().exit()
