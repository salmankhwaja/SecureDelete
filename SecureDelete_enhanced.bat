@echo off
setlocal

:: Configurable Variables
set "sdelete_path=C:\Downloads\SDelete\sdelete.exe"  :: Path to SDelete executable  Download Secure Delete EXE from here . https://download.sysinternals.com/files/SDelete.zip
set "days_old=8"                                                         :: Number of days old files to delete
set "folder_paths=C:\ExamplePath\1;C:\Another\Folder\Path"  :: Multiple folder paths (separated by ;)
set "PathToOmit=C:\ExamplePath\1\omit\;C:\Another\Folder\Exclude" :: Paths to omit (separated by ;)

:: Set log file path
set "log_file=C:\deletion_log.txt"  :: Log file path to log deleted files

:: Add header to the log file with the current date and time
echo Deletion Log - %date% %time% >> "%log_file%"
echo ------------------------------------------ >> "%log_file%"

:: Iterate through each folder path
for %%F in (%folder_paths%) do (
    echo Processing folder: %%F
    if exist "%%F" (
        forfiles /p "%%F" /s /m *.* /d -%days_old% /c "cmd /c set \"skip=0\" && for %%O in (%PathToOmit%) do (echo @path | findstr /i /b \"%%O\" >nul && set \"skip=1\") && if %%skip%%==0 (echo Deleting @path... && echo @path >> \"%log_file%\" && \"%sdelete_path%\" -p 3 -s @path)"
    ) else (
        echo Folder not found: %%F >> "%log_file%"
    )
)

:: Notify the user
echo Files older than %days_old% days have been securely deleted and logged, excluding specified paths.
endlocal
