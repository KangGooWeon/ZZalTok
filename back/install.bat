@echo off
pushd %~dp0

echo ��ġ�� CUDA ��� Ȯ��
nvcc --version | find "10.2"
if errorlevel 1 goto :exit
goto :BatchGotAdmin
:exit
echo �ش� �ν��緯�� "CUDA 10.2" ��ġ�� �ʿ��մϴ�
echo �ϴ� ��ũ�� ���� ��ġ�� �ϰ�, �ν��緯�� ������Ͻñ� �ٶ��ϴ�
echo https://developer.nvidia.com/cuda-10.2-download-archive
timeout /t 30 >nul
exit

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
title INSTALL REQUIREMENTS

set root=C:\ProgramData\Miniconda3
call %root%\Scripts\activate.bat %root%

REM echo .
REM echo ���� ��ġ�� ���̺귯�� �� ��� �ʱ�ȭ
REM call conda clean -a -y
REM call conda install --revision 0 -y

REM echo .
REM echo ���̽� 3.7�� �缳ġ
REM call conda install python=3.7 -y

echo .
echo ����ȯ�� "AI"�� �����ϰ�, ���̽� 3.8�� ��ġ
call conda create -n AI python=3.8 -y
call conda activate AI

REM echo .
REM echo ���̽��� 3.7�� ��ġ�Ǿ� ���� �ʴٸ� �����ڿ��� �̽��� �޾��ּ���
REM call conda list python | find "python"

echo .
echo ���̺귯�� �� ��� ��ġ ����
call conda install -c conda-forge dlib -y
call pip install -r requirements.txt

echo .
echo pytorch ��ġ ����
REM call conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
REM call conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch -y
call conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch -y --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

echo .
echo ��ġ�� �Ϸ�Ǿ����ϴ�. run.bat ���Ϸ� ������ �����Ͻø� �˴ϴ�.
pause
