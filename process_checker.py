#Process Monitor
# Created by @Gitago for TouchPortal
# Jan, 2023


## BUGS
## when checking for a process if its NOT loaded, then no states are made or mention that its not running.. but if its runing then you close it updates as expected
# when stopping a monitor it doesnt seem to clear the length of total?

import TouchPortalAPI as TP
from argparse import ArgumentParser
from logging import (getLogger, Formatter, NullHandler, FileHandler, StreamHandler, DEBUG, INFO, WARNING)

from os import path
import psutil
import threading
import sys
import webbrowser
import time
import requests
import base64
import time

PLUGIN_NAME = "Process Monitor"
PLUGIN_ID = "tp.plugin.process_monitor"
GITHUB_URL = "process-monitor-touchportal-plugin"
# DEFAULT_CONFIG_SAVE_PATH = path.join(path.dirname(path.realpath(__file__)), "color_config.json")




process_monitor_choiceList = []
process_monitor_dict = {}

class ProcessChecker:
    def __init__(self, process_name):
        self.process_name = process_name
        self.should_continue = True
      #  self.process_monitor_choiceList = []
        

    def time_completion(self, data, the_process):
        start_time = time.time()
        self.the_task(data=data, the_process=the_process)
        end_time = time.time()
        completion_time = end_time - start_time
        print("Task completed in: ", completion_time, " seconds")


    def the_task(self, process_name, the_process):
        process_checked = self.is_running()
        
        global process_monitor_choiceList
        
      #  print("This is process checked the is_running stuff", process_checked)
        
        if process_checked == False:
            for x in ['pid', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time']:
                TPClient.createState(stateId=PLUGIN_ID + f".state.{self.process_name}.process_info.{x}", description=f"PM | {self.process_name} - {x}", value="", parentGroup=str(self.process_name))
            
            # Updating Status to "Closed" since the process appears to not be running
            TPClient.createState(stateId=PLUGIN_ID + f".state.{self.process_name}.process_info.status", description=f"PM | {self.process_name} - status", value="Closed", parentGroup=str(self.process_name))
            
        if process_checked:
            process_monitor_dict[process_name] = the_process
            the_list = list(process_monitor_dict.keys())
            the_list.append("ALL")
            
            # Checking to see if the Process monitor Choice List is the same, if so we dont update it
            if process_monitor_choiceList != the_list:
                ## submitted a PR for this to be added to the API by default
                TPClient.choiceUpdate(choiceId=PLUGIN_ID + ".act.process_name.stop", values=the_list)
          
            process_monitor_choiceList = the_list
            
            ## update a state showing how many values are in the list minus the "ALL" value
            TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue=str(len(the_list) - 1))
            
          #  print(f"{the_process.process_name} is running")
            
            for x in process_checked:
                if x == 'memory_percent':
                    ## Round it to the 2nd decimal place
                    process_checked[x] = round(process_checked[x], 2)
                    
                if x == 'create_time':
                    from datetime import datetime
                    create_time = process_checked.get('create_time', "None")
                    if create_time is not None:
                        create_time_datetime = datetime.fromtimestamp(create_time)
                        process_checked[x] = create_time_datetime.strftime("%m/%d/%Y [%I:%M:%S %p]")
                        
                ## use a thread to create sttes as fast as possible
                TPClient.createState(stateId=PLUGIN_ID + f".state.{the_process.process_name}.process_info.{x}", description=f"PM | {the_process.process_name} - {x}", value=str(process_checked.get(x, "None")), parentGroup=str(the_process.process_name))
                
                
    def is_running(self):
        
        for process in psutil.process_iter():
            if process.name().lower() == self.process_name.lower():
                process_Info = process.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time', 'status'])
                        #    print("Before joiing the cmdline: ", process_checked)
                process_Info["cmdline"] = ' '.join(process_Info["cmdline"])
            
           # print("After joiing the cmdline: ", process_checked)
             #  memory_info = process.memory_info().rss
             #  memory_mb = memory_info / 1048576
             #  process_Info['memory_MB'] = memory_mb
                return process_Info
        
        return False
    
    
    def check_continuously(self, interval, process_name, the_process):
        while self.should_continue:
            g_log.debug("Checking if " + self.process_name + " is running")
           # print("Checking if ",  self.process_name, " is running")
           
            self.the_task(process_name = process_name, the_process=the_process)
            time.sleep(interval)
            
        return False
    
    
    def stop(self):
        self.should_continue = False



### The TP Client
try:
    TPClient = TP.Client(
        pluginId = PLUGIN_ID,
        sleepPeriod = 0.05,
        autoClose = True,
        checkPluginId = True,
        maxWorkers = 4,
        updateStatesOnBroadcast = False,
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")


# Crate the global logger
g_log = getLogger()



@TPClient.on(TP.TYPES.onNotificationOptionClicked)
def check_noti(data):
    if data['optionId'] == PLUGIN_ID+ '.update.download':
        github_check = TP.Tools.updateCheck("GitagoGaming",GITHUB_URL)
        url = f"https://github.com/gitagogaming/{GITHUB_URL}/releases/tag/{github_check}"
        webbrowser.open(url, new=0, autoraise=True)



@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)
        
    plugin_update_check(data)
    TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue="0")
        


