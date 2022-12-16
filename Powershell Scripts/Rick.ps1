#Check that Audio Service is running
$ServiceName = 'audiosrv'
$arrService = Get-Service -Name $ServiceName

while ($arrService.Status -ne 'Running')
{

    Start-Service $ServiceName
    write-host $arrService.status
    write-host 'Service starting'
    Start-Sleep -seconds 5
    $arrService.Refresh()
    if ($arrService.Status -eq 'Running')
    {
        Write-Host 'Service is now Running'
    }

}

#Open Rick Astley in Chrome
[system.diagnostics.Process]::Start("chrome","https://youtu.be/dQw4w9WgXcQ")

#Open Rick Astley saved on Server
#C:\Users\Administrator\Videos\Rick.mp4