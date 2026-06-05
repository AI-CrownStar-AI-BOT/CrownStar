[Setup]
AppId={{CrownStar-Basic}}
AppName=CrownStar Basic
AppVersion=1.0.0
AppPublisher=CrownStar AI
DefaultDirName={pf}\CrownStar\Basic
DefaultGroupName=CrownStar
UninstallDisplayIcon={app}\crownstar.ico
OutputDir=..\..\..\installers
OutputBaseFilename=CrownStar_Basic_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
[Files]
Source: "dist\CrownStar_Basic.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\..\assets\branding\crownstar.ico"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\CrownStar Basic"; Filename: "{app}\CrownStar_Basic.exe"; IconFilename: "{app}\crownstar.ico"
Name: "{commondesktop}\CrownStar Basic"; Filename: "{app}\CrownStar_Basic.exe"; IconFilename: "{app}\crownstar.ico"
[Run]
Filename: "{app}\CrownStar_Basic.exe"; Description: "Launch CrownStar Basic"; Flags: postinstall nowait skipifsilent
