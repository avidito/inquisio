# DB Initialization Script
# Description:
#   Script to reconstruct Database, Schema and Admin for Inquisio. Configuration will be read from conf.txt.
# Args:
#   -
# Prompt:
#   - USER: str. Database superuser username
#   - PASS: str. Database superuser password
# Example:
#   & .\init.ps1

########## VARIABLE ##########
Get-Content conf.txt | Foreach-Object{
   $var = $_.Split('=')
   New-Variable -Name $var[0] -Value $var[1]
}
$user = Read-Host "Superuser Username"
$pass = Read-Host "Superuser Password" -AsSecureString
$env:PGPASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass))
$env:PGOPTIONS = "--client-min-messages=warning"

########## MAIN ##########
# Start execution logging
$start_ut = $(Get-Date -UFormat %s)
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Start $database database and admin initiation"

# Delete existing database, schema and admin role for Inquisio
psql -h $hostname -U $user -c "DROP DATABASE IF EXISTS $($database);" -q
psql -h $hostname -U $user -c "DROP ROLE IF EXISTS $($admin_user);" -q

# Create admin role
psql -h $hostname -U $user -c "CREATE ROLE $($admin_user) WITH CREATEROLE LOGIN PASSWORD '$($admin_pass)';" -q
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Succesfully create '$admin_user' as Inquisio admin"

# Create database
psql -h $hostname -U $user -c "CREATE DATABASE $($database);" -q
psql -h $hostname -U $user -c "GRANT ALL PRIVILEGES ON DATABASE $($database) TO $($admin_user);" -q
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Succesfully create '$database' database"

# Create SrC schema
$env:PGPASSWORD = $admin_pass
psql -h $hostname -d $database -U $admin_user -c "CREATE SCHEMA $($schema_src);" -q
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Succesfully create '$schema_src' schema as CDC schema"

# Create Archive schema
psql -h $hostname -d $database -U $admin_user -c "CREATE SCHEMA $($schema_dw);" -q
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Succesfully create '$schema_dw' schema as Archive schema"

# Create Table from DDL
psql -h $hostname -d $database -U $admin_user -f "ddl/table_src.sql" -q
psql -h $hostname -d $database -U $admin_user -f "ddl/table_dw.sql" -q

# Clear environment variable
Remove-Item Env:PGPASSWORD
Remove-Item Env:PGOPTIONS

# End execution logging
$end_ut = $(Get-Date -UFormat %s)
$duration = $($end_ut - $start_ut)
Write-Host "[$(Get-Date -UFormat '%Y-%m-%d %H:%M:%S')] Succesfully reconstruct $database database, schema and admin role in $([int]$duration) second(s)."
