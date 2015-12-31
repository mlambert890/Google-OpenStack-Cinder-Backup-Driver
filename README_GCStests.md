# Introduction

    This script is for testing Google cinder backup driver.
    Below backup tests are covered by this script:

    1. create a full backup of 1GB volume
         * create a volume of size 1GB
         * create a full backup from 1GB volume

    2. create a incremental backup of 1GB volume having a full backup

    3. restore incremental backup to new volume

    4. restore incremental backup to original volume

    Note:
        * listing of cinder volumes and backups on tests completion
        * exception handling while running tests
        * resource(volume, backup) cleanup at end of tests completion
        * run the tests by running below command:
            python GCStests.py -u OS_USER_NAME -p OS_PASSWORD -t OS_TENANT_NAME -a OS_AUTH_URL -s <volume_size>
              Ex: python GCStests.py -u admin -p demo123 -t admin -a http://127.0.0.1:5000/v2.0 -s 2
        
              * OS_USER_NAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL are openstack credentials
              * size of volume for tests is configurable with -s option
              * default values are:
                    OS_USER_NAME: admin
                    OS_PASSWORD: Biarc8123
                    OS_TENANT_NAME: admin
                    OS_AUTH_URL: http://127.0.0.1:5000/v2.0
                    volume_size: 1
                     
