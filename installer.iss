[Setup]
AppName=云计算竞赛训练平台-故障排除项目实训模块
AppVersion=1.0
DefaultDirName={autopf}\CloudRaiser-Troubleshooting
DefaultGroupName=CloudRaiser
OutputBaseFilename=CloudRaiser-Troubleshooting-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CloudRaiser-Login.exe

[Files]
Source: "dist\CloudRaiser-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\云计算竞赛训练平台-故障排除"; Filename: "{app}\CloudRaiser-Login.exe"
Name: "{group}\卸载 云计算竞赛训练平台-故障排除"; Filename: "{uninstallexe}"
Name: "{commondesktop}\云计算竞赛训练平台-故障排除"; Filename: "{app}\CloudRaiser-Login.exe"

[Run]
Filename: "{app}\CloudRaiser-Login.exe"; Description: "启动 云计算竞赛训练平台-故障排除"; Flags: nowait postinstall skipifsilent
