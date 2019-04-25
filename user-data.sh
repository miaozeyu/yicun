#!/usr/bin/env bash

sudo yum update -y

sudo yum groupinstall -y 'development tools'
sudo yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel mysql-server mysql-devel

sudo yum install epel-release
sudo yum install nginx
#sudo service nginx start
#sudo service nginx restart
#ifconfig eth0 | grep inet | awk '{ print $2 }'


wget http://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
sudo yum install xz-libs
xz -d Python-3.6.4.tar.xz
tar -xvf Python-3.6.4.tar

cd Python-3.6.4
./configure --prefix=/usr/local --with-ssl

sudo make
sudo make altinstall
export PATH="/usr/local/bin:$PATH"

echo "alias python3='python3.6'
alias pip3='pip3.6'" >> ~/.bashrc

pip3 install virtualenv --user


mkdir hackerjobnow
cd hackerjobnow
virtualenv -p python3.6 app_venv
git clone https://github.com/miaozeyu/hackerjobnow.git
mv yicun app
source app_venv/bin/activate
pip3 install -r requirements.txt

pip3 install gunicorn
gunicorn app:app -b localhost:8000 &
nohup gunicorn app:app -b localhost:8000 &
ps ax|grep gunicorn

pip3 install supervisor
cd ~
echo_supervisord_conf > supervisord.conf
sudo mv supervisord.conf /etc/supervisord.conf
echo "[program:hackerjobnow]
directory=/home/ec2-user/hackerjobnow/app
command=/home/ec2-user/hackerjobnow/app_venv/bin/gunicorn app:app -b localhost:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/hackerjobnow/hackerjobnow.err.log
stdout_logfile=/var/log/hackerjobnow/hackerjobnow.out.log" >> /etc/supervisord.conf


sudo vim /etc/nginx/conf.d/virtual.conf
sudo -s 'echo "server {
    listen       80;
    server_name  your_public_dnsname_here;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}" >> /etc/nginx/conf.d/virtual.conf'

sudo nginx -t

#gunicorn --log-file error_logs.log
#gunicorn --access-logfile acclogs
#gunicorn --log-level error
#gunicorn --name hackerjobnow_app


sudo python3 -m pip uninstall pip && sudo apt install python3-pip --reinstall




