
# Process-Monitor
- [Process Monitor](#Process-Monitor)
  - [Description](#description)
  - [Features](#Features)
    - [Actions](#actions)
        - [Category: Process Monitor](#tp.plugin.process_monitor.mainactions)
    - [States](#states)
        - [Category: Process Monitor](#tp.plugin.process_monitor.mainstates)
  - [Bugs and Support](#bugs-and-suggestion)
  - [License](#license)
  
# Description
 Check the status of a process that is running on your computer.
 
 You can utilize this plugin by checking if another plugin .exe is running.. and if its not then launch it.. this will make sure that if a plugin crashes that it reloads for you.
 
 
![image](https://user-images.githubusercontent.com/76603653/213901271-82eb4b9e-767d-44cc-a8d6-92e908c4c72e.png)


# Features

## Actions
<details open id='tp.plugin.process_monitor.mainactions'><summary><b>Category:</b> Process Monitor <small><ins>(Click to expand)</ins></small></summary><table>
<tr valign='buttom'><th>Action Name</th><th>Description</th><th>Format</th><th nowrap>Data<br/><div align=left><sub>choices/default (in bold)</th><th>On<br/>Hold</sub></div></th></tr>
<tr valign='top'><td>Check If Process is Running</td><td> </td><td>Get Process Status [1] - Every [2] Seconds</td><td><ol start=1><li>Type: text &nbsp; 
Default: <b>TouchPortal.exe</b></li>
<li>Type: choice &nbsp; 
Default: <b>0</b> Possible choices: ['0', '5', '10', '15', '30', '45', '60', '120', '240']</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>Stop Process Monitor for [X]</td><td> </td><td>Stop [1] Process Monitor</td><td><ol start=1><li>Type: choice &nbsp; 
Default: <b>ALL</b> Possible choices: ['ALL']</li>
</ol></td>
<td align=center>No</td>
</tr></table></details>
<br>

## States
<details open id='tp.plugin.process_monitor.mainstates'><summary><b>Category:</b> Process Monitor <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .state.process_monitor.count | PM |  Total Process Monitors Running |  |   |
</details>

<br>

# Bugs and Suggestion
Open an issue on github or join offical [TouchPortal Discord](https://discord.gg/MgxQb8r) for support.


# License
This plugin is licensed under the [GPL 3.0 License] - see the [LICENSE](LICENSE) file for more information.

