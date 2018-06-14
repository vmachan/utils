#
# NAME        : remove_last_line_from_files
# USAGE       : remove_last_line_from_files.ps1 <Path to directory containing files> <Regex pattern to filter files e.g. *.sql>
# DESCRIPTION : This is a small utility that will accept a file path and a regular expression to identify files in that path 
#               It then loops thru the files removing the last line from each and overwriting it in place.
#               It displays each file name as is processes it.
#

Param
(
  [Parameter(Mandatory=$true)]
  [ValidateNotNull()]
  $p_path
 ,
  [Parameter(Mandatory=$true)]
  [ValidateNotNull()]
  $p_file_extension
)

if (!$p_path) {
  Write-Host "Please provide path to files"
  EXIT
}

if (!$p_file_extension) {
  Write-Host "Please provide file extension e.g. *.txt"
  EXIT
}

Write-Host "Parameter Path is $p_path"
Write-Host "Parameter file extension are $p_file_extension"
pause

$files = Get-ChildItem -path ".\$p_path\" -filter $p_file_extension

foreach ($item in $files)
{
    Write-Host "${item} "
    $search = Get-content $item.FullName
    $output = $search[0..($search.count - 2)]
    $output | Set-Content $item.FullName
}

