:: This method is not recommended, and we recommend you use the `start.sh` file with WSL instead.
@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the directory of the current script
SET "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%" || exit /b

:: Add conditional Playwright browser installation
IF /I "%WEB_LOADER_ENGINE%" == "playwright" (
    IF "%PLAYWRIGHT_WS_URL%" == "" (
        echo Installing Playwright browsers...
        playwright install chromium
        playwright install-deps chromium
    )

    python -c "import nltk; nltk.download('punkt_tab')"
)

SET "KEY_FILE=.answerai_secret_key"
IF NOT "%ANSWERAI_SECRET_KEY_FILE%" == "" (
    SET "KEY_FILE=%ANSWERAI_SECRET_KEY_FILE%"
)

IF "%PORT%"=="" SET PORT=8080
IF "%HOST%"=="" SET HOST=0.0.0.0
SET "ANSWERAI_SECRET_KEY=%ANSWERAI_SECRET_KEY%"
SET "ANSWERAI_JWT_SECRET_KEY=%ANSWERAI_JWT_SECRET_KEY%"

:: Check if ANSWERAI_SECRET_KEY and ANSWERAI_JWT_SECRET_KEY are not set
IF "%ANSWERAI_SECRET_KEY% %ANSWERAI_JWT_SECRET_KEY%" == " " (
    echo Loading ANSWERAI_SECRET_KEY from file, not provided as an environment variable.

    IF NOT EXIST "%KEY_FILE%" (
        echo Generating ANSWERAI_SECRET_KEY
        :: Generate a random value to use as a ANSWERAI_SECRET_KEY in case the user didn't provide one
        SET /p ANSWERAI_SECRET_KEY=<nul
        FOR /L %%i IN (1,1,12) DO SET /p ANSWERAI_SECRET_KEY=<!random!>>%KEY_FILE%
        echo ANSWERAI_SECRET_KEY generated
    )

    echo Loading ANSWERAI_SECRET_KEY from %KEY_FILE%
    SET /p ANSWERAI_SECRET_KEY=<%KEY_FILE%
)

:: Execute uvicorn
SET "ANSWERAI_SECRET_KEY=%ANSWERAI_SECRET_KEY%"
IF "%UVICORN_WORKERS%"=="" SET UVICORN_WORKERS=1
uvicorn answer_ai.main:app --host "%HOST%" --port "%PORT%" --forwarded-allow-ips '*' --workers %UVICORN_WORKERS% --ws auto
:: For ssl user uvicorn answer_ai.main:app --host "%HOST%" --port "%PORT%" --forwarded-allow-ips '*' --ssl-keyfile "key.pem" --ssl-certfile "cert.pem" --ws auto
