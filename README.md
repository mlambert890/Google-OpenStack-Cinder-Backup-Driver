# Introduction

    This repo is for hosting OpenStack cinder backup driver source code for Google Cloud Storage(GCS).
    It also contains a configuration guide for using Google Cloud Storage(GCS) cinder backup driver.
    Also, it contains cinder exception file, Test plans file, Test automation script and sample cinder configuration file.

    1. Configuring_OpenStackwithGCS_BackupDriver_v1.5.1_Liberty.pdf
    2. Configuring_OpenStackwithGCS_BackupDriver_v1.5.2_Mitaka.pdf
      * Configuaration guide for using Google Cloud Storage(GCS) cinder backup driver

    2. README.md

    3. google.py
      * source code for Google Cloud Storage(GCS) cinder backup driver

    4. exception.py
      * update cinder exception file with GCS cinder backup driver exceptions

    5. GCS-TEST-PLANv3.pdf
      * Test plans

    6. cinder.conf
      * sample cinder.conf

    7. GCStests.py
      * Test automation script
      * Run below command for getting help
            python GCStests.py -h

    8. README_GCStests.md

# How to use Google Cloud Storage(GCS) cinder backup driver

  * GCS cinder backup driver is tested on ubuntu 14.04.03 server with OpenStack liberty and mitaka release.
  * It is compatible with any cinder volume backends like LVM backend, any third party cinder volume driver backend.
  * For getting detailed information on how to use it, please refer  "Configuring_OpenStackwithGCS_BackupDriver_v1.5.1_Liberty.pdf"
    and "Configuring_OpenStackwithGCS_BackupDriver_v1.5.2_Mitaka.pdf".
