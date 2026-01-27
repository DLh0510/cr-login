[Setup]
AppName=CloudRaiser Admin 登录
AppVersion=1.0
DefaultDirName={autopf}\CloudRaiser-Login
DefaultGroupName=CloudRaiser
OutputBaseFilename=CloudRaiser-Login-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CloudRaiser-Login.exe

[Files]
Source: "dist\CloudRaiser-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CloudRaiser Admin 登录"; Filename: "{app}\CloudRaiser-Login.exe"
Name: "{group}\卸载 CloudRaiser Admin 登录"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CloudRaiser Admin 登录"; Filename: "{app}\CloudRaiser-Login.exe"

[Run]
Filename: "{app}\CloudRaiser-Login.exe"; Description: "启动 CloudRaiser Admin 登录"; Flags: nowait postinstall skipifsilent
