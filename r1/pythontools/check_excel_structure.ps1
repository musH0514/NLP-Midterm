# PowerShell script to check Excel file structure

$inputFile = "F:\projects\nlp\NLP-Midterm\04_Diaspora_Articles_12195(1).xlsx"

Write-Host "Checking Excel file structure..."

try {
    # Create Excel object
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    # Open workbook
    Write-Host "Opening workbook..."
    $workbook = $excel.Workbooks.Open($inputFile)

    # Get first worksheet
    $worksheet = $workbook.Worksheets.Item(1)
    Write-Host "Worksheet opened"

    # Get total rows
    $lastRow = $worksheet.UsedRange.Rows.Count
    Write-Host "Total rows: $lastRow"

    # Get total columns
    $lastCol = $worksheet.UsedRange.Columns.Count
    Write-Host "Total columns: $lastCol"

    # List all column headers
    Write-Host "`nColumn headers:"
    for ($col = 1; $col -le $lastCol; $col++) {
        $cellValue = $worksheet.Cells.Item(1, $col).Value2
        Write-Host "Column $col`: $cellValue"
    }

    # Check first 5 rows of relevant columns
    Write-Host "`nChecking first 5 rows of key columns:"

    # Find relevant columns
    $authorCol = 0
    $researcherIdCol = 0
    $orcidCol = 0

    for ($col = 1; $col -le $lastCol; $col++) {
        $cellValue = $worksheet.Cells.Item(1, $col).Value2
        if ($cellValue -eq "Diaspora_Author_Names") { $authorCol = $col }
        if ($cellValue -eq "Researcher Ids") { $researcherIdCol = $col }
        if ($cellValue -eq "ORCIDs") { $orcidCol = $col }
    }

    Write-Host "Diaspora_Author_Names column: $authorCol"
    Write-Host "Researcher Ids column: $researcherIdCol"
    Write-Host "ORCIDs column: $orcidCol"

    # Show first 5 rows
    if ($authorCol -gt 0) {
        Write-Host "`nFirst 5 rows of Diaspora_Author_Names:"
        for ($row = 2; $row -le 6; $row++) {
            $cellValue = $worksheet.Cells.Item($row, $authorCol).Value2
            Write-Host "Row $row`: $cellValue"
        }
    }

    if ($researcherIdCol -gt 0) {
        Write-Host "`nFirst 5 rows of Researcher Ids:"
        for ($row = 2; $row -le 6; $row++) {
            $cellValue = $worksheet.Cells.Item($row, $researcherIdCol).Value2
            Write-Host "Row $row`: $cellValue"
        }
    }

    if ($orcidCol -gt 0) {
        Write-Host "`nFirst 5 rows of ORCIDs:"
        for ($row = 2; $row -le 6; $row++) {
            $cellValue = $worksheet.Cells.Item($row, $orcidCol).Value2
            Write-Host "Row $row`: $cellValue"
        }
    }

    # Clean up
    $workbook.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($excel) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}
