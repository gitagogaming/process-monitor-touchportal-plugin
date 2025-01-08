#Process Monitor
# Created by @Gitago for TouchPortal
# Jan, 2023

## If users ever want multiple PIDS for the .exe we can make an action take it as an argument and then when user selects .exe it will show all the PIDs for that .exe and user can select which one they want to monito
## BUGS
## when process is checked with a 0 timer it is still counting as an active monitor although its only checking it once and stopping..
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
from datetime import datetime
PLUGIN_NAME = "Process Monitor"
PLUGIN_ID = "tp.plugin.process_monitor"
GITHUB_URL = "process-monitor-touchportal-plugin"

DEFAULT_STATES = ['pid', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time', 'status']


class ProcessMonitorData:
    def __init__(self):
        self.process_monitor_choiceList = []
        self.process_monitor_dict = {}

    def add_to_choiceList(self, item):
        self.process_monitor_choiceList.append(item)
        
    def add_to_dict(self, key, value):
        self.process_monitor_dict[key] = value

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


    def setClosedState(self):
        stateList = []
        for x in DEFAULT_STATES:
            if x == 'status':
            # Updating Status to "Closed" since the process appears to not be running
                stateList.append({
                    "id": PLUGIN_ID + f".state.{self.process_name}.process_info.status",
                    "desc": f"PM | {self.process_name} - status",
                    "value":"closed",
                    'parentGroup':str(self.process_name)
                })
            else:
                stateList.append({
                    "id": PLUGIN_ID + f".state.{self.process_name}.process_info.{x}",
                    "desc": f"PM | {self.process_name} - {x}",
                    "value":"", 'parentGroup':str(self.process_name),
                    "parentGroup": str(self.process_name)
                    })

            TPC.TPClient.createStateMany(stateList)

    
    def setRunningState(self, process_checked):

        print("Process Checked: ", process_checked)
        stateList = []
        for x in process_checked:
            if x == 'memory_percent':
                ## Round it to the 2nd decimal place
                process_checked[x] = round(process_checked[x], 2)
                
            if x == 'create_time':
                create_time = process_checked.get('create_time', "None")
                if create_time is not None:
                    create_time_datetime = datetime.fromtimestamp(create_time)
                    process_checked[x] = create_time_datetime.strftime("%m/%d/%Y [%I:%M:%S %p]")

            stateList.append({
                "id": PLUGIN_ID + f".state.{self.process_name}.process_info.{x}",
                "desc": f"PM | {self.process_name} - {x}",
                "value":str(process_checked.get(x, "None")),
                "parentGroup": str(self.process_name)
            })
                    
        TPC.TPClient.createStateMany(stateList)
        

    
    def addToChoiceList(self, the_process):
        PM.add_to_dict(self.process_name, the_process)
        choice_list = list(PM.process_monitor_dict.keys())
        choice_list.append("ALL")
        
        # Checking to see if the Process monitor Choice List is the same, if so we dont update it
        if PM.process_monitor_choiceList != choice_list:
            ## submitted a PR for this to be added to the API by default
            TPC.TPClient.choiceUpdate(choiceId=PLUGIN_ID + ".act.process_name.stop", values=choice_list)

        PM.add_to_choiceList(choice_list)
        # process_monitor_choiceList = the_list
        
        ## update a state showing how many values are in the list minus the "ALL" value
        TPC.TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue=str(len(choice_list) - 1))


    def the_task(self, process_name, the_process):
        process_checked = self.is_running()
        print("Process Checked: ", process_checked)
        
        if process_checked == False:
            self.setClosedState()
            
        if process_checked:
            self.addToChoiceList(the_process)
            self.setRunningState(process_checked)

            TPC.g_log.debug(f"{the_process.process_name} is running")
            
                
                
    def is_running(self): 
        for process in psutil.process_iter():
            if process.name().lower() == self.process_name.lower():
                process_Info = process.as_dict(attrs=DEFAULT_STATES)
                process_Info["cmdline"] = ' '.join(process_Info["cmdline"])
                return process_Info
        
        return False
    
    
    def check_continuously(self, interval, process_name, the_process):
        while self.should_continue:
            TPC.g_log.debug("Checking if " + self.process_name + " is running")         
            self.the_task(process_name = process_name, the_process=the_process)
            time.sleep(interval)      
        return False
    
    
    def stop(self):
        self.should_continue = False

