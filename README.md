
# Process-Checker
- [Process Checker](#Process-Checker)
  - [Description](#description)
  - [Features](#Features)
    - [Actions](#actions)
        - [Category: Process Checker](#tp.plugin.process_checker.mainactions)
    - [States](#states)
        - [Category: Process Checker](#tp.plugin.process_checker.mainstates)
  - [Bugs and Support](#bugs-and-suggestion)
  - [License](#license)
  
# Description

This documentation generated for Process Checker V100 with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).
# Features

## Actions
<details open id='tp.plugin.process_checker.mainactions'><summary><b>Category:</b> Process Checker <small><ins>(Click to expand)</ins></small></summary><table>
<tr valign='buttom'><th>Action Name</th><th>Description</th><th>Format</th><th nowrap>Data<br/><div align=left><sub>choices/default (in bold)</th><th>On<br/>Hold</sub></div></th></tr>
<tr valign='top'><td>Check If Process is Running</td><td> </td><td>Get Process Status [1] - Every [2] Seconds</td><td><ol start=1><li>Type: text &nbsp; 
Default: <b>TouchPortal.exe</b></li>
<li>Type: choice &nbsp; 
Default: <b>0</b> Possible choices: ['0', '5', '10', '15', '30', '45', '60', '120', '240']</li>
</ol></td>
<td align=center>No</td>
</tr></table></details>
<br>

## States
<details open id='tp.plugin.process_checker.mainstates'><summary><b>Category:</b> Process Checker <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .state.current_text_name_style | Color Picker: Text Name Style |  |   |
| .state.last_mouse_x | Color Picker: Last Mouse Location - X |  |   |
</details>

<br>

# Bugs and Suggestion
Open an issue on github or join offical [TouchPortal Discord](https://discord.gg/MgxQb8r) for support.


# License
This plugin is licensed under the [GPL 3.0 License] - see the [LICENSE](LICENSE) file for more information.

