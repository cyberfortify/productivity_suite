# run_cli.ps1
if (-not (Test-Path env:VIRTUAL_ENV)) {
  Write-Host "Activate your venv first: .\\venv\\Scripts\\Activate"
  exit 1
}
python -m productivity.cli