class TPClientClass:
    def __init__(self, pluginId, sleepPeriod=0.05, autoClose=True, checkPluginId=True, maxWorkers=4, updateStatesOnBroadcast=False):
        self.pluginId = pluginId
        self.sleepPeriod = sleepPeriod
        self.autoClose = autoClose
        self.checkPluginId = checkPluginId
        self.maxWorkers = maxWorkers
        self.updateStatesOnBroadcast = updateStatesOnBroadcast
        try:
            self.TPClient = TP.Client(
                pluginId=self.pluginId,
                sleepPeriod=self.sleepPeriod,
                autoClose=self.autoClose,
                checkPluginId=self.checkPluginId,
                maxWorkers=self.maxWorkers,
                updateStatesOnBroadcast=self.updateStatesOnBroadcast
            )
            self.g_log = getLogger()
        except Exception as e:
            sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")



TPC = TPClientClass(PLUGIN_ID)

@TPC.TPClient.on(TP.TYPES.onNotificationOptionClicked)
def check_noti(data):
    if data['optionId'] == PLUGIN_ID+ '.update.download':
        github_check = TP.Tools.updateCheck("GitagoGaming",GITHUB_URL)
        url = f"https://github.com/gitagogaming/{GITHUB_URL}/releases/tag/{github_check}"
        webbrowser.open(url, new=0, autoraise=True)


@TPC.TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    TPC.g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    TPC.g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)

    if settings:#('Auto Monitor Programs (comma seperated)') != "":
        auto_monitor_programs = settings[0]['The Programs to Monitor (comma separated)']

        if auto_monitor_programs != "":
            auto_monitor_programs = auto_monitor_programs.split(",")
            every_X_seconds = 5 ## default to 5 seconds unless specified in settings
            if settings[1]['Check every x seconds'] != "":
                every_X_seconds = int(settings[1]['Check every x seconds'])

            for x in auto_monitor_programs:
                TPC.g_log.info(f"Checking every 5 seconds for {x}")
                the_process = ProcessChecker(x)
                if x not in PM.process_monitor_dict.keys():
                    th = threading.Thread(target=the_process.check_continuously, args=(every_X_seconds , x, the_process))
                    th.start()


    plugin_update_check(data)

    TPC.TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue="0")
        


@TPC.TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    TPC.g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)

    
    if settings:#('Auto Monitor Programs (comma seperated)') != "":
        auto_monitor_programs = settings[0]['The Programs to Monitor (comma separated)']

        if auto_monitor_programs != "":
            auto_monitor_programs = auto_monitor_programs.split(",")
            every_X_seconds = 5 ## default to 5 seconds unless specified in settings
            if settings[1]['Check every x seconds'] != "":
                every_X_seconds = int(settings[1]['Check every x seconds'])

            for x in auto_monitor_programs:
                TPC.g_log.info(f"Checking every 5 seconds for {x}")
                the_process = ProcessChecker(x)
                if x not in PM.process_monitor_dict.keys():
                    th = threading.Thread(target=the_process.check_continuously, args=(every_X_seconds , x, the_process))
                    th.start()

                    




@TPC.TPClient.on(TP.TYPES.onAction)
def onAction(data):
    TPC.g_log.debug(f"Action: {data}")
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return
    
    ##  Get Color from Mouse
    if data['actionId'] == PLUGIN_ID + ".act.check_process":
        
        if data['data'][1]['value']:
            if data['data'][1]['value'] == "0":
                the_process = ProcessChecker(data['data'][0]['value'])
                the_process.the_task(process_name=data['data'][0]['value'], the_process=the_process)
            else:
                TPC.g_log.info('Checking every ' + str(data['data'][1]['value']) + ' seconds for ' + data['data'][0]['value'])
                the_process = ProcessChecker(data['data'][0]['value']) 
                
                if data['data'][0]['value'] not in PM.process_monitor_dict.keys():
                    
                    th = threading.Thread(target=the_process.check_continuously, args=(int(data['data'][1]['value']), data['data'][0]['value'], the_process))
                    th.start()             

        
    if data['actionId'] == PLUGIN_ID +".act.stop_process.Monitor":
        the_process = data['data'][0]['value']
        try:
            if the_process =="ALL":
                for x in PM.process_monitor_dict:
                    TPC.g_log.info(f"Stopping the process monitor for: {x}")
                    if x != "ALL":
                        PM.process_monitor_dict[x].stop()
                        TPC.g_log.info(f"Stopping the process monitor for: {x}")
                        
                PM.process_monitor_dict = {}
            else:
                PM.process_monitor_dict[the_process].stop()
                ## delete the key from the dict
                TPC.g_log.info(f"Stopping the process monitor for: {the_process}")
                PM.process_monitor_dict.pop(the_process)
                
            TPC.TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.process_monitor.count", stateValue=str(len(PM.process_monitor_dict.keys())))
        except Exception as e:
            TPC.g_log.error(f"Error stopping the process: {e} - Current Monitors: {PM.process_monitor_dict}")
    

