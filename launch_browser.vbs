Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get full path to script directory
projectPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Build full command
cmd = "cmd /c cd /d """ & projectPath & """ && call .venv\Scripts\activate && python manage.py runserver 0.0.0.0:8000"

' Run Django server silently
shell.Run cmd, 0, False

' Wait 5 seconds
WScript.Sleep 5000

' Open browser
shell.Run "http://127.0.0.1:8000"
