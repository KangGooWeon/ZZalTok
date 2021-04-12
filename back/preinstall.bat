@echo off
@chcp 65001 1> NUL 2> NUL
setlocal enableextensions enabledelayedexpansion
pushd %~dp0

:BatchGotAdmin
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
title PREINSTALL REQUIREMENTS

set root=C:\ProgramData\Miniconda3
call %root%\Scripts\activate.bat %root%

echo 해당 파일은 requirements만을 추가 설치하기 위해 만들어졌습니다.
call conda activate AI

echo .
echo 라이브러리 및 모듈 설치 시작
call pip install -r requirements.txt

echo .
echo 설치가 완료되었습니다. run.bat 파일로 서버를 실행하시면 됩니다.
pause
