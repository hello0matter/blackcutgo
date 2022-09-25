wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar -xf Python-3.7.9.tgz
mv Python-3.7.9 python3
cd python3
./configure --prefix=/usr/local/python3 \--with-ssl \--enable-optimizations
make
make install
cd /usr/bin
mv python python.bak
ln -s /usr/local/python3/bin/python3 /usr/bin/python
#此处/usr/local/python3路径为步骤2中安装包解压后的路径
python -V
# 输出结果：Python 3.7.9