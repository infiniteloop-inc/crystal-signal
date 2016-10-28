#!/bin/bash

#
# *** How to use ***
#
# 何も考えずにフルインストール
# $ sudo install.sh
#
# OSをアップデートせずにサーバープログラムだけをインストール
# $ sudo install.sh install
#
# バージョン1.1を指定してフルインストール
# $ sudo install.sh -r 1.1
#
# サーバープログラムのみを最新にアップデート
# $ sudo install.sh update
#
# サーバープログラムをバージョン1.2へアップデート
# $ sudo install.sh -r 1.2 update
#
# OSとサーバープログラムを最新にアップデート
# $ sudo install.sh fullupdate
#

if [ $(id -ru) -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

APT=/usr/bin/apt
WGET=/usr/bin/wget
TAR=/bin/tar
CAT=/bin/cat
CURL=/usr/bin/curl
SYSTEMCTL=/bin/systemctl
CHMOD=/bin/chmod
SED=/bin/sed
A2ENMOD=/usr/sbin/a2enmod
A2ENCONF=/usr/sbin/a2enconf
RSYNC=/usr/bin/rsync
RM=/bin/rm
CP=/bin/cp
JQ=/usr/bin/jq
MKTEMP=/bin/mktemp
SLEEP=/bin/sleep
RASPICONFIG=/usr/bin/raspi-config
TIMEDATECTL=/usr/bin/timedatectl

WORKDIR=/tmp
DOCUMENTROOT=/var/www/html
CGIDIR=${DOCUMENTROOT}/ctrl

SERVERVER=master

while getopts :r: OPT
do
    case $OPT in
        r)
            SERVERVER=$OPTARG
            ;;
        \?)
            ;;
    esac
done

shift $(($OPTIND - 1))

function os_update
{
    $APT update && $APT full-upgrade -y
}

function set_timezone
{
    $TIMEDATECTL set-timezone Asia/Tokyo
}

function install_pigpiod
{
    $APT update && $APT install -y pigpio python-pigpio
    $SYSTEMCTL enable pigpiod.service
    $SYSTEMCTL restart pigpiod.service
}

function install_apache
{
    $APT update && $APT install -y apache2 php5

    $SED -i -e '/.*#AddHandler cgi-script .cgi$/i \\tAddHandler cgi-script .py' /etc/apache2/mods-available/mime.conf
    $A2ENMOD cgi

    $CAT > /etc/apache2/conf-available/crystal-signal.conf <<EOF
<Directory /var/www/html/ctrl>
     Options +Indexes +ExecCGI
     DirectoryIndex controller.py
</Directory>
EOF

    $A2ENCONF crystal-signal
    $SYSTEMCTL restart apache2.service
}

function install_crystalsignal
{
    if [ ! -x $RSYNC ]; then
       $APT update && $APT install -y rsync
    fi

    if [ ! -x $JQ ]; then
       $APT update && $APT install -y jq
    fi

    RESTORE=0
    TEMP=$($MKTEMP)
    $CURL -s 'http://localhost/ctrl/?json=1' > $TEMP
    $JQ . $TEMP > /dev/null 2>&1

    if [ $? -eq 0 ]; then
       INFO=$($JQ .info $TEMP)
       REPEAT=$($JQ .repeat $TEMP)
       MODE=$($JQ .mode $TEMP)
       PERIOD=$($JQ .period $TEMP)
       RED=$($JQ .color[0] $TEMP)
       GREEN=$($JQ .color[1] $TEMP)
       BLUE=$($JQ .color[2] $TEMP)
       ACK=$($JQ .ack $TEMP)
       RESTORE=1
    fi

    $RM $TEMP

    $WGET -O ${WORKDIR}/crystal-signal.tar.gz "https://github.com/infiniteloop-inc/crystal-signal/archive/${SERVERVER}.tar.gz"

    $TAR xf ${WORKDIR}/crystal-signal.tar.gz -C $WORKDIR

    $CP ${WORKDIR}/crystal-signal-${SERVERVER}/bin/LEDController.py /usr/local/bin
    $CHMOD +x /usr/local/bin/LEDController.py

    $CAT > /etc/systemd/system/LEDController.service <<EOF
[Unit]
Description=LED Controller
After=pigpiod.service

[Service]
ExecStart=/usr/local/bin/LEDController.py

[Install]
WantedBy=multi-user.target
EOF

    $RSYNC -avz --delete ${WORKDIR}/crystal-signal-${SERVERVER}/html/ $DOCUMENTROOT/
    $CHMOD +x $CGIDIR/*.py

    $RM -rf ${WORKDIR}/crystal-signal-${SERVERVER}

    $SYSTEMCTL enable LEDController.service
    $SYSTEMCTL restart LEDController.service

    $SLEEP 5
    $CURL --globoff -s "http://localhost/ctrl/?color=0,0,128&mode=1&repeat=3&period=500&info=UPDATE%20SUCCESS" > /dev/null

    if [ $RESTORE -eq 1 ]; then
        $SLEEP 3
        $CURL -s "http://localhost/ctrl/?color=${RED},${GREEN},${BLUE}&mode=${MODE}&repeat=${REPEAT}&period=${PERIOD}&info=${INFO}&ack=${ACK}" > /dev/null
    fi
}

case "$1" in
    "update")
        install_crystalsignal
        ;;
    "fullupdate")
        os_update
        install_crystalsignal
        ;;
    "install")
        install_pigpiod
        install_apache
        install_crystalsignal
        ;;
    *)
        os_update
        set_timezone
        install_pigpiod
        install_apache
        install_crystalsignal
        ;;
esac

echo "FINISHED"
