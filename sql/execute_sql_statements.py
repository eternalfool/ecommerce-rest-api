import os

curr_dir_listing = os.listdir(".")
for files in sorted(curr_dir_listing):
    if not files.startswith("exe"):
        print "current file = %s" % files
        re = os.system(' mysql --host=us-cdbr-iron-east-04.cleardb.net --user=bb3b44179051f6 --password=d239bffa heroku_ec028af4a8b795d < %s' % files)
        if re != 0:
            exit(1)
