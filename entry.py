#entry.py


## Entry.py - ColorPicker


__version__ = 1.4
PLUGIN_ID = "tp.plugin.process_monitor"
PLUGIN_NAME = "Process_Monitor"

# Basic plugin metadata
TP_PLUGIN_INFO = {
    'sdk': 6,
    'version': int(float(__version__) * 100),  # TP only recognizes integer version numberstopo
    'name': "Process Monitor",
    'id': PLUGIN_ID,
    "plugin_start_cmd": f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\{PLUGIN_NAME}.exe",
    "plugin_start_cmd_mac": f"sh %TP_PLUGIN_FOLDER%{PLUGIN_NAME}//start.sh {PLUGIN_NAME}",
    "plugin_start_cmd_linux": f"sh %TP_PLUGIN_FOLDER%{PLUGIN_NAME}//start.sh {PLUGIN_NAME}",
    'configuration': {
        'colorDark': "#2f2f2f",
        'colorLight': "#919191"
    }

}



TP_PLUGIN_SETTINGS = {
   #'example': {
   #    'name': "Color Names - Can be changed via plugin actions",
   #    'type': "text",
   #    'default': "Basic",
   #    'readOnly': True,
   #    'value': None  # we can optionally use the settings struct to hold the current value
   #}
}

# This example only uses one Category for actions/etc., but multiple categories are supported also.
TP_PLUGIN_CATEGORIES = {
    "main": {
        'id': PLUGIN_ID + ".main",
        'name' : "Process Monitor",
        'imagepath': f"%TP_PLUGIN_FOLDER%{PLUGIN_NAME}\\{PLUGIN_NAME.lower()}_icon.png",
    },
    "current": {
        'id': PLUGIN_ID + ".current",
        'name' : "Process Monitor | Category 1",
    }           
                
}

# Action(s) which this plugin supports.
TP_PLUGIN_ACTIONS = {
    'Process Monitor': {
        'category': "main",
        'id': PLUGIN_ID + ".act.check_process",
        'name': "Check If Process is Running",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        'format': "Get Process Status $[1] - Every $[2] Seconds",
        'data': {
            'text_color': {
                'id': PLUGIN_ID + ".act.process_name",
                'type': "text",
                'label': "Text",
                'default': "TouchPortal.exe"
            },
              'check_per_seconds': {
               'id': PLUGIN_ID + ".act.process_name.checktime",
               'type': "choice",
               'label': "check every x seconds",
               'default': "0",
               'valueChoices': ["0","5", "10", "15", "30", "45", "60", "120", "240"]
           },
        }
    },
    
    'Stop Process Monitor': {
        'category': "main",
        'id': PLUGIN_ID + ".act.stop_process.Monitor",
        'name': "Stop Process Monitor for [X]",
        'prefix': TP_PLUGIN_CATEGORIES['main']['name'],
        'type': "communicate",
        'tryInline': True,
        'format': "Stop $[1] Process Monitor",
        'data': {
            'Process Name to Stop': {
                'id': PLUGIN_ID + ".act.process_name.stop",
                'type': "choice",
                'label': "Text",
                'default': "ALL",
                'valueChoices': ["ALL"]
            }
       #       'check_per_seconds': {
       #        'id': PLUGIN_ID + ".act.process_name.checktime",
       #        'type': "choice",
       #        'label': "check every x seconds",
       #        'default': "0",
       #        'valueChoices': ["0","5", "10", "15", "30", "45", "60", "120", "240"]
       #    },
        }
    },
    
    
}

TP_PLUGIN_STATES = {
    'Total Monitors Running': {
        'category': "main",
        'id': PLUGIN_ID + ".state.process_monitor.count",
        'desc': "PM |  Total Process Monitors Running",
        'default': ""
    }
}

# Plugin Event(s).
TP_PLUGIN_EVENTS = {}