#!/bin/bash
#This bash script will configure pure-ftp users/groups to simplify process of spinning up an FTP server on Kali
#Create ftpgroup group
groupadd ftpgroup

#Create ftpuser user and add to ftpgroup; sets that user to discard anything it saves to home(-d /dev/null); set that user to not have a shell (-s /etc)
useradd -g ftpgroup -d /dev/null -s /etc ftpuser

#create pure-ftp virtual user called offsec that maps to the actual user ftpuser(-u ftpuser), that has a home directory of /ftphome (-d)
pure-pw useradd offsec -u ftpuser -d /ftphome

#commit the changes to pure-ftp
pure-pw mkdb

#Change directories
cd /etc/pure-ftpd/auth/

#create symbolic links
ln -s ../conf/PureDB 60pdb

#create directory to serve as home directroy for virtual users; make parent directories as needed (-p)
mkdir -p /ftphome

#give full permissions to ftpuser and ftp group to the directory
chown -R ftpuser:ftpgroup /ftphome/

#restart pure-ftp server
/etc/init.d/pure-ftp restart
