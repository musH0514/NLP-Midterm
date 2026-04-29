# PowerShell script to extract authors from Excel file

$inputFile = ".\04_Diaspora_Articles_12195(1).xlsx"
$outputFile = ".\extracted_authors.csv"

Write-Host "Reading Excel file: $inputFile"

# Create Excel COM object
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $workbook = $excel.Workbooks.Open((Resolve-Path $inputFile))
    $worksheet = $workbook.Worksheets.Item(1)
    
    # Get used range
    $usedRange = $worksheet.UsedRange
    $rows = $usedRange.Rows.Count
    $cols = $usedRange.Columns.Count
    
    Write-Host "Worksheet has $rows rows and $cols columns"
    
    # Find Diaspora_Author_Names column
    $authorColumnIndex = 0
    for ($col = 1; $col -le $cols; $col++) {
        $header = $worksheet.Cells.Item(1, $col).Value2
        if ($header -eq "Diaspora_Author_Names") {
            $authorColumnIndex = $col
            Write-Host "Found Diaspora_Author_Names column at index $authorColumnIndex"
            break
        }
    }
    
    if ($authorColumnIndex -eq 0) {
        Write-Host "Error: Diaspora_Author_Names column not found!"
        $workbook.Close($false)
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        return
    }
    
    # Collect authors
    $allAuthors = @()
    
    for ($row = 2; $row -le $rows; $row++) {
        $cellValue = $worksheet.Cells.Item($row, $authorColumnIndex).Value2
        if ($cellValue -ne $null) {
            # Split by semicolon
            $authors = $cellValue -split ';'
            foreach ($author in $authors) {
                $author = $author.Trim()
                if ($author -ne "") {
                    $allAuthors += $author
                }
            }
        }
    }
    
    # Deduplicate
    $uniqueAuthors = $allAuthors | Select-Object -Unique | Sort-Object
    
    # Create CSV content
    $csvContent = "Author`n"
    foreach ($author in $uniqueAuthors) {
        $csvContent += "$author`n"
    }
    
    # Write to file
    $csvContent | Out-File -FilePath $outputFile -Encoding UTF8
    
    Write-Host "Extraction completed!"
    Write-Host "Total authors found: $($allAuthors.Count)"
    Write-Host "Unique authors after deduplication: $($uniqueAuthors.Count)"
    Write-Host "Results saved to: $outputFile"
    
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