#!/bin/sh
export DJANGO_SETTINGS_MODULE=api.settings
export PYTHONPATH=$(cd ..;pwd)


year=`date +%Y`
echo $year

day=`date +%j`
echo $day
if [$day>200]; then
  semester="a"
else
  semester="c"
fi
echo $semester

# Download from registrar
python download.py
if [ "$?" -ne "0" ]; then
  echo "Download script failed."
  exit 1
fi

# Import from Penn Course Review data
python import_from_pcr.py
if [ "$?" -ne "0" ]; then
  echo "Import from pcr failed."
  exit 1
fi

# Upload from the stuff that we downloaded
python uploadcourses.py $year $semester registrardata/*.txt
if [ "$?" -ne "0" ]; then
  echo "Upload script failed."
  exit 1
fi