Clear-Host
Write-Host "generating dataset ......"

$Path = ".\lfw\"
$DatasetPath = ".\dataset\"
$Number = 0
$Extention = ".jpg"
Foreach ($file in Get-Childitem $Path -recurse -force)
{   
    If ($file.extension -eq $Extention)
    {
        "{0,10} {1,-24} {2,-2}" -f $file.length, $file.LastAccessTime, $file.fullname
        Copy-Item $file.fullname "$DatasetPath$Number$Extention"
        $Number++
    }
}

Write-Host "total generated " + $Number + " images !"