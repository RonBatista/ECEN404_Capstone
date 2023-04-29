import sys
import os
import shutil
import time
from zipfile import ZipFile
#import paramiko

def main():
    zip_file_path_noExt = sys.argv[1]       #grabs system arguments containing the path to the temp results dirtectory and zipfile downloaded by the client

    zip_file_path = sys.argv[2]

    selected_ortho_temp = sys.argv[3]

    selected_shape_name = sys.argv[4]

    location = "/var/www/html/uas_data/download/product/"
    directory = selected_ortho_temp + "_" + selected_shape_name

    path = os.path.join(location, directory)

    #This commented section was an attempt of using an import called paramiko to run commands. Was still in testing.
    #file_path = sys.argv[1].split("::")
    #print("Split path: ", file_path)


    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname='158.101.127.212', username='ubuntu', pkey='')

    t = 604800  # a week in seconds
    #t = 10 #timer test
    while t:  #loop creates timer to keep data in data in database for t amount of time before deleting
       mins, secs = divmod(t, 60)
       timer = '{:02d}:{:02d}'.format(mins, secs)
       time.sleep(1)
       t -= 1 # reduces t variable

    if (os.path.exists(zip_file_path_noExt)):   #if these paths exist, delete them


        shutil.rmtree(path, ignore_errors=True)
        os.remove(zip_file_path_noExt)
        print("The temp results directory and zip file were deleted successfully!")
        #stdin, stdout, stderr = ssh.exec_command('rm -r zip_file_path')
        #print(stdout.read().decode('utf-8'))

    else:
        print("The temp results directory and zip file do not exist!")


    #ssh.close()

#---------------------------------------------------------------------------------------------------------------------Run Main
if __name__ == "__main__":
    main()
