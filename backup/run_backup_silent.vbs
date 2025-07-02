Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' Get the full path of the current script (run_backup_silent.vbs)
currentScript = WScript.ScriptFullName

' Get the folder where this script is located (BusinessApp\backup)
backupFolder = fso.GetParentFolderName(currentScript)

' Get the project root folder (one level above)
projectRoot = fso.GetParentFolderName(backupFolder)

' Build the path to python inside virtual environment
pythonPath = projectRoot & "\.venv\Scripts\python.exe"

' Build full paths to the scripts/batch file
writePathScript = backupFolder & "\write_backup_path.py"
backupScript = backupFolder & "\backup.py"
zipBatchFile = backupFolder & "\convert_to_zip.bat"

' Run the script that writes the backup path (silent)
WshShell.Run """" & pythonPath & """ """ & writePathScript & """", 0, True

' Run the backup Python script (silent)
WshShell.Run """" & pythonPath & """ """ & backupScript & """", 0, True

' Run the zip batch file (silent)
WshShell.Run """" & zipBatchFile & """", 0, False



' When creating your task:
'
'     In Action, choose:
'
'         Program/script: wscript.exe
'
'         Add arguments: "C:\path\to\run_backup_silent.vbs" (quotes required)
'
' This runs the script with no window popping up, fully in the background.
