import os, sys
from collections import defaultdict
ldap_to_english = {"telephoneNumber":"phone",
                   "mail"           :"mail",
                   "givenName"      :"first_name",
                   "sn"             :"last_name",
                   "uid"            :"pennkey",
                   "title"          :"title",
                   "displayname"    :"display_name"}

def write_ldap_file(file_name, prefix):
  """make a cmd-line call to get all faculty starting w/ prefix into file"""
  os.system("""ldapsearch -h directory.upenn.edu -b 
               "ou=People, dc=upenn, dc=edu" -x  
               -LLL "(&(eduPersonAffiliation=fac)(uid=%s*))" >> %s"""
              % (prefix, file_name)
           )

def parse_ldap_file(file_name, entries=None):
  """ parse the LDAP results into a coherent form 
      (this code is way too complex for what it needs to do ATM)
  """
  f = open(file_name)
  entries = defaultdict(list) if entries is None else entries
  entry = {}
  for line in f:
    line = line.strip()
    if line != "":
      if ":" in line:
        k, v = map(lambda x: x.strip(), line.split(":", 1))
        if k in ldap_to_english:
          entry[ldap_to_english[k]] = v
    else:
      entries[(entry["first_name"], entry["last_name"])].append(entry)
      entry = {}

  return entries
