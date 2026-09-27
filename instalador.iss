[Setup]
AppName=EasyMSIX
AppVersion=1.0
DefaultDirName={autopf}\EasyMSIX
DefaultGroupName=EasyMSIX
OutputBaseFilename=EasyMSIX_Setup
ChangesAssociations=yes
PrivilegesRequired=admin

[Files]
Source: "dist\EasyMSIX\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\EasyMSIX"; Filename: "{app}\EasyMSIX.exe"

[Registry]
; --- 1. Registo do ProgID para EasyMSIX ---
Root: HKLM; Subkey: "Software\Classes\EasyMSIX.Package"; ValueType: string; ValueName: ""; ValueData: "Pacote de Aplicativo Windows (EasyMSIX)"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Classes\EasyMSIX.Package\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\EasyMSIX.exe,0"
Root: HKLM; Subkey: "Software\Classes\EasyMSIX.Package\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\EasyMSIX.exe"" ""%1"""

; --- 2. Associar as extensões (.appx, .msix, .appxbundle, .msixbundle) ---
Root: HKLM; Subkey: "Software\Classes\.appx"; ValueType: string; ValueName: ""; ValueData: "EasyMSIX.Package"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.msix"; ValueType: string; ValueName: ""; ValueData: "EasyMSIX.Package"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.appxbundle"; ValueType: string; ValueName: ""; ValueData: "EasyMSIX.Package"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.msixbundle"; ValueType: string; ValueName: ""; ValueData: "EasyMSIX.Package"; Flags: uninsdeletevalue

; --- 3. Lista de programas recomendados ("Abrir Com") ---
Root: HKLM; Subkey: "Software\Classes\Applications\EasyMSIX.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\EasyMSIX.exe"" ""%1"""
Root: HKLM; Subkey: "Software\Classes\.appx\OpenWithProgids"; ValueType: string; ValueName: "EasyMSIX.Package"; ValueData: ""; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.msix\OpenWithProgids"; ValueType: string; ValueName: "EasyMSIX.Package"; ValueData: ""; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.appxbundle\OpenWithProgids"; ValueType: string; ValueName: "EasyMSIX.Package"; ValueData: ""; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\.msixbundle\OpenWithProgids"; ValueType: string; ValueName: "EasyMSIX.Package"; ValueData: ""; Flags: uninsdeletevalue

[Run]
Filename: "{app}\EasyMSIX.exe"; Parameters: "--register"; Flags: runhidden