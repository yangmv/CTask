FROM centos:7
# 设置编码
ENV LANG en_US.UTF-8

# 同步时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 1. 安装基本依赖
RUN yum update -y && yum install epel-release -y && yum update -y && yum install wget unzip epel-release nginx  xz gcc automake zlib-devel openssl-devel supervisor  net-tools mariadb-devel groupinstall development  libxslt-devel libxml2-devel libcurl-devel git -y

# 2. 准备python
RUN wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz
RUN xz -d Python-3.6.6.tar.xz && tar xvf Python-3.6.6.tar && cd Python-3.6.6 && ./configure && make && make install

# 3. 复制代码
ADD . /var/www/CTask/
WORKDIR /var/www/CTask/

# 4. 安装pip依赖
RUN pip3 install --user --upgrade pip
RUN pip3 install -r requirements.txt

# 5. 数据初始化
# python3 manage.py db init        #首次需要
# python3 manage.py db migrate
# python3 manage.py db upgrade

# 6. 日志
VOLUME /var/log/

# 7. 准备文件
COPY docs/supervisor_cron.conf  /etc/supervisord.conf
COPY docs/nginx_cron.conf /etc/nginx/conf.d/

EXPOSE 80
CMD ["/usr/bin/supervisord"]

#docker build -t ctask .
#docker run --name ctask -d -p 5001:80 ctask:latest