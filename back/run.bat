@echo off
@chcp 65001 1> NUL 2> NUL
setlocal enableextensions enabledelayedexpansion
pushd %~dp0

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

title JJAL Python SERVER

set root=C:\ProgramData\Miniconda3
call %root%\Scripts\activate.bat %root%
call conda activate AI
call uvicorn main:app --workers=4 --host=0.0.0.0 --port=8000 --no-access-log --http=httptools