$l = [IO.File]::ReadAllLines('f:\Development\tools\README.md')
$m = 0; $c = 0
foreach ($x in $l) {
    if ($x.Trim() -eq '') { $c++; if ($c -gt $m) { $m = $c } } else { $c = 0 }
}
Write-Output ('max-consecutive-blank=' + $m + ' total-lines=' + $l.Count)
