#!/usr/bin/env python2
#-*-encoding:utf-8-*-
"""
Loginsight agent scripts
"""
import base64
import os
import platform
#from jinja2 import Template
import socket
import time
import sys
import shlex
import getpass

#http://www.loginsight.cn/o/applications/2/
CLIENT_ID = "1S_wRvye9?Xq4mU91e!MPixJ9Qjl3yQIaW?7G=2j"
CLIENT_SECRET = "hLXU?HCktQu::1xz9EsjWMUq:yiLp2A=SgQpH4HKTgM4zFS@WMQjFtVGSYV.gu6wC!6UCgfxSqyzKUZWymuyQq_lUGQH;Udmhy3gvAQ73GNF3HXgzT94YkNP0RvIx:m1"

# 用户名和密码
# username='test'
# password = '123qwe'

username = str(raw_input('please input your usrname:\n'))
password = str(getpass.getpass('please input your password:\n'))
host_type = str(raw_input('please input your will add host type(e.g. web):\n'))

host_name = socket.gethostname()
platform_info = platform.system()
sys_type = platform.linux_distribution()[0]

url = "http://auth.loginsight.cn/o/token/"
headers = {"Authorization": "Basic " + base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)}
nxlog_data_path = '/etc/nxlog/data'

def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
        time.sleep(2)
        sys.exit()
    return msg

def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    return shlex.os.system(cmd)

class PreSetup(object):
    def __init__(self):
        self.dist = platform.linux_distribution(supported_dists=['system'])[0].lower()
        self.version = platform.linux_distribution(supported_dists=['system'])[1]

    @property
    def _is_redhat(self):
        if self.dist.startswith("centos") or self.dist.startswith(
                "red") or self.dist == "fedora" or self.dist == "amazon linux ami":
            return True

    @property
    def _is_centos7(self):
        if self.dist.startswith("centos") and self.version.startswith("7"):
            return True

    @property
    def _is_fedora_new(self):
        if self.dist == "fedora" and int(self.version) >= 20:
            return True

    @property
    def _is_ubuntu(self):
        if self.dist == "ubuntu" or self.dist == "debian":
            return True

    def check_platform(self):
        if not (self._is_redhat or self._is_ubuntu):
            print(u"支持的平台: CentOS, RedHat, Fedora, Debian, Ubuntu, Amazon Linux, 暂不支持其他平台安装.")
            exit()

    @staticmethod
    def check_bash_return(ret_code, error_msg):
        if ret_code != 0:
            color_print(error_msg, 'red')
            exit()


    def _rpm_repo(self):
        if self._is_redhat:
            color_print('开始安装epel源', 'green')
            bash('yum update')
            bash('yum -y install epel-release')


    def _depend_rpm(self):
        color_print('开始安装依赖包', 'green')
        if self._is_redhat:
            cmd = 'yum -y install git python-pip libdbi libdbi.so.0 libpcre.so.0 libpcre.so*'
            ret_code = bash(cmd)
            self.check_bash_return(ret_code, "安装依赖失败, 请检查安装源是否更新或手动安装！")
        if self._is_ubuntu:
            cmd1 = 'apt-get update'
            cmd2 = 'apt-get -y --force-yes install git python-pip  libdbi1 libapr1 libperl5.18'
            ret_code = bash('%s; %s' % (cmd1, cmd2))
            self.check_bash_return(ret_code, "安装依赖失败, 请检查安装源是否更新或手动安装！")


    def _require_pip(self):
        color_print('开始安装依赖pip包', 'green')
#        bash('pip uninstall -y pycrypto')
#        bash('rm -rf /usr/lib64/python2.6/site-packages/Crypto/')
        ret_code = bash('pip install -r requirements.txt')
        self.check_bash_return(ret_code, "安装Loginsight依赖的python库失败！")


    def start(self):
        color_print('请务必先查看https://github.com/zsjohny/loginsight_agent/blob/master/README.md')
        time.sleep(3)
        self.check_platform()
        self._rpm_repo()
        self._depend_rpm()
        self._require_pip()

#    os.system('python %s' % os.path.join(jms_dir, 'install/next.py'))
def main():
    pathisexists=os.path.exists(nxlog_data_path)
    if platform_info == "Linux" or platform_info == "linux" :
        if pathisexists:
            pass
        else:
           os.makedirs(nxlog_data_path)
        color_print('准备安装Agent', 'green')
        if sys_type == "Ubuntu":
