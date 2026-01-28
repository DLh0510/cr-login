[Setup]
AppName=云计算竞赛训练工作站(CR-Questing 模块)
AppVersion=1.0
DefaultDirName={autopf}\CR-Questing
DefaultGroupName=CR-Questing
OutputBaseFilename=CR-Questing-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CloudRaiser-Login.exe

[Files]
Source: "dist\CloudRaiser-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\云计算竞赛训练工作站"; Filename: "{app}\CloudRaiser-Login.exe"
Name: "{group}\卸载 云计算竞赛训练工作站"; Filename: "{uninstallexe}"
Name: "{commondesktop}\云计算竞赛训练工作站"; Filename: "{app}\CloudRaiser-Login.exe"

[Run]
Filename: "{app}\CloudRaiser-Login.exe"; Description: "启动 云计算竞赛训练工作站"; Flags: nowait postinstall skipifsilent
