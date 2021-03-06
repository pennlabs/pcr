#!/usr/bin/env ruby

# Penn Course Review Data Import Script
# Given the new semester data in the form of 5 sql files, add these files to the existing database and create a new database.
#
# Prerequisites:
#   - The 5 sql files should be in the same folder as the script.
#   - Pass in the correct arguments for semester and MySQL password.
#   - You should be in the pcr virtual environment.
#
# Database Assumptions:
#   - The database PCRDEV should exist.
#   - There should be an existing database in the format pcr_api_v{version}_{date}.
#
# Example Usage: ./update.rb --password <mysql root password> --semester '2017A 2017B' | tee log.txt
#
# Created by Eric Wang (@ezwang), 3/11/2018

require 'optparse'

options = {}

OptionParser.new do |opts|
  opts.on('-o', '--overwrite', 'Delete the most recent database and replace it.') do |v|
    options[:overwrite] = v
  end
  opts.on('-s', '--semester SEMESTER', 'Specify which semesters to import.') do |sem|
    options[:semester] = sem
  end
  opts.on('-p', '--password PASSWORD', 'Specify the MySQL root password.') do |pass|
    options[:password] = pass
  end
end.parse!

# used to connect to database
MYSQL_USR = 'root'
MYSQL_PWD = options[:password]

# sql files to import into PCRDEV
SQL_FILES = ['TEST_PCR_COURSE_DESC_V.sql', 'TEST_PCR_CROSSLIST_SUMMARY_V.sql', 'TEST_PCR_SUMMARY_HIST_V.sql', 'TEST_PCR_SUMMARY_V.sql']

# location of pcr repo
API_PATH = File.dirname(File.dirname(File.realpath(__FILE__)))

# which semesters to import
if options[:semester]
  SEMESTERS = options[:semester]
else
  puts 'Please specify a semester to import with --semester!'
  exit 1
end

# make sure pcr directory is set correctly
unless File.exist?(File.join(API_PATH, 'manage.py'))
  puts "The path to the pcr directory is set to '#{API_PATH}', but this folder does not seem valid!"
  puts "No manage.py file found in the pcr directory."
  exit 1
end

# make sure root password is set
unless options[:password]
  puts 'Please specify the MySQL root password with --password!'
  exit 1
end

past = Time.now

# make sure we are in pcr virtual environment
unless ENV.has_key?('VIRTUAL_ENV')
  puts 'You do not appear to be running inside the pcr virtual environment, exiting...'
  exit 1
end

# make sure that all sql files needed exist
SQL_FILES.each do |file|
  unless File.exist?(file)
    puts "File '#{file}' does not exist, terminating script..."
    exit 1
  end
end

old_dbs = `echo 'SHOW DATABASES;' | mysql -u #{MYSQL_USR} -p#{MYSQL_PWD}`.split("\n")
raise 'Failed to retrieve database information!' unless $?.success?
old_dbs = old_dbs.select { |db| db.start_with?("pcr_api") }.sort { |a, b| a.match(/v(\d+)/).captures[0].to_i <=> b.match(/v(\d+)/).captures[0].to_i }.reverse

if options[:overwrite]
  unless old_dbs[0].end_with?(Time.now.strftime("%Y%m%d"))
    puts "Not deleting database #{old_dbs[0]}, too old."
    puts "Exiting..."
    exit 1
  end
  old_db = old_dbs[1]
  puts "Deleting database #{old_dbs[0]}..."
  `echo 'DROP DATABASE #{old_dbs[0]};' | mysql -u #{MYSQL_USR} -p#{MYSQL_PWD}`
else
  old_db = old_dbs[0]
end
old_db_num = old_db.match(/v(\d+)/).captures[0].to_i

new_db = "pcr_api_v#{old_db_num + 1}_#{Time.now.strftime("%Y%m%d")}"

puts "Identified old database as #{old_db}..."

if old_db.end_with?(Time.now.strftime("%Y%m%d"))
  puts "The old database (#{old_db}) was created today, this may not be the correct old database."
  puts "Exiting..."
  exit 1
end

if File.exist?('backup-file.sql')
  puts 'File "backup-file.sql" already exists, deleting...'
  File.delete('backup-file.sql')
end

puts 'Dumping old database to backup-file.sql...'

`mysqldump --add-drop-table -u #{MYSQL_USR} -p#{MYSQL_PWD} #{old_db} > backup-file.sql`

puts 'Loading old database into PCRDEV...'

`mysql -u #{MYSQL_USR} -p#{MYSQL_PWD} PCRDEV < backup-file.sql`
File.delete('backup-file.sql') if $?.success?

puts 'Formatting new sql files...'

puts `/usr/bin/env bash #{File.join(API_PATH, 'scripts', 'sqledit.sh')}`
raise 'Failed to format sql files!' unless $?.success?

# remove all non-utf8 characters from sql files
SQL_FILES.each do |file|
  puts "Removing non-utf8 characters from '#{file}'..."
  contents = IO.read(file).encode('UTF-8', :invalid => :replace, :undef => :replace)
  IO.write(file, contents)
end

puts 'Importing sql files...'

SQL_FILES.each do |file|
  puts "Importing '#{file}'..."
  puts `mysql -u #{MYSQL_USR} -p#{MYSQL_PWD} PCRDEV < #{file}`
  raise "Failed to import file '#{file}'!" unless $?.success?
end

puts 'Running conversion script...'

system({
  'DATABASE_URL' => "mysql://#{MYSQL_USR}:#{MYSQL_PWD}@localhost:3306/PCRDEV",
  'API_IMPORT_DATABASE_NAME' => 'PCRDEV',
  'API_IMPORT_DATABASE_USER' => MYSQL_USR,
  'API_IMPORT_DATABASE_PWD' => MYSQL_PWD
}, "cd #{API_PATH}; python manage.py importfromisc #{SEMESTERS} --catcherrors --otheraliases")
raise 'Failed to run conversion script!' unless $?.success?

puts "Creating new database #{new_db}..."

`echo "CREATE DATABASE #{new_db}" | mysql -u #{MYSQL_USR} -p#{MYSQL_PWD}`

puts "Granting permissions on #{new_db} to pcr-staging..."

`echo "GRANT ALL PRIVILEGES ON #{new_db}.* TO 'pcr-staging'@'localhost';" | mysql -u #{MYSQL_USR} -p#{MYSQL_PWD}`

puts 'Dumping PCRDEV to file...'

`mysqldump -u #{MYSQL_USR} -p#{MYSQL_PWD} PCRDEV > backup-file.sql`

puts "Loading file into #{new_db}..."

`mysql -u #{MYSQL_USR} -p#{MYSQL_PWD} #{new_db} < backup-file.sql`
File.delete('backup-file.sql') if $?.success?

present = Time.now

puts "Success! Time taken: #{present - past} seconds"
