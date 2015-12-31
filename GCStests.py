from cinderclient.v2 import client
import sys,re,getopt
import subprocess
import time

def check_status(obj, id, sleep=None,status_check=True):
    """Checking object status to became avaliable."""
    status_code = -1
    while status_check:
        status= obj.get(id).status
        if status=="available":
            status_check = False
            status_code = 0
        elif "error" in status:
            status_check = False
            status_code = 1
        elif sleep:
            time.sleep(sleep)
    return status_code

def check_delete_status(obj, id, msg):
    status_check = True
    while status_check:
        try:
            del_obj = obj.get(id)
            if del_obj.status == "deleting":
                print "status is deleting."
                time.sleep(10)
            else:
                print "status is error."
                status_check = False
        except Exception:
            print "%s deleted successfully." % msg
            status_check = False

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Poll process for new output until finished

    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break

        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output

def logger(var1, var2):
    print "%s failed due to status of %s not available." %(var1, var2)


class GCSTest():
    def __init__(self, username, pwd, tenant, auth_url, vol_size):
        self.username = username
        self.pwd = pwd
        self.tenant = tenant
        self.auth_url = auth_url
        self.vol_size = vol_size
        self.cinder = client.Client(username, pwd, tenant, auth_url)
        self.testvol = self.testbackup = self.testincbackup = self.newv = None        

    def cleanup_resource(self):
        print "cleanup resource"
        cinder = self.cinder
        testvol = self.testvol
        testbackup = self.testbackup
        testincbackup = self.testincbackup
        newv = self.newv
        if testincbackup:
            cinder.backups.delete(testincbackup.id)
            check_delete_status(cinder.backups, testincbackup.id, "incremental backup")

        time.sleep(5)
        if testbackup:
            cinder.backups.delete(testbackup.id)
            check_delete_status(cinder.backups, testbackup.id, "full backup")

        time.sleep(5)

        if newv:
            cinder.volumes.delete(newv.volume_id)
            check_delete_status(cinder.volumes, newv.volume_id, "restored volume")

        time.sleep(5)

        if testvol:
            cinder.volumes.delete(testvol.id)
            check_delete_status(cinder.volumes, testvol.id, "original backup-volume")

        print ""
        print "Testing GCS Cinder backup driver: end"

    def GCS_test(self):
        print "Testing GCS Cinder backup driver: start\n"
        print "    Test1: create a full backup of %sGB volume" % self.vol_size
        print "        a) create a volume of size %sGB" % self.vol_size
        cinder = self.cinder
        testvol = cinder.volumes.create(name="test-vol", size=self.vol_size)
        status_code = check_status(cinder.volumes, testvol.id)

        if status_code == 1:
            logger("Test1", "volume")
            return

        print "               Volume created with id:", testvol.id

        time.sleep(5)

        print "        b) create a full backup from %sGB volume" % self.vol_size
        testbackup = cinder.backups.create(testvol.id)
        status_code = check_status(cinder.backups, testbackup.id, 10)

        if status_code == 1:
            logger("Test1", "backup")
            return

        print "               Full backup created with id: ", testbackup.id

        time.sleep(5)

        print "    Test2: create a incremental backup of %sGB volume having a full backup" % self.vol_size
        testincbackup= cinder.backups.create(testvol.id, incremental=True)
        status_code = check_status(cinder.backups, testincbackup.id, 10)

        if status_code == 1:
            logger("Test2", "backup")
            return

        print "               Incremental Backup created with  id:",testincbackup.id

        time.sleep(5)

        print "    Test3: Restore incremental backup to new volume."
        newv= cinder.restores.restore(testincbackup.id)
        status_code = check_status(cinder.volumes, newv.volume_id, 10)

        if status_code == 1:
           logger("Test3", "volume")
           return

        print "               Restore done with new volume id:", newv.volume_id

        time.sleep(5)

        print "    Test4: Restore incremental backup to original volume."
        oldv= cinder.restores.restore(testincbackup.id, testvol.id)
        status_code = check_status(cinder.volumes, oldv.volume_id, 10)

        if status_code == 1:
            logger("Test4", "volume")
            return

        print "               Restore done with original volume id:", oldv.volume_id

        time.sleep(5)

        credential = '--os-username %s --os-password %s --os-tenant-name %s --os-auth-url %s' % (self.username, self.pwd, self.tenant, self.auth_url)
        vol_list  = 'cinder %s list' % credential
        execute(vol_list)

        bck_list = 'cinder %s backup-list' % credential
        execute(bck_list)
        self.testvol = testvol
        self.testbackup = testbackup
        self.testincbackup = testincbackup
        self.newv = newv
        
def main(argv):
    OS_USER_NAME = 'admin'
    OS_PASSWORD = 'Biarc8123'
    OS_TENANT_NAME='admin'
    OS_AUTH_URL='http://127.0.0.1:5000/v2.0'
    VOL_SIZE = 1
    try:
        opts, args = getopt.getopt(argv,"hu:p:t:a:s:", ["username=","password=","tenantname=","authurl=","vol_size="])
    except getopt.GetoptError:
        print getopt.GetoptError
        print 'test.py -u <username> -p <password> -t <tenantname> -a <authurl> -s <volume_size>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python GCStests.py -u <username> -p <password> -t <tenantname> -a <authurl> -s <volume_size>'
            sys.exit()
        elif opt in ("-u", "--username"):
            OS_USER_NAME = arg
        elif opt in ("-p", "--password"):
            OS_PASSWORD = arg
        elif opt in ("-t", "--tenantname"):
            OS_TENANT_NAME = arg
        elif opt in ("-a", "--authurl"):
            OS_AUTH_URL = arg
        elif opt in ("-s", "--vol_size"):
            VOL_SIZE = arg

    gcs =  GCSTest(OS_USER_NAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, VOL_SIZE)
    try:
        gcs.GCS_test()
        gcs.cleanup_resource()
    except Exception:
        gcs.cleanup_resource()


if __name__ == "__main__":
   main(sys.argv[1:])
