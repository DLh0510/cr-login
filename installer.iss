[Setup]
AppName=云计算技能大赛训练平台
AppVersion=1.0
DefaultDirName={autopf}\CloudSkills-Training
DefaultGroupName=CloudSkills
OutputBaseFilename=CloudSkills-Training-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CloudRaiser-Login.exe

[Files]
Source: "dist\CloudRaiser-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\云计算技能大赛训练平台"; Filename: "{app}\CloudRaiser-Login.exe"
Name: "{group}\卸载 云计算技能大赛训练平台"; Filename: "{uninstallexe}"
Name: "{commondesktop}\云计算技能大赛训练平台"; Filename: "{app}\CloudRaiser-Login.exe"

[Run]
Filename: "{app}\CloudRaiser-Login.exe"; Description: "启动 云计算技能大赛训练平台"; Flags: nowait postinstall skipifsilent
