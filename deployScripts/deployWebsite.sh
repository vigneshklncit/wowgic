rm -rf /tmp/wowWebBackup
mv /var/www/*  /tmp/wowWebBackup
cp -r /home/wowgic/wowgic/wowgicWeb /var/www
chmod 777 /var/www/wowgicWeb/*
