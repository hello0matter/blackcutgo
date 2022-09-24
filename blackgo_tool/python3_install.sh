#! /bin/bash
# demo 版本为3.7.6
# 首先安装 python3需要的依赖
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
# 下载压缩包
yum -y install wget && wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
# 解压缩
yum -y install tar && tar -zxvf Python-3.7.6.tgz
cd Python-3.7.6/
# 将python3编译到/usr/local下
yum -y install gcc gcc-c++ make automake
./configure --prefix=/usr/local/python3
make && make install
# 建立软连接
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3