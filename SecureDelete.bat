@echo off
setlocal

:: Configurable Variables
set "sdelete_path=C:\Downloads\SDelete\sdelete.exe"  :: Path to SDelete executable  Download Secure Delete EXE from here . https://download.sysinternals.com/files/SDelete.zip
set "days_old=8"                                                         :: Number of days old files to delete
set "folder_path=C:\ExamplePath\"       :: Folder from which files and subfolders will be deleted
set "log_file=C:\deletion_log.txt"  :: Log file path to log deleted files

:: Add header to the log file with current date and time
echo Deletion Log - %date% %time% >> "%log_file%"
echo ------------------------------------------ >> "%log_file%"

:: Traverse the folder, search for files older than 'days_old' days, and securely delete them using SDelete
forfiles /p "%folder_path%" /s /m *.* /d -%days_old% /c "cmd /c echo Deleting @path... && echo @path >> \"%log_file%\" && call \"%sdelete_path%\" -p 3 -s @path"

:: Notify the user that the deletion process has completed
echo Files older than %days_old% days have been securely deleted and logged.
endlocal