#           os.system('sudo apt-get install  libdbi1 libapr1 libperl5.18 -y')
            color_print('Cleaning the cache...', 'yellow')
            time.sleep(3)
            os.system('rm -rf /tmp/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
            os.system('wget -P /tmp https://nxlog.co/system/files/products/files/1/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
            os.system('sudo dpkg -i /tmp/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
            os.system('rm -rf /tmp/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb*')
        elif sys_type == "Redhat" in sys_type or sys_type =="CentOS Linux":
#           os.system('yum install -y libdbi libdbi.so.0 libpcre.so.0 libpcre.so*')
            color_print('Cleaning the cache...', 'yellow')
            time.sleep(3)
            os.system('rm -rf /tmp/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm*')
            os.system('wget -P /tmp https://nxlog.co/system/files/products/files/1/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm')
            os.system('rpm -ivh /tmp/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm --nodeps')
            os.system('rm -rf /tmp/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm*')
        else:
            color_print('你的linux 衍生版不在维护范围内!')
    elif platform_info == "Windows":
        color_print('请阅读window文档安装', 'red')
    else:
        color_print('不支持mac系统', 'red')


def ca():
    ca_file = 'CA.tar.gz'
    ca_username = 'loginsight'
    ca_passwd = 'loginsight'
    Auth = '%s:%s' % (ca_username, ca_passwd)
    ca_url = 'http://%s@download.loginsight.cn/%s' % (Auth, ca_file)
    # Download ca
    os.system('wget -P %s %s' % (nxlog_data_path, ca_url))
    os.system('tar fvxz %s/%s -C %s' % (nxlog_data_path, ca_file, nxlog_data_path))
    os.system('rm -rf %s/%s' % (nxlog_data_path, ca_file))


def get_access_token():
    import requests
    # 请求oauth access token
    print '\n\nget access token ...'
    r = requests.post(url, data={'grant_type': 'password', 'username': username, 'password':password}, headers=headers)
    access_token = r.json()
    return access_token


def refresh_access_token():
    import requests
    print '\n\nrefresh access token...'
    # 刷新access token
    token = get_access_token()
    headers = {"Authorization": "Basic " + base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)}
    r = requests.post(url, data={'grant_type': 'refresh_token', 'refresh_token': token['refresh_token']}, headers=headers)
    token = r.json()
    return token


def scan_logs():
    if os.path.exists("/var/log"):
        for default_logfile in os.listdir("/var/log"):
            if default_logfile.endswith("log"):
                return default_logfile
                #todo: will add this to dict and caliing it on jinja
                #print(default_logfile)


# def download_CA():
#     response = urllib2.urlopen('http://www.example.com/')
#     html = response.read()


def registered():
    import requests
    access_token = get_access_token()
    print 'access_token ==', access_token
    headers = {"Authorization": access_token['token_type'] + " " + access_token['access_token']}

    # 获取sentry 实例
    # 向sentry 实例注册主机
    data = {'host_name': host_name, 'host_type': host_type, 'system': platform_info, 'distver': '1.0',
            'mac_addr': "ff-cc-cd-20-21-21"}
    r = requests.post(url="http://app.loginsight.cn/api/0/agent/hosts", data=data, headers=headers)
    host_key = r.json()['host_key']
    return host_key
    color_print('注册成功!', 'blue')


def custom_config():
    from jinja2 import Template
    host_key = registered()
    raw_input('Press any key to continue..\n')
    nxlog_config = '/etc/nxlog'
    tpl_file = './nxlog.conf.tpl'
    output_file = '%s/nxlog.conf' % nxlog_config
    cert_dir = '%s/CA' % (nxlog_data_path)
    #log_name = raw_input("Please input your log name:\n")

    log_path = raw_input("Please input your log path:\n")
    streamkey = raw_input("Please input your streamkey:\n")
    streamtype = raw_input("Please input your streamtype:\n")
    streamtag = raw_input("Please input your streamtag:\n")


    with open(tpl_file, "r") as fd:
        content = fd.read(4096)
        # print 'content = ', content
        template = Template(content)


    kwargs = {
    'LOG_PATH': log_path,
    'HOSTNAME': host_key,
    'STREAMKEY': streamkey,
    'SREAMTYPE': streamtype,
    'STREAMRAG': streamtag,
    'CERTDIR': cert_dir,
    'NXLOG_CONFIG_DIR': nxlog_config,
    'CERTDIR': cert_dir
    }

    a = template.render(**kwargs)
    print a
    with open(output_file,'w') as f:
        f.write(a)


    # if len(nxlog_config) == 0 or len(cert_dir) == 0 or len(log_name) == 0 or len(log_path) == 0 or len(host_name) == 0 or len(tag) == 0:
    #     print("Please input corrent path")
    # else:
    #     os.environ['nxlog_config'] = str(nxlog_config)
    #     os.environ['cert_dir'] = str(cert_dir)
    #     os.environ['log_name'] = str(log_name)
    #     os.environ['log_path'] = str(log_path)
    #     os.environ['host_name'] = str(host_name)
    #     os.environ['tag'] = str(tag)
    #     #The follow is result
    #     os.system('echo $nxlog_config')
    #     os.system('echo $cert_dir')
    #     os.system('echo $log_name')
    #     os.system('echo $log_path')
    #     os.system('echo $host_name')
    #     os.system('echo $tag')


if __name__ == "__main__":
    pre_setup = PreSetup()
    pre_setup.start()
    main()
    ca()
    custom_config = custom_config()
    color_print('安装完成!', 'yellow')
