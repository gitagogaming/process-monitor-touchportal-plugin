{"FF":"Default","A":[{"kPlugType":2,"kID":"tp.plugin.process_monitor.act.check_process","kPrefix":"Process Monitor","kInline":"false","kHHF":"false","kcD":-13684945,"kPID":"tp.plugin.process_monitor","kData":[{"default":"TouchPortal.exe","id":"tp.plugin.process_monitor.act.process_name","label":"Text","type":"text"},{"default":"0","id":"tp.plugin.process_monitor.act.process_name.checktime","label":"check every x seconds","valueChoices":["0","5","10","15","30","45","60","120","240"],"type":"choice"}],"kVals":[{"VAL":"obs64.exe","ID":"tp.plugin.process_monitor.act.process_name","TYPE":"text"},{"VAL":"0","ID":"tp.plugin.process_monitor.act.process_name.checktime","TYPE":"choice"}],"kStatic":"false","kcL":-7237231,"kET":0,"KEY_TYPE":"PLUGIN_ACTION","kFormat":"Get Process Status {$tp.plugin.process_monitor.act.process_name$} - Every {$tp.plugin.process_monitor.act.process_name.checktime$} Seconds","kName":"Check If Process is Running"}],"BD":1,"C":[],"BE":-13684944,"kSCM":25,"BG":-13684944,"E":[{"kTxt":"NAME:         ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.name}\nPID:              ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.pid}\nCPU:             ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.cpu_percent}%\nMEM:            ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.memory_percent}%\nSTATUS:       ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.status}\nCREATED:    ${value:tp.plugin.process_monitor.state.obs64.exe.process_info.create_time}","KEY_TYPE":"AUTO_UPDATE_EVENT"},{"KEY_STATE_DESCRIPTION":"On state changes to","kPSC":true,"KEY_IS_NOT_EQUAL":false,"kCSC":0,"KEY_STATE":"running","KEY_STATE_ID":"tp.plugin.process_monitor.state.obs64.exe.process_info.status","KEY_TYPE":"ON_STATE_AWARENESS_CHANGE","kICustom":false},{"KEY_START_COLOR":-13408717,"KEY_IS_ROUNDED":false,"KEY_IS_CHANGE_ICON":false,"KEY_END_COLOR":-6697831,"kiBD":false,"KEY_IS_CHANGE_IS_ROUNDED":false,"KEY_ALIGN_HOR":0,"KEY_IS_CHANGE_IS_TRANSPARENT":false,"KEY_TITLE":"","KEY_IS_FULL_ICON":false,"KEY_IS_CHANGE_ALIGN_VERT":false,"KEY_IS_CHANGE_IS_FULL_ICON":false,"kIAs":[],"KEY_IS_TRANSPARENT":false,"KEY_ALIGN_VERT":0,"KEY_TEXT_COLOR":-1,"KEY_IS_CHANGE_TITLE":false,"kTS":-1,"kBD":1,"KEY_IS_CHANGE_TEXT_COLOR":false,"KEY_FILENAME":"","KEY_IS_CHANGE_ALIGN_HOR":false,"kC":false,"KEY_TYPE":"CHANGE_BUTTON_VISUALS_ACTION","KEY_IS_CHANGE_BG_COLOR":true},{"KEY_STATE_DESCRIPTION":"On state changes to","kPSC":true,"KEY_IS_NOT_EQUAL":false,"kCSC":0,"KEY_STATE":"closed","KEY_STATE_ID":"tp.plugin.process_monitor.state.obs64.exe.process_info.status","KEY_TYPE":"ON_STATE_AWARENESS_CHANGE","kICustom":false},{"KEY_START_COLOR":-10066432,"KEY_IS_ROUNDED":false,"KEY_IS_CHANGE_ICON":false,"KEY_END_COLOR":-6711040,"kiBD":false,"KEY_IS_CHANGE_IS_ROUNDED":false,"KEY_ALIGN_HOR":0,"KEY_IS_CHANGE_IS_TRANSPARENT":false,"KEY_TITLE":"","KEY_IS_FULL_ICON":false,"KEY_IS_CHANGE_ALIGN_VERT":false,"KEY_IS_CHANGE_IS_FULL_ICON":false,"kIAs":[],"KEY_IS_TRANSPARENT":false,"KEY_ALIGN_VERT":0,"KEY_TEXT_COLOR":-1,"KEY_IS_CHANGE_TITLE":false,"kTS":-1,"kBD":1,"KEY_IS_CHANGE_TEXT_COLOR":false,"KEY_FILENAME":"","KEY_IS_CHANGE_ALIGN_HOR":false,"kC":false,"KEY_TYPE":"CHANGE_BUTTON_VISUALS_ACTION","KEY_IS_CHANGE_BG_COLOR":true},{"KEY_PATH":"E:\\OBS-Studio\\bin\\64bit\\obs64.exe","KEY_COMMANDLINE":" --startreplaybuffer --startvirtualcam --studio-mode","kWFE":false,"kRT":1,"kBT":"/bin/bash","KEY_TYPE":"START_APPLICATION_ACTION","kOB":false}],"kIAPBKC":-14803426,"I":"","ITS":true,"BiR":true,"kSCTY":0,"BiT":true,"kSCHS":false,"inS":"","IiS":false,"T":"Check obs64.exe","kSCAC":-14145496,"kSCC":-4611631,"kSCHRC":false,"THO":4,"id":"u811hne768qoa","GUdata":"","kSCIUFATS":false,"kCT":1,"kSIP":0,"TELS":5,"kSCI":"","kIAs":[],"GUid":-1,"kSCIIVA":true,"COLS":2,"TA":4,"TC":-1,"kSVP":0,"kSTP":0,"kSVAC":-10575407,"TO":4,"TP":2,"inB":false,"EXP":[],"kSD":0,"kSCTM":0,"TS":9,"inC":0,"ROWS":1}