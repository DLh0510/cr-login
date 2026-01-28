[Setup]
AppName=云计算无服务器架构竞赛实训平台
AppVersion=1.0
DefaultDirName={autopf}\CloudServerless-Training
DefaultGroupName=CloudServerless
OutputBaseFilename=CloudServerless-Training-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CloudRaiser-Login.exe

[Files]
Source: "dist\CloudRaiser-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\云计算无服务器架构竞赛实训平台"; Filename: "{app}\CloudRaiser-Login.exe"
Name: "{group}\卸载 云计算无服务器架构竞赛实训平台"; Filename: "{uninstallexe}"
Name: "{commondesktop}\云计算无服务器架构竞赛实训平台"; Filename: "{app}\CloudRaiser-Login.exe"

[Run]
Filename: "{app}\CloudRaiser-Login.exe"; Description: "启动 云计算无服务器架构竞赛实训平台"; Flags: nowait postinstall skipifsilent
