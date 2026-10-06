Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
currentFolder = objFSO.GetParentFolderName(WScript.ScriptFullName)



' Run the batch file
objShell.Run chr(34) & currentFolder & "\startup.bat" & chr(34), 0, False
