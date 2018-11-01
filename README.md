# 定时任务特点

- 可视化界面操作
- 定时任务统一管理

- 完全兼容Crontab
- 支持秒级定时任务
- 任务可搜索、暂停、编辑、删除


#### 一 同步数据库
```
python3 manage.py db init        #首次需要
python3 manage.py db migrate
python3 manage.py db upgrade
```

#### 二 gunicorn
```
pip3 install guncorn
cd /opt/CTask
gunicorn -b 0.0.0.0:5000 manage:app --workers 4 --preload --reload
```


#### 三 Supervisor
```
cat >> /etc/supervisord.conf <<EOF
[program:cron_job]
process_name=cron_job
command=/usr/local/bin/gunicorn -b 0.0.0.0:5000 manage:app --workers 4 --preload
directory=/opt/CTask/
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/cron_job.log
loglevel=info
EOF

supervisorctl update
supervisorctl reload
```

#### 四 Nginx配置
```
upstream  job{
        server  127.0.0.1:5000;
}

location /api/v1.0/job/ {
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://job;
}
```
