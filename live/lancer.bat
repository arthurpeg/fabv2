@echo off
rem Usage : live\lancer.bat A   (ou B). Relance le bot s'il s'arrête.
cd /d %~dp0..
:boucle
uv run python -m live.bot --config live\config_%1.toml
echo [%date% %time%] bot %1 arrete, relance dans 30 s >> live\etat\relances_%1.log
timeout /t 30 /nobreak > nul
goto boucle
