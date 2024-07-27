import sys

print(f"python {sys.version} found")
if (sys.version_info[0] < 3) or (sys.version_info[1] < 7):
    print ("Wrong python version found")
    exit(1)

exit(0)