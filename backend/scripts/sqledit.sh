#!/usr/bin/env bash

# This script is used to eliminate the manual editing of the 
# large PCR SQL files that would originally cause errors while
# importing into MySQL.
#
# Instructions for usage:
# Place this file in the same directory as your SQL files containing the PCR data. Run using:
#
# ./sqledit.sh
#
# #
# 1. Deletes the first line causing an error.
# 2. Replaces TO_DATE() with STR_TO_DATE() in the ratings file TEST_PCR_RATING_V.sql.
# 3. Replaces the date format from the Oracle format to the MySQL format in the ratings file.

files=("TEST_PCR_COURSE_DESC_V.sql" "TEST_PCR_CROSSLIST_SUMMARY_V.sql" "TEST_PCR_SUMMARY_HIST_V.sql" "TEST_PCR_SUMMARY_V.sql" "TEST_PCR_RATING_V.sql")

for i in {0..4}
do
	echo "${files[i]} being worked on..."
	first_line=$(head -1 ${files[i]})
	if [[ "$first_line" == "SET DEFINE OFF;"* ]]
		then
		tail -n +2 ${files[i]} > "f.tmp"
	else
		continue
	fi
	if [[ i -eq 4 ]]
		then
		echo "Replacing TO_DATE with STR_TO_DATE..."
		sed -i "s/TO_DATE/STR_TO_DATE/g" f.tmp
		echo "Replacing the date format..."
		sed -i "s/MM\/DD\/YYYY HH24:MI:SS/%m\/%d\/%Y %H:%i:%s/g" f.tmp
	fi
	cat f.tmp > "${files[i]}"
	rm f.tmp
done
echo "Done."
