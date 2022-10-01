# CPU_GPU_RAM_MONITOR_WIDGET

## Set-Up
  ↠ Open system_info folder. <br>
  ↠ Just DoubleClick sys_info_setup.py <br>
  
  That's it, now wait for few seconds until monitor widget launches <br>
  
## Delete Set-Up 
  ⇨ Open system_info folder <br>
  ⇨ Run Delete_SetUp.py <br>
  
## Future's 
  ⋙ It automatically pop up when you start up or restart of your system. <br>
  ⋙ It show info about CPU, GPU, RAM and DISK usage, temperature, consuming wattage. <br>
  ⋙ Double any where to see more info about CPU, GPU, RAM and DISK usage. <br>
  ⋙ As the TempINFO.exe file generate result.json under system_info/assets/TempINFO folder file you can also use it for your project. <br>
  ⋙ TempInfo.exe also provide moreInfo.txt file under system_info/assets/TempINFO folder for more information of your system deatials and performance. <br>
  ⋙ It automaticaly store the last position and size in property.json file before close, So it can able to open in last position when close. <br>
  ⋙ Nice look animation😁 <br>
  
## Working Algorithm 
  ⇒ When you Double-Click the sys_info_setup.py, it call requirment_installer.py to install required modules. <br>
  ⇒ It check for run asAdmin if not ask permission. <br>
  ⇒ If user give permission, it schedule TempINFO.exe file (system_info/assets/TempInfo) to task scheduler for bipass administrator mode. <br>
  ⇒ Create scheduled task shortcut in assets folder with name of 'TempInfo.lnk'. <br>
  ⇒ Exclude working directory folder from windows virus & threat production. <br>
  ⇒ Add sys_info.pyw to registry for start automaticaly when system startup. <br>
  ⇒ Call sys_info.pyw -> load() to run. <br>
  ⇒ sys_info.pyw run TempInfo.lnk file -> TempINFO.exe generates result.json file. <br>
  ⇒ sys_info.pyw read's result.json file and get information then display. <br>
  ⇒ Update information at every 1sec. <br>
  ⇒ On system ShurtDown sys_info.pyw terminate TempINFO.exe and update current position in property.json then exit. <br>
  ⇒ ends. <br>
  
## GIF

<img src="https://github.com/prasanna892/CPU_GPU_RAM_MONITOR_WIDGET/blob/main/Video.gif" />
  
## Notes
  ⇾ Some times the widget did not pop up at first setup run beacuse of any antivirus app you installed in your system. <br>
  ⇾ Do not move the folder after running sys_info_setup.py file. If you do that, working directory error will accure. Then widget can crash. <br>
  ⇾ If you want to move the folder first run Delete_SetUp.py and then .move the folder where you want to move and re-run sys_info_setup.py to re-assign the new path. <br>
  ⇾ I used OpenHardware.dll file for this project. You can get this from https://openhardwaremonitor.org/ 

## Requirement 
  ≫ python3

## Contact 

Mail address : k.prasannagh@gmail.com

Follow me on instagram : https://www.instagram.com/prasanna_rdj_fan/
