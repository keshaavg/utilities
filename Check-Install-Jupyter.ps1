# Filename: Check-Install-Jupyter.ps1
param(
    [switch]$Apply,
    [switch]$InstallMiniconda
)

Write-Host "`n=== Jupyter Notebook Environment Check ===`n"

# Helper Functions
function Check-Command($cmd) {
    try {
        & $cmd --version > $null 2>&1
        return $true
    } catch {
        return $false
    }
}

function Install-Python {
    $url = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    $installer = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest $url -OutFile $installer
    Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $installer -Force
}

function Install-Miniconda {
    $url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
    $installer = "$env:TEMP\miniconda-installer.exe"
    Invoke-WebRequest $url -OutFile $installer
    Start-Process -FilePath $installer -ArgumentList "/InstallationType=AllUsers /AddToPath=1 /S" -Wait
    Remove-Item $installer -Force
}

function Install-Jupyter {
    python -m pip install --upgrade pip
    python -m pip install notebook
}

# Check for prerequisites
$pythonInstalled = Check-Command "python"
$pipInstalled = Check-Command "pip"
$jupyterInstalled = Check-Command "jupyter"

$pythonOK = $false
if ($pythonInstalled) {
    $ver = & python --version
    if ($ver -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        $pythonOK = ($major -ge 3 -and $minor -ge 8)
    }
}

$missing = @()
if (-not $pythonInstalled) { $missing += "Python" }
elseif (-not $pythonOK) { $missing += "Python >= 3.8" }
if (-not $pipInstalled) { $missing += "pip" }
if (-not $jupyterInstalled) { $missing += "Jupyter Notebook" }

if ($missing.Count -eq 0) {
    Write-Host "All prerequisites for Jupyter Notebook are already satisfied."
} else {
    Write-Host "Missing or outdated components:"
    $missing | ForEach-Object { Write-Host " - $_" }

    if (-not $Apply) {
        Write-Host "`nDry Run: Use -Apply to install the missing components."
        Write-Host "Optionally add -InstallMiniconda to install Miniconda instead of Python from python.org"
        exit 0
    }

    Write-Host "`nStarting installation..." -ForegroundColor Cyan

    if ($InstallMiniconda) {
        Write-Host "Installing Miniconda..."
        Install-Miniconda
    } else {
        Write-Host "Installing Python from python.org..."
        Install-Python
    }

    if (-not $pipInstalled) {
        python -m ensurepip --default-pip
    }

    Write-Host "Installing Jupyter Notebook..."
    Install-Jupyter

    Write-Host "`nSetup complete. You can now launch Jupyter using `jupyter notebook`."
}
