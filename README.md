# CPU_GPU_RAM_MONITOR_APPLICATION

## Set-Up
  1) Open system_info folder
  2) Just DoubleClick sys_info_setup.py
  
  That's it, now wait for few seconds until monitor widget launches
  
## Delete Set-Up 
  1) Open system_info folder
  2) Run Delete_SetUp.py
  
## Future's 
  1) It automatically pop up when you start up or restart of your system.
  2) It show info about CPU, GPU, RAM and DISK usage, temperature, consuming wattage.
  3) As the TempINFO.exe file generate result.json file you can also use it for your project.
  4) TempInfo.exe also provide write.txt file for more information of your system deatials and performance.
  5) It automaticaly store the last position and size in property.json file before close, So it can able to open in last position when close.
  6) Nice look animation😁
  
## Working Algorithm 
  1) When you Double-Click the sys_info_setup.py, it call requirment_installer.py to install required modules.
  2) It check for run asAdmin if not ask permission.
  3) If user give permission, it schedule TempINFO.exe file (system_info/assets/TempInfo) to task scheduler for bipass administrator mode.
  4) Create scheduled task shortcut in assets folder with name of 'TempInfo.lnk'.
  5) Exclude working directory folder from windows virus & threat production.
  6) Add sys_info.pyw to registry for start automaticaly when system startup
  7) Call sys_info.pyw -> load() to run
  8) sys_info.pyw run TempInfo.lnk file -> TempINFO.exe generates result.json file.
  9) sys_info.pyw read's result.json file and get information then display.
  10) Update information at every 1sec.
  11) On system ShurtDown sys_info.pyw terminate TempINFO.exe and update current position in property.json then exit
  12) ends
  
## Notes
  ※ Some times the widget did not pop up at first setup run beacuse of any antivirus app you installed in your system. <br>
  ※ Do not move the folder after running sys_info_setup.py file. If you do that, working directory error will accure. Then widget can crash. <br>
  ※ If you want to move the folder first run Delete_SetUp.py and then .move the folder where you want to move and re-run  » sys_info_setup.py to re-assign the new path. <br>
  ※ I used OpenHardware.dll file for this project. You can get this from https://openhardwaremonitor.org/ 

## Requirement 
  ※ python3

## Contact 

Mail address : k.prasannagh@gmail.com

Follow me on instagram : https://www.instagram.com/prasanna_rdj_fan/
