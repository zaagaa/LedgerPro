Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get path of this VBS file
strCurrentPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strBatFile = strCurrentPath & "\update.bat"

' Run the batch file silently
objShell.Run Chr(34) & strBatFile & Chr(34), 0, False
