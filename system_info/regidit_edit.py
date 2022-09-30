# Python code to add current script to the registry

# module to edit the windows registry
import winreg as reg	
import os

def AddToRegistry(file_path, key_name):
	# path of the python file with extension
	address = file_path
	
	# key we want to change is HKEY_CURRENT_USER
	# key value is Software\Microsoft\Windows\CurrentVersion\Run
	key = reg.HKEY_CURRENT_USER
	key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
	
	# open the key to make changes to
	open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
	
	# modify the opened key
	reg.SetValueEx(open, key_name, 0, reg.REG_SZ, address)

	# key we want to change is HKEY_CURRENT_USER
	# key value is Software\Microsoft\Windows\CurrentVersion\App Paths
	key = reg.HKEY_CURRENT_USER
	key_value = r"Software\Microsoft\Windows\CurrentVersion\App Paths"

	# open the key to make changes to
	open = reg.OpenKeyEx(key, key_value, 0, reg.KEY_ALL_ACCESS)
	new_key = reg.CreateKey(open, f"{key_name}.py")
	# modify the opened key
	reg.SetValueEx(new_key, "Path", 0, reg.REG_SZ, str(os.getcwd()))

	# now close the opened key
	reg.CloseKey(open)
	reg.CloseKey(new_key)