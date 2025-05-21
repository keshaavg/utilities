# Jupyter Notebook Setup Script

This script (`Check-Install-Jupyter.ps1`) installs everything required to run Jupyter Notebook on a Windows PC. It supports:

- Dry run mode to check for prerequisites
- Apply mode to install missing components
- Optional Miniconda installation instead of python.org build

---

## How to Use

> Make sure PowerShell is running as Administrator and you have internet access.

### 1. Save the script

Save your PowerShell script as:

```
Check-Install-Jupyter.ps1
```

---

### 2. Run the script

To check or install the required tools, use one of the following commands:

#### ✅ Check only (Dry Run)

This checks if Python, pip, and Jupyter Notebook are already installed.

```
.\Check-Install-Jupyter.ps1
```

#### ⚙️ Install everything (Apply mode with Python from python.org)

This installs Python (if missing), pip, and Jupyter Notebook.

```
.\Check-Install-Jupyter.ps1 -Apply
```

#### 🐍 Install using Miniconda (instead of python.org Python)

This installs Miniconda, pip, and Jupyter Notebook.

```
.\Check-Install-Jupyter.ps1 -Apply -InstallMiniconda
```

---

## After Installation

Once setup is complete, launch Jupyter Notebook with:

```
jupyter notebook
```

This opens Jupyter in your default browser.

---

## Notes

- Python will be installed system-wide and added to your PATH
- Jupyter will be installed using pip
- Miniconda is optional and can be used instead of python.org Python
- Use `-Apply` to perform actions, otherwise the script runs in dry run mode
