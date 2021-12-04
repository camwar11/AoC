$year=$args[0]
$day=$args[1]
Set-Location -Path "I:\Code\AoC\src\$year\day$day"
Measure-Command {python .\day$day.py}