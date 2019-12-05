$day=$args[0]
Set-Location -Path "D:\Code\AoC2019\src\$day"
Measure-Command {python .\$day.py}