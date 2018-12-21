## 特性

- 可视化界面操作
- 定时任务统一管理

- 完全兼容Crontab
- 支持秒级定时任务
- 任务可搜索、暂停、编辑、删除

## 部署

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

#### 五 用户使用说明
##### 新增任务
- Job_id： 任务名称，建议为有意义的英文名称
- 可执行命令： Linux Bash 命令
- 任务定时器： （秒、分、时、日、月、周）
- 示例：每分钟的第20秒开始执行pwd命令

![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/01.png)

##### 任务暂停/恢复
![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/02.png)

##### 任务日志
![image](https://raw.githubusercontent.com/yangmv/CTask/master/images/03.png)


## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).