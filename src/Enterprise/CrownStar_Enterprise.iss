[Setup]
AppId={{CrownStar-Enterprise}}
AppName=CrownStar Enterprise
AppVersion=1.0.0
AppPublisher=CrownStar AI
DefaultDirName={pf}\CrownStar\Enterprise
DefaultGroupName=CrownStar
UninstallDisplayIcon={app}\crownstar.ico
OutputDir=..\..\..\installers
OutputBaseFilename=CrownStar_Enterprise_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
[Files]
Source: "dist\CrownStar_Enterprise.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\..\assets\branding\crownstar.ico"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\CrownStar Enterprise"; Filename: "{app}\CrownStar_Enterprise.exe"; IconFilename: "{app}\crownstar.ico"
Name: "{commondesktop}\CrownStar Enterprise"; Filename: "{app}\CrownStar_Enterprise.exe"; IconFilename: "{app}\crownstar.ico"
[Run]
Filename: "{app}\CrownStar_Enterprise.exe"; Description: "Launch CrownStar Enterprise"; Flags: postinstall nowait skipifsilent
