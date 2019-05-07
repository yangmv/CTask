#!/usr/bin/env bash
# author : yangmv@126.com
# date   : 2019-05-07 16:38
# role   : CTask快速启动脚本
# 注意：本脚本不会安装docker和mysql环境,默认为执行机上面已安装docker和mysql环境
basedir="/var/www"

# DB信息请修改正确
mysql_host="10.211.55.4"
mysql_user="root"
mysql_pwd="123456"

function code_init() {
    echo "[Start] 克隆代码,并初始化配置"
    [ ! -d $basedir ] && mkdir $basedir
    cd $basedir && git clone https://github.com/yangmv/CTask.git
    sed -i "s/127.0.0.1/$mysql_host/g" CTask/config.py
    sed -i "s/root/$mysql_user/g" CTask/config.py
    sed -i "s/123456/$mysql_pwd/g" CTask/config.py
}

function mysql_init() {
    echo "[Start] 创建DB库,并导入SQL文件"
    cd $basedir/CTask
    mysql -h $mysql_host -u $mysql_user -p$mysql_pwd -e "create database ctask default character set utf8mb4 collate utf8mb4_unicode_ci;"
    mysql -h $mysql_host -u $mysql_user -p$mysql_pwd ctask < docs/cron.sql
}

function docker_init() {
    echo "[Start] Docker构建镜像,并启动"
    cd $basedir/CTask
    docker build -t ctask .
    docker run --name ctask -d -p 5001:80 ctask:latest
}

code_init
mysql_init
docker_init

cat >> /etc/hosts <<EOF
127.0.0.1     cron.yangmv.com
EOF

echo "[注意] 请在需要访问的机器上添加hosts"
echo "you_host_ip     cron.yangmv.com"
echo "然后请用浏览器访问  http://cron.yangmv.com:5001"


