[Setup]
AppId={{CrownStar-Pro}}
AppName=CrownStar Pro
AppVersion=1.0.0
AppPublisher=CrownStar AI
DefaultDirName={pf}\CrownStar\Pro
DefaultGroupName=CrownStar
UninstallDisplayIcon={app}\crownstar.ico
OutputDir=..\..\..\installers
OutputBaseFilename=CrownStar_Pro_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
[Files]
Source: "dist\CrownStar_Pro.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\..\assets\branding\crownstar.ico"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\CrownStar Pro"; Filename: "{app}\CrownStar_Pro.exe"; IconFilename: "{app}\crownstar.ico"
Name: "{commondesktop}\CrownStar Pro"; Filename: "{app}\CrownStar_Pro.exe"; IconFilename: "{app}\crownstar.ico"
[Run]
Filename: "{app}\CrownStar_Pro.exe"; Description: "Launch CrownStar Pro"; Flags: postinstall nowait skipifsilent
