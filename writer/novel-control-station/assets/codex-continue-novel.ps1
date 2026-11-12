# codex-continue-novel.ps1
# powershell -ExecutionPolicy Bypass -File .\codex-continue-novel.ps1
# Keep this file encoded as UTF-8 with BOM on Windows.

$utf8Bom = [System.Text.UTF8Encoding]::new($true)
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$followUp = @"
使用novel-control-station技能继续小说的疯狂创作。
必须直接写回项目文件,不要只在标准输出中返回正文。

硬性要求:
1. 继续当前章节链,按顺序创作下一章。
2. 每完成一章,都必须把正文保存到 chapters/ 下对应的下一章文件,并遵守项目当前命名规则。
3. 每完成一章,都必须同步创建或更新对应的 control-cards/ 章节控制卡。
4. 每完成一章,都必须同步更新:
   - 08-dynamic-state.md
   - logs/writing-log.md
   - 07-chapter-roadmap.md
   - 06-foreshadow-ledger.md
   - 05-main-plotlines.md
   - 04-relationship-map.md
   - 02-worldbuilding.md
   - 03-cast-bible.md
   按需更新,没有变化的文件可以不改。
5. 标准输出只保留简短进度说明,不要直接输出整章正文。
6. 如果无法写入上述项目文件,请直接回复 FileWriteBlocked。
7. 如果整本小说已经完成,而不是当前章节完成,请直接回复 AllNovelDone。
"@
$projectRoot = "__PROJECT_ROOT__"
$logFile = Join-Path $projectRoot "codex-continue.log"
$logEncodingChecked = $false

function Initialize-Utf8Runtime {
    try {
        & "$env:SystemRoot\System32\chcp.com" 65001 > $null
    } catch {
    }

    try {
        [Console]::InputEncoding = $utf8NoBom
        [Console]::OutputEncoding = $utf8NoBom
        $global:OutputEncoding = $utf8NoBom
    } catch {
    }
}

function Ensure-LogFile {
    if ($logEncodingChecked) {
        return
    }

    if (-not (Test-Path -LiteralPath $logFile)) {
        [System.IO.File]::WriteAllText($logFile, "", $utf8Bom)
        $script:logEncodingChecked = $true
        return
    }

    $bytes = [System.IO.File]::ReadAllBytes($logFile)
    $hasUtf8Bom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF

    if ($bytes.Length -eq 0) {
        [System.IO.File]::WriteAllText($logFile, "", $utf8Bom)
        $script:logEncodingChecked = $true
        return
    }

    if (-not $hasUtf8Bom) {
        $legacyLog = Join-Path $projectRoot ("codex-continue.legacy-{0}.log" -f (Get-Date -Format "yyyyMMdd-HHmmss"))
        Move-Item -LiteralPath $logFile -Destination $legacyLog -Force
        [System.IO.File]::WriteAllText($logFile, "", $utf8Bom)
        Write-Host "[encoding] Existing log was archived to $legacyLog"
    }

    $script:logEncodingChecked = $true
}

function Append-LogLine($text) {
    Ensure-LogFile
    [System.IO.File]::AppendAllText($logFile, "$text$([Environment]::NewLine)", $utf8NoBom)
}

function Log($msg) {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$time] $msg"
    Write-Host $line
    Append-LogLine $line
}

function Write-CommandOutput($lines) {
    foreach ($line in @($lines)) {
        if ($null -eq $line) {
            continue
        }

        $text = [string]$line
        Write-Host $text
        Append-LogLine $text
    }
}

function Test-StopSignal($lines, $signal) {
    foreach ($line in @($lines)) {
        if ([string]$line -match ('^\s*' + [regex]::Escape($signal) + '\s*$')) {
            return $true
        }
    }

    return $false
}

function Get-TrackedProjectSnapshot {
    $entries = New-Object System.Collections.Generic.List[string]

    $trackedFiles = @(
        '08-dynamic-state.md',
        'logs/writing-log.md',
        '07-chapter-roadmap.md',
        '06-foreshadow-ledger.md',
        '05-main-plotlines.md',
        '04-relationship-map.md',
        '02-worldbuilding.md',
        '03-cast-bible.md'
    )

    foreach ($relativePath in $trackedFiles) {
        $fullPath = Join-Path $projectRoot $relativePath
        if (-not (Test-Path -LiteralPath $fullPath)) {
            continue
        }

        $item = Get-Item -LiteralPath $fullPath
        $entries.Add(('{0}|{1}|{2}' -f $item.FullName, $item.LastWriteTimeUtc.Ticks, $item.Length))
    }

    foreach ($relativeDir in @('chapters', 'control-cards')) {
        $fullDir = Join-Path $projectRoot $relativeDir
        if (-not (Test-Path -LiteralPath $fullDir)) {
            continue
        }

        foreach ($item in (Get-ChildItem -LiteralPath $fullDir -File -Filter '*.md' | Sort-Object FullName)) {
            $entries.Add(('{0}|{1}|{2}' -f $item.FullName, $item.LastWriteTimeUtc.Ticks, $item.Length))
        }
    }

    return ($entries -join "`n")
}

Initialize-Utf8Runtime
Set-Location -LiteralPath $projectRoot
Log "开始恢复最后一次会话"

while ($true) {
    Set-Location -LiteralPath $projectRoot
    $beforeSnapshot = Get-TrackedProjectSnapshot
    $output = & codex exec resume --last $followUp --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox 2>&1
    $code = $LASTEXITCODE
    $afterSnapshot = Get-TrackedProjectSnapshot
    Write-CommandOutput $output

    if (Test-StopSignal $output "AllNovelDone") {
        Log "收到 AllNovelDone，整本小说已完成，停止脚本"
        break
    }

    if (Test-StopSignal $output "FileWriteBlocked") {
        Log "收到 FileWriteBlocked，当前会话未能写入项目文件，停止脚本"
        break
    }

    if ($code -eq 0) {
        if ($beforeSnapshot -eq $afterSnapshot) {
            Log "会话正常结束，但未检测到项目文件写入，停止脚本"
            break
        }

        Log "会话正常结束，并检测到项目文件更新"
        continue
    }

    Log "检测到异常退出，退出码: $code，准备自动继续"
    Start-Sleep -Seconds 2
}