@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)




@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    global process_monitor_dict
    g_log.debug(f"Action: {data}")
    
    print(data)
    
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return
    
    ##  Get Color from Mouse
    if data['actionId'] == PLUGIN_ID + ".act.check_process":
        
        if data['data'][1]['value']:
            if data['data'][1]['value'] == "0":
                the_process = ProcessChecker(data['data'][0]['value'])
                the_process.the_task(process_name=data['data'][0]['value'], the_process=the_process)
            else:
                print(f"Checking every {str(data['data'][1]['value'])} seconds for {data['data'][0]['value']}")
                the_process = ProcessChecker(data['data'][0]['value']) 
                
                if data['data'][0]['value'] not in process_monitor_dict.keys():
                    
                    th = threading.Thread(target=the_process.check_continuously, args=(int(data['data'][1]['value']), data['data'][0]['value'], the_process))
                    th.start()
                    
                    
               # process_checked = the_process.check_continuously(int(data['data'][1]['value']), data=data['data'][0]['value'], the_process=the_process)
        
        
    if data['actionId'] == PLUGIN_ID +".act.stop_process.Monitor":
        the_process = data['data'][0]['value']
        try:
            if the_process =="ALL":
               # print("Trying to remove all processes from the dict")
                for x in process_monitor_dict:
            
                  #  print("Stopping the process: ", x)
                    if x != "ALL":
                        process_monitor_dict[x].stop()
                        g_log.debug(stopped_process := f"Stopping the process: {x}")
                        
                process_monitor_dict = {}
            else:
                process_monitor_dict[the_process].stop()
                ## delete the key from the dict
              #  print("Trying to remove the process {} from the dict".format(the_process))
                process_monitor_dict.pop(the_process)
                
            TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue=str(len(process_monitor_dict.keys())))
            #  del process_monitor_dict[the_process]
        except Exception as e:
            print(e)
    



def handleSettings(settings, on_connect=False):
    #print("Settings: " + str(settings))
    pass



def plugin_update_check(data):
    """ 
    Checks Github for the latest version of the plugin
    - Returns patchnotes on notification if there is a new version 
    """
    
    try:
        github_check = TP.Tools.updateCheck("GitagoGaming", GITHUB_URL).replace('v','').replace(".","")
        plugin_version = str(data['pluginVersion'])
        
        ## Checking to see if current version is different from github version
        if github_check != plugin_version:
            # Pulling Patch Notes for Notification
            r = requests.get(f"https://api.github.com/repos/GitagoGaming/{GITHUB_URL}/contents/recent_patchnotes.txt")
            message = base64.b64decode(r.json()['content']).decode('ascii')
            
            TPClient.showNotification(
                    notificationId=PLUGIN_ID + ".update.check",
                    title=f"{PLUGIN_NAME} Plugin {github_check} is available",
                    msg=f"A new version of {PLUGIN_NAME} is available and ready to Download. This may include Bug Fixes and or New Features\n\nPatch Notes\n{message} ",
                    options= [{
                    "id":PLUGIN_ID + ".update.download",
                    "title":"Click to Update!"
                    }])
    except Exception as e:
        g_log.error("[UPDATE CHECK] Something went wrong checking update", e)




# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')



















## The Main + Logging System
def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    # handle CLI arguments
    parser = ArgumentParser()
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help="Log to this file (default is stdout).")
    parser.add_argument("-s", action='store_true',
                        help="If logging to file, also output to stdout.")

    opts = parser.parse_args()
    del parser

    # set up logging
    if opts.q:
        # no logging at all
        g_log.addHandler(NullHandler())
    else:
        # set up pretty log formatting (similar to TP format)
        fmt = Formatter(
            fmt="{asctime:s}.{msecs:03.0f} [{levelname:.1s}] [{filename:s}:{lineno:d}] {message:s}",
            datefmt="%H:%M:%S", style="{"
        )
        # set the logging level
        if   opts.d: g_log.setLevel(DEBUG)
        elif opts.w: g_log.setLevel(WARNING)
        else:        g_log.setLevel(INFO)
        # set up log destination (file/stdout)
        if opts.l:
            try:
                # note that this will keep appending to any existing log file
                fh = FileHandler(str(opts.l))
                fh.setFormatter(fmt)
                g_log.addHandler(fh)
            except Exception as e:
                opts.s = True
                print(f"Error while creating file logger, falling back to stdout. {repr(e)}")
        if not opts.l or opts.s:
            sh = StreamHandler(sys.stdout)
            sh.setFormatter(fmt)
            g_log.addHandler(sh)


    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

   # g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret


if __name__ == "__main__":
    sys.exit(main())
