from parseregister import main
import os

for file in os.listdir("register"):
    if not file.endswith(".pdf"):
        continue
    dept = file.split(".")[0]
    os.popen("python parseregister.py register/%s > out/%s.txt" % (file, dept))
    #main(["parseregister", "register/"+file, "-o", "out/"+file])