def handleSettings(settings, on_connect=False):
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
            
            TPC.TPClient.showNotification(
                    notificationId=PLUGIN_ID + ".update.check",
                    title=f"{PLUGIN_NAME} Plugin {github_check} is available",
                    msg=f"A new version of {PLUGIN_NAME} is available and ready to Download. This may include Bug Fixes and or New Features\n\nPatch Notes\n{message} ",
                    options= [{
                    "id":PLUGIN_ID + ".update.download",
                    "title":"Click to Update!"
                    }])
    except Exception as e:
        TPC.g_log.error("[UPDATE CHECK] Something went wrong checking update", e)


# Shutdown handler
@TPC.TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    TPC.g_log.info('Received shutdown event from TP Client.')


def main():
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
        TPC.g_log.addHandler(NullHandler())
    else:
        # set up pretty log formatting (similar to TP format)
        fmt = Formatter(
            fmt="{asctime:s}.{msecs:03.0f} [{levelname:.1s}] [{filename:s}:{lineno:d}] {message:s}",
            datefmt="%H:%M:%S", style="{"
        )
        # set the logging level
        if   opts.d: TPC.g_log.setLevel(DEBUG)
        elif opts.w: TPC.g_log.setLevel(WARNING)
        else:        TPC.g_log.setLevel(INFO)
        # set up log destination (file/stdout)
        if opts.l:
            try:
                # note that this will keep appending to any existing log file
                fh = FileHandler(str(opts.l))
                fh.setFormatter(fmt)
                TPC.g_log.addHandler(fh)
            except Exception as e:
                opts.s = True
                print(f"Error while creating file logger, falling back to stdout. {repr(e)}")
        #if not opts.l or opts.s:
        #    sh = StreamHandler(sys.stdout)
        #    sh.setFormatter(fmt)
        #    TPC.g_log.addHandler(sh)


    try:
        TPC.TPClient.connect()
        TPC.g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        TPC.g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        TPC.g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPC.TPClient.disconnect()
    del TPC.TPClient
    return ret


if __name__ == "__main__":
    PM = ProcessMonitorData()
    sys.exit(main())
    


#  import win32gui
#  import win32process
#  import psutil
#  
#  process_info = None
#  ### have to make a special 'check' in the plugin action to see if process is 'visible' rather than running..
#  ## this will help people determine if a browser source is actually open or not.. this needs to be optional as if we take out iswindowvisible then it says msedge is open even though its not..
#  def callback(hwnd, app_processes):
#      global process_info
#      if win32gui.IsWindowVisible(hwnd):
#          try:
#              pid = win32process.GetWindowThreadProcessId(hwnd)[1]
#              process = psutil.Process(pid)
#              if process.name().lower() in app_processes:
#                  process_info = process.as_dict(attrs=['num_threads','pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time', 'status', 'cwd', 'exe'])
#                  app_processes[process.name().lower()] = True
#               
#          except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#              pass
#  
#  # define the process names for different browsers
#  app_process = {'msedge.exe': False}
#  
#  # loop through all the windows and check if any belong to the browser process
#  win32gui.EnumWindows(callback, app_process)
#  
#  # check if any of the browser processes have an open window
#  for process_name, has_window in app_process.items():
#      if has_window:
#          print(f"Yes, a {process_name} window is open")
#      else:
#          print(f"No, a {process_name} window is not open")
