#ifndef PackageDir
  #error Supply /DPackageDir with the assembled safe release directory
#endif
#ifndef OutputDir
  #define OutputDir "."
#endif

[Setup]
AppId={{C7E3DA19-B196-4273-9F58-16B31D6A764C}
AppName=CWRC
AppVersion=3.05-rc5
AppPublisher=CWRC contributors
AppComments=Unofficial Chinese localization and modified client. Original engine by Bohemia Interactive.
DefaultDirName={localappdata}\Programs\CWRC
DisableDirPage=yes
DefaultGroupName=CWRC
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#OutputDir}
OutputBaseFilename=CWRC-3.05-rc5-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=no
RestartApplications=no
UninstallDisplayName=CWRC Chinese localization
UninstallDisplayIcon={app}\helper\cwrc-helper.exe
LicenseFile={#PackageDir}\notices\COMPONENTS.txt
SetupLogging=yes

[Files]
Source: "{#PackageDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[INI]
Filename: "{app}\game.ini"; Section: "CWRC"; Key: "Game"; String: "{code:GameDirectory}"; Flags: uninsdeleteentry uninsdeletesectionifempty

[Icons]
Name: "{group}\CWRC"; Filename: "{code:GameDirectory}\crwc-client\PoseidonGame.exe"; Parameters: "--add-mod @zhcn-prototype --voice English"; WorkingDir: "{code:GameDirectory}"; Comment: "Unofficial Chinese localization; requires your original Remastered 3.05 data"
Name: "{group}\Uninstall CWRC"; Filename: "{uninstallexe}"

[Code]
var
  GamePage: TInputDirWizardPage;
  OperationPage: TOutputProgressWizardPage;
  LastOutput: String;
  NewlyInstalled, Finished: Boolean;

function GameDirectory(Param: String): String;
begin
  Result := RemoveBackslashUnlessRoot(GamePage.Values[0]);
end;

procedure HelperOutput(const S: String; const Error, FirstLine: Boolean);
var
  N: Integer;
  Tail: String;
begin
  Log(S);
  if LastOutput <> '' then LastOutput := LastOutput + #13#10;
  LastOutput := LastOutput + S;
  if Length(LastOutput) > 4000 then Delete(LastOutput, 1, Length(LastOutput) - 4000);
  if Copy(S, 1, 5) = 'STEP ' then begin
    Tail := Copy(S, 6, Length(S));
    N := Pos(' ', Tail);
    if N > 0 then begin
      if not IsUninstaller then begin
        OperationPage.SetProgress(StrToIntDef(Copy(Tail, 1, N-1), 0), 100);
        OperationPage.SetText(Copy(Tail, N+1, Length(Tail)), GameDirectory(''));
      end else
        UninstallProgressForm.StatusLabel.Caption := Copy(Tail, N+1, Length(Tail));
    end;
  end;
end;

function RunHelper(Base, Operation, Game: String): Boolean;
var
  Code: Integer;
begin
  LastOutput := '';
  Result := ExecAndLogOutput(Base + '\helper\cwrc-helper.exe',
    Operation + ' "' + Game + '" --package "' + Base + '" --wrapper-dir "' + ExpandConstant('{app}') + '"', Base,
    SW_HIDE, ewWaitUntilTerminated, Code, @HelperOutput);
  Result := Result and (Code = 0);
end;

procedure InitializeWizard;
var
  Game: String;
begin
  GamePage := CreateInputDirPage(wpSelectDir, 'Select your existing game',
    'Windows x64 Remastered 3.05 is required',
    'Select the Remastered folder containing the ORIGINAL PoseidonGame.exe. Required localization sources will be verified. Profiles, saves and unrelated mods are preserved.', False, '');
  GamePage.Add('Existing Remastered folder:');
  Game := ExpandConstant('{param:GAME|}') ;
  if Game = '' then Game := GetPreviousData('Game', '');
  if Game = '' then Game := 'C:\GOG Games\Cold War Assault Remastered\Remastered';
  GamePage.Values[0] := Game;
  OperationPage := CreateOutputProgressPage('Preparing CWRC', 'Verifying originals and installing locally generated overlays');
end;

procedure RegisterPreviousData(PreviousDataKey: Integer);
begin
  SetPreviousData(PreviousDataKey, 'Game', GameDirectory(''));
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Previous: String;
begin
  Result := True;
  if CurPageID = GamePage.ID then begin
    Previous := GetIniString('CWRC', 'Game', '', ExpandConstant('{app}\game.ini'));
    if (Previous <> '') and (CompareText(Previous, GameDirectory('')) <> 0) then begin
      MsgBox('Uninstall the recognized CWRC installation before selecting a different game folder.', mbError, MB_OK);
      Result := False;
    end else if not FileExists(GameDirectory('') + '\PoseidonGame.exe') then begin
      MsgBox('Select the Remastered folder containing the original PoseidonGame.exe.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  Installed, Major, Minor, Build: Cardinal;
begin
  Result := '';
  if not RegQueryDWordValue(HKLM64, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed', Installed) or
     (Installed <> 1) or
     not RegQueryDWordValue(HKLM64, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Major', Major) or
     not RegQueryDWordValue(HKLM64, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Minor', Minor) or
     not RegQueryDWordValue(HKLM64, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Bld', Build) or
     (Major < 14) or ((Major = 14) and ((Minor < 44) or ((Minor = 44) and (Build < 35207)))) then begin
    Result := 'Install the Microsoft Visual C++ x64 runtime (14.44.35207 or newer), then retry: https://aka.ms/vc14/vc_redist.x64.exe';
    exit;
  end;
  ExtractTemporaryFiles('{app}\*');
  NewlyInstalled := not FileExists(GameDirectory('') + '\.crwc-install\receipt.json');
  OperationPage.Show;
  try
    if not RunHelper(ExpandConstant('{tmp}') + '\{app}', 'install', GameDirectory('')) then
      Result := 'CWRC preparation failed. No automatic cleanup will remove original backups.' + #13#10 + LastOutput;
  finally
    OperationPage.Hide;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone then Finished := True;
end;

procedure DeinitializeSetup;
begin
  if NewlyInstalled and not Finished then begin
    if FileExists(ExpandConstant('{tmp}') + '\{app}\helper\cwrc-helper.exe') then
      if not RunHelper(ExpandConstant('{tmp}') + '\{app}', 'uninstall', GameDirectory('')) then
        MsgBox('Restoration is incomplete. Original backups are retained. Run this installer again to recover, or inspect the recorded conflict before removing anything.', mbError, MB_OK);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  Game: String;
  Remaining: AnsiString;
begin
  if CurUninstallStep = usUninstall then begin
    Game := GetIniString('CWRC', 'Game', '', ExpandConstant('{app}\game.ini'));
    if (Game = '') or not DirExists(Game) then begin
      MsgBox('The recorded game folder is unavailable. CWRC components and recovery metadata will not be removed.', mbError, MB_OK);
      Abort;
    end;
    if not RunHelper(ExpandConstant('{app}'), 'uninstall', Game) then begin
      MsgBox('Restoration is incomplete. User-modified files, original backups and CWRC recovery components are preserved. Resolve the reported conflict and retry.' + #13#10 + LastOutput, mbError, MB_OK);
      Abort;
    end;
  end;
  if CurUninstallStep = usPostUninstall then begin
    if LoadStringFromFile(ExpandConstant('{app}\game.ini'), Remaining) then
      if Trim(Remaining) = '' then DeleteFile(ExpandConstant('{app}\game.ini'));
    RemoveDir(ExpandConstant('{app}')); // Empty only: retain any unrelated/user files.
  end;
end;
