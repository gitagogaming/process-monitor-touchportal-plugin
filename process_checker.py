#process checker



import TouchPortalAPI as TP
from argparse import ArgumentParser
from logging import (getLogger, Formatter, NullHandler, FileHandler, StreamHandler, DEBUG, INFO, WARNING)

from os import path
import psutil
import sys
import webbrowser
import time

PLUGIN_NAME = "Process Checker"
PLUGIN_ID = "tp.plugin.process_checker"
GITHUB_URL = "process-checker-touchportal-plugin"
# DEFAULT_CONFIG_SAVE_PATH = path.join(path.dirname(path.realpath(__file__)), "color_config.json")

def handleSettings(settings, on_connect=False):
    ## Setting the Color Naming Convention based on user input
    print("Settings: " + str(settings))
  #  the_colors.color_name_setting = settings[0]['Color Names - Can be changed via plugin actions']
   # TPClient.stateUpdate(stateId=PLUGIN_ID + ".state.current_text_name_style", stateValue=the_colors.color_name_setting)







import time

class ProcessChecker:
    def __init__(self, process_name):
        self.process_name = process_name
        self.should_continue = True
        
        

    def time_completion(self, data, the_process):
        start_time = time.time()
        self.the_task(data=data, the_process=the_process)
        end_time = time.time()
        completion_time = end_time - start_time
        print("Task completed in: ", completion_time, " seconds")



    def the_task(self, data, the_process):
        #print("this is data, {} and this is process {}".format(data, the_process))
        #the_process = ProcessChecker(data) 
        process_checked = self.is_running()
        
        if process_checked == False:
          #  print(self.process_name + " is not running")
            for x in ['pid', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time']:
                TPClient.createState(stateId=PLUGIN_ID + f".state.{self.process_name}.process_info.{x}", description=f"PM | {self.process_name} - {x}", value="", parentGroup=str(self.process_name))
            
            TPClient.createState(stateId=PLUGIN_ID + f".state.{self.process_name}.process_info.status", description=f"PM | {self.process_name} - status", value="Closed", parentGroup=str(self.process_name))
            
      # print("this is process checked {}".format(process_checked))
        
        
        if process_checked:

            print(f"{the_process.process_name} is running")

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
            if process.name() == self.process_name:
                process_Info = process.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline', 'create_time', 'status'])
                return process_Info
        
        return False
    
    
    
    def check_continuously(self, interval, data, the_process):
        while self.should_continue:
            g_log.debug("Checking if " + self.process_name + " is running")
           # print("Checking if ",  self.process_name, " is running")
            self.the_task(data, the_process=the_process)
            time.sleep(interval)
            
        return False

    
    
    def stop(self):
        self.should_continue = False



# ## STARTING THE THING
# pc = ProcessChecker("WizLight_Plugisn.exe")
# 
# is_running = pc.is_running()
# 
# check_always = pc.check_continuously(10)








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
        



@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)


# import time
# 
# def time_completion(data, the_process):
#     start_time = time.time()
#     the_task(data=data, the_process=the_process)
#     end_time = time.time()
#     completion_time = end_time - start_time
#     print("Task completed in: ", completion_time, " seconds")
# 
# 
# 
# def the_task(data, the_process):
#     
#     print("this is data, {} and this is process {}".format(data, the_process))
#     #the_process = ProcessChecker(data) 
#     process_checked = the_process.is_running()
#     if process_checked:
#         g_log.info(f"{the_process.process_name} is running")
#         
#         for x in process_checked:
#             if x == 'memory_percent':
#                 ## Round it to the 2nd decimal place
#                 process_checked[x] = round(process_checked[x], 2)
#             
#             if x == 'create_time':
#                 from datetime import datetime
#                 create_time = process_checked.get('create_time', "None")
#                 if create_time is not None:
#                     create_time_datetime = datetime.fromtimestamp(create_time)
#                     process_checked[x] = create_time_datetime.strftime("%m/%d/%Y [%I:%M:%S %p]")
#                     
#             ## use a thread to create sttes as fast as possible
#             TPClient.createState(stateId=PLUGIN_ID + f".state.{the_process.process_name}.process_info.{x}", description=f"PM | {the_process.process_name} - {x}", value=str(process_checked.get(x, "None")), parentGroup=str(the_process.process_name))



@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    g_log.debug(f"Action: {data}")
    
    print(data)
    
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return

    ##  Get Color from Mouse
    if data['actionId'] == PLUGIN_ID + ".act.check_process":
        
        if data['data'][1]['value']:
            if data['data'][1]['value'] == "0":
                the_process = ProcessChecker(data['data'][0]['value']) 
                #the_process.time_completion(data=data['data'][0]['value'], the_process=the_process)
                the_process.the_task(data=data, the_process=the_process)
            else:
                print(f"We are gonna check every {str(data['data'][1]['value'])} seconds")
                the_process = ProcessChecker(data['data'][0]['value']) 
                process_checked = the_process.check_continuously(int(data['data'][1]['value']), data=data['data'][0]['value'], the_process=the_process)
               # print(process_checked)

        
      # the_process = ProcessChecker(data['data'][0]['value']) 
      # process_checked = the_process.get_process_info()
      # if process_checked:
      #     g_log.info(f"{the_process.process_name} is running")
      #     
      #     g_log.debug(f"Process Info: {process_checked}")
      #     
      #     print(process_checked)
      #     for x in process_checked:
      #         if x == 'memory_percent':
      #             ## Round it to the 2nd decimal place
      #             process_checked[x] = round(process_checked[x], 2)
      #         
      #         if x == 'create_time':
      #             from datetime import datetime
      #             create_time = process_checked.get('create_time', "None")
      #             if create_time is not None:
      #                 create_time_datetime = datetime.fromtimestamp(create_time)
      #                 process_checked[x] = create_time_datetime.strftime("%m/%d/%Y [%I:%M:%S %p]")
      #             
      #         TPClient.createState(stateId=PLUGIN_ID + f".state.{the_process.process_name}.process_info.{x}", description=f"PM | {the_process.process_name} - {x}", value=str(process_checked.get(x, "None")), parentGroup=str(the_process.process_name))





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
    
    


## stop it
#pc.stop()
