import ctypes
import getpass
import os
import platform
import socket
import time
import urllib
import uuid


SURVEY_FORMAT = '''
System Platform     - {}
Processor           - {}
Architecture        - {}
Internal IP         - {}
External IP         - {}
MAC Address         - {}
Internal Hostname   - {}
External Hostname   - {}
Hostname Aliases    - {}
FQDN                - {}
Current User        - {}
System Datetime     - {}
Admin Access        - {}'''


def run(plat):
    # OS information
    sys_platform = platform.platform()
    processor    = platform.processor()
    architecture = platform.architecture()[0]

    print("sys_platform:  "+sys_platform+"\n")
    print("processor:  "+processor+"\n")
    print("architecture:  "+architecture+"\n")
    # session information
    username = getpass.getuser()
    print("username:  "+username+"\n")
    # network information
    hostname    = socket.gethostname()
    fqdn        = socket.getfqdn()
    print("hostname:  "+hostname+"\n")
    print("fqdn:  "+fqdn+"\n")
    try:
        internal_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        internal_ip = ''
    raw_mac     = uuid.getnode()
    mac         = ':'.join(('%012X' % raw_mac)[i:i+2] for i in range(0, 12, 2))
    print("internal_ip:  "+internal_ip+"\n")
    print("mac:  "+mac+"\n")
    # get external ip address
    ex_ip_grab = [ 'ipinfo.io/ip', 'icanhazip.com', 'ident.me',
                   'ipecho.net/plain', 'myexternalip.com/raw',
                   'wtfismyip.com/text' ]
    # external_ip = ''
    # for url in ex_ip_grab:
    #     try:
    #         external_ip = urllib.urlopen('http://'+url).read().rstrip()
    #     except IOError:
    #         pass
    #     if external_ip and (6 < len(external_ip) < 16):
    #         break
    #print("external_ip:  "+external_ip+"\n")
    print("ext_hostname:  \n")
    # reverse dns lookup
    try:
        ext_hostname, aliases, _ = socket.gethostbyaddr(external_ip)
    except (socket.herror, NameError):
        ext_hostname, aliases = '', []
    aliases = ', '.join(aliases)
    print("aliases:  "+aliases+"\n")
    # datetime, local non-DST timezone
    dt = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]),
         time.localtime())
    print("dt:  "+dt+"\n")
    # platform specific
    is_admin = False

    if plat == 'win':
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    elif plat in ['linix', 'mac']:
        is_admin = os.getuid() == 0

    admin_access = 'Yes' if is_admin else 'No'
    print("admin_access:  "+admin_access+"\n")

    # return survey results
    info = "sys_platform: \t"+ sys_platform +"\n"+"processor:    \t"+processor+"\n"
    info += "architecture: \t"+architecture+"\n"+"internal_ip:  \t"+internal_ip+"\n"
    info += "mac:  \t\t"+mac+"\n"+"hostname:\t"+hostname+"\n"
    info += "fqdn:\t\t"+fqdn+"\n"+"username:\t"+username+"\n"
    info += "datetime\t"+dt+"\n"+"admin_access:\t"+admin_access
    print(info)
    # return SURVEY_FORMAT.format(sys_platform, processor, architecture,
    # internal_ip, external_ip, mac, hostname, ext_hostname, aliases, fqdn,
    # username, dt, admin_access)
    return info
