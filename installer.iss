[Setup]
AppName=提示词工程课程实训平台
AppVersion=1.0
DefaultDirName={autopf}\PromptEngineering-Platform
DefaultGroupName=提示词工程实训平台
OutputBaseFilename=PromptEngineering-Platform-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\PromptEngineering-Login.exe

[Files]
Source: "dist\PromptEngineering-Login.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\提示词工程课程实训平台"; Filename: "{app}\PromptEngineering-Login.exe"
Name: "{group}\卸载 提示词工程课程实训平台"; Filename: "{uninstallexe}"
Name: "{commondesktop}\提示词工程课程实训平台"; Filename: "{app}\PromptEngineering-Login.exe"

[Run]
Filename: "{app}\PromptEngineering-Login.exe"; Description: "启动 提示词工程课程实训平台"; Flags: nowait postinstall skipifsilent
