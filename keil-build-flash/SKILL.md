---
name: keil-build-flash
description: Compile (Build) and Flash (Download) Keil MDK projects on Windows using UV4.exe
---

# Keil MDK Compile and Flash Skill

This skill provides precise instructions on how to compile (Build) and flash (Download) Keil MDK-ARM projects under Windows environments.

## Prerequisite Configurations

1. **Project File Path**: Find the `.uvprojx` file inside the workspace (usually under `MDK-ARM` folder).
2. **Log Files**:
   - Build log: `build_keil.log`
   - Flash log: `burn.log`

## 0. Configure Keil UV4 Path

Never assume a fixed Keil installation path. Use a user-level environment variable so the path survives terminal sessions and computer migrations.

Ask the user in the conversation for the Keil installation directory when `KEIL_UV4_PATH` is missing or invalid. Do not use `Read-Host` in an automated run. Then set `$searchRoot` to the directory supplied by the user and run:

```powershell
$uv4Path = [Environment]::GetEnvironmentVariable('KEIL_UV4_PATH', 'User')

if (-not $uv4Path -or -not (Test-Path -LiteralPath $uv4Path)) {
    if (-not (Test-Path -LiteralPath $searchRoot -PathType Container)) {
        throw "Keil installation directory not found: $searchRoot"
    }

    $uv4Candidates = @(Get-ChildItem -LiteralPath $searchRoot -Filter 'UV4.exe' -File -Recurse -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName)

    if ($uv4Candidates.Count -eq 0) {
        throw "UV4.exe not found under: $searchRoot"
    }

    if ($uv4Candidates.Count -gt 1) {
        throw "Multiple UV4.exe files found. Ask the user to select one: $($uv4Candidates -join '; ')"
    }

    $uv4Path = $uv4Candidates[0]

    [Environment]::SetEnvironmentVariable('KEIL_UV4_PATH', $uv4Path, 'User')
    $env:KEIL_UV4_PATH = $uv4Path
}

Write-Host "Using Keil: $uv4Path"
```

The user only needs to provide an installation directory once. On later runs, read `KEIL_UV4_PATH` and verify that the resolved file still exists. If Keil is moved or upgraded, ask for the new directory and update the variable.

---

## 1. How to Compile (Build)

To compile the Keil project, run the build command **synchronously** in PowerShell using `Start-Process` with the `-Wait` parameter to block until compilation is complete. Do not run it asynchronously.

### Compilation Command

```powershell
$projectPath = '<Absolute-Path-To-uvprojx>'
$buildLogPath = '<Absolute-Path-To-build_keil.log>'
$buildProcess = Start-Process -FilePath $uv4Path `
    -ArgumentList @('-b', "`"$projectPath`"", '-o', "`"$buildLogPath`"") `
    -Wait -PassThru
if ($buildProcess.ExitCode -ne 0) {
    throw "Keil build process failed with exit code $($buildProcess.ExitCode)"
}
```

### Verification of Compile Output

After the command returns, read the `<build_keil.log>` file:
- Check for `"0 Error(s)"` at the end of the log to confirm success.
- If there are errors, report them to the user.

---

## 2. How to Flash (Download)

To download the compiled firmware onto the hardware target, run the flash command **synchronously**.

### Flash Command

```powershell
$projectPath = '<Absolute-Path-To-uvprojx>'
$flashLogPath = '<Absolute-Path-To-burn.log>'
$flashProcess = Start-Process -FilePath $uv4Path `
    -ArgumentList @('-f', "`"$projectPath`"", '-o', "`"$flashLogPath`"") `
    -Wait -PassThru
if ($flashProcess.ExitCode -ne 0) {
    throw "Keil flash process failed with exit code $($flashProcess.ExitCode)"
}
```

### Verification of Flash Output

After the command returns, read the `<burn.log>` file:
- Look for `Erase Done.Programming Done.Verify OK.` to confirm a successful download.
- Verify `Application running ...` is printed.
- If J-Link connection fails, report the connection error (e.g. `Flash Download failed`).

---

## 3. Best Practices & Safety

- **Process Cleanup**: Check for an existing `UV4.exe` process only when a previous operation appears hung. Do not unconditionally terminate every UV4 process. After confirming it is the stale process, stop that specific process and explain the impact to the user:
  ```powershell
  Stop-Process -Id <Hung-Process-Id> -Force
  ```
- **Absolute Paths**: Always use absolute paths for the project `.uvprojx` file and the output `.log` files to avoid working directory mismatches.
