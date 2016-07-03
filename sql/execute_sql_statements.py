import os

curr_dir_listing = os.listdir(".")
for files in sorted(curr_dir_listing):
    if not files.startswith("exe"):
        print "current file = %s" % files
        re = os.system('mysql -uroot < %s' % files)
        if re != 0:
            exit(1)
