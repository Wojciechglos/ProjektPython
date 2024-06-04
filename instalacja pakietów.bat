@echo off

rem Instalacja pakietu pip
echo Instalowanie pip...
python -m ensurepip
echo Instalacja pip zakończona.

rem Pobranie ścieżki do pliku requirements.txt
set REQUIREMENTS_FILE=ścieżka_do_pliku\requirements.txt

rem Sprawdzenie czy plik requirements.txt istnieje
if not exist %REQUIREMENTS_FILE% (
    echo Błąd: Plik requirements.txt nie istnieje.
    exit /b 1
)

rem Instalacja pakietów z requirements.txt
echo Instalowanie pakietów z pliku requirements.txt...
pip install -r %REQUIREMENTS_FILE%
echo Instalacja zakończona.

pause
