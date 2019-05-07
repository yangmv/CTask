## 特性

- 可视化界面操作
- 定时任务统一管理

- 完全兼容Crontab
- 支持秒级定时任务
- 任务可搜索、暂停、编辑、删除

## 更新日志
- 2019-05-07      增加一键部署脚本,方便快速预览
- 2019-01-15      增加前端管理页面
- 2018-11-01      提交后端版本代码

## 快速体验部署[Docker]
```
vim quick_start.sh      #配置DB账号信息
bash quick_start.sh
```

## 普通部署
#### 一 安装依赖
```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

#### 二 配置
- 配置文件 config.py
- 配置数据库信息


#### 三 同步数据库
```
# python3 manage.py db init        #首次需要
# python3 manage.py db migrate
# python3 manage.py db upgrade
mysql -h 127.0.0.1 -u root -p123456 -e "create database ctask default character set utf8mb4 collate utf8mb4_unicode_ci;"
mysql -h 127.0.0.1 -u root -p123456 ctask < docs/cron.sql
```

#### 四 Supervisor
```
cat >> /etc/supervisord.conf <<EOF
[program:cron_job]
process_name=cron_job
command=/usr/local/bin/gunicorn -b 0.0.0.0:5001 manage:app --workers 4 --preload
directory=/opt/CTask/
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/cron_job.log
loglevel=info
EOF

supervisorctl update
supervisorctl reload
```

#### 五 Nginx配置
```
upstream  job{
        server  127.0.0.1:5001;
}

location / {
        root /var/www/CTask/dist;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        }

location /v1/cron/job {
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://job;
}
```

#### 五 用户使用说明
##### 新增任务
- Job_id： 任务名称，建议为有意义的英文名称
- 可执行命令： Linux Bash 命令
- 任务定时器： （秒、分、时、日、月、周）
- 示例：每分钟的第20秒开始执行pwd命令

![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/01.png)

##### 任务列表/可暂停/可恢复
![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/02.png)

##### 任务日志
![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/03.jpg)


## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).