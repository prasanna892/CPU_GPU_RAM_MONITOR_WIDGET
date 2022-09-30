import win32com.client
import os
import ctypes
import sys
import winreg as reg

# function to check if user run script in administrator mode
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# function to delete scheduled tempInfo task
def deleteTempInfoScheduledTask():
    task_id = "tempInfo"

    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    rootFolder = scheduler.GetFolder("\\")

    task = rootFolder.GetTask(task_id)
    rootFolder.DeleteTask(task.Name, 0)

# function to delete created tempInfo task shortcut
def deleteShortCut():
    path = os.path.join(os.getcwd(), 'assets\TempInfo.lnk')
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)

# function to delete registered register key
def deleteRegistryKey():
    try:
        Key_Name1 = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, Key_Name1, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(key, 'tempInfo')
    except:
        pass

    try:
        Key_Name2 = r"Software\Microsoft\Windows\CurrentVersion\App Paths"
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, Key_Name2, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteKey(key, 'tempInfo.py')
    except:
        pass


def main():
    if is_admin(): # checking if script is running in administrator mode
        deleteTempInfoScheduledTask()
        deleteShortCut()
        deleteRegistryKey()

    else: # else ask user to run this script in administrator mode
        # to re-run this script with administrator mode if user allow's
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "Delete_SetUp.py")

if __name__ == '__main__':
    main()
    input("Deletion complete...\nPress any key to exit")