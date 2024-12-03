# run_tests.ps1

Write-Output "running tests"

# Start the HTTP server in the background and save its PID
$serverProcess = Start-Process -FilePath 'python' -ArgumentList '-m http.server 8000' -PassThru
$serverProcess.Id | Out-File -FilePath server.pid

# Wait for the server to initialize
Start-Sleep -Seconds 2

# Open the test page in the default browser
Start-Process http://localhost:7777/frontend/src/tests/index.html

# Wait for the tests to be accessible
Start-Sleep -Seconds 2

# Kill the HTTP server process using the saved PID
$processId = Get-Content server.pid
Stop-Process -Id $processId
Remove-Item server.pid

Write-Output "tests complete"
