[Setup]
AppId={{CrownStar-Free}}
AppName=CrownStar Free
AppVersion=1.0.0
AppPublisher=CrownStar AI
DefaultDirName={pf}\CrownStar\Free
DefaultGroupName=CrownStar
UninstallDisplayIcon={app}\crownstar.ico
OutputDir=..\..\..\installers
OutputBaseFilename=CrownStar_Free_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
[Files]
Source: "dist\CrownStar_Free.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\..\assets\branding\crownstar.ico"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\CrownStar Free"; Filename: "{app}\CrownStar_Free.exe"; IconFilename: "{app}\crownstar.ico"
Name: "{commondesktop}\CrownStar Free"; Filename: "{app}\CrownStar_Free.exe"; IconFilename: "{app}\crownstar.ico"
[Run]
Filename: "{app}\CrownStar_Free.exe"; Description: "Launch CrownStar Free"; Flags: postinstall nowait skipifsilent
