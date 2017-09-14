#!/bin/bash

#
# *** How to use ***
#
# 下記のinstallと同等です。
# Same as "install" below
# $ sudo install.sh
#
# OSをアップデートせずにサーバープログラムだけをインストールします。
# Install Crystal Signal Pi middleware(without OS update).
# $ sudo install.sh install
#
# OSアップデートとタイムゾーンのセットをした上でインストールします。
# Install Crystal Signal Pi middleware(with OS update and set timezone).
# $ sudo install.sh fullinstall
#
# バージョンを指定してインストールします(VERSIONはGitHub上のリリースまたはブランチ名です)。
# Install with version specified(VERSION is release or branch on GitHub Repository).
# $ sudo install.sh -r VERSION
#
# サーバープログラムのみを最新にアップデートします。
# Update Crystal Signal Pi middleware(without OS update).
# $ sudo install.sh update
#
# サーバープログラムを指定のバージョンへアップデートします。
# Update Crystal Signal Pi middleware to specific version(without OS update).
# $ sudo install.sh -r VERSION update
#
# OSとサーバープログラムを最新にアップデートします。
# Update Crystal Signal Pi middleware and OS to latest release.
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
MKDIR=/bin/mkdir
MKTEMP=/bin/mktemp
SLEEP=/bin/sleep
RASPICONFIG=/usr/bin/raspi-config
TIMEDATECTL=/usr/bin/timedatectl
SORT=/usr/bin/sort
HEAD=/usr/bin/head
OPENJTALK=/usr/bin/open_jtalk
ESPEAK=/usr/bin/espeak
PHP=/usr/bin/php

WORKDIR=/tmp
DOCUMENTROOT=/var/www/html
CGIDIR=${DOCUMENTROOT}/ctrl

CSPIDIR=/var/lib/crystal-signal
SCRIPTDIR=${CSPIDIR}/scripts
SOUNDSDIR=${CSPIDIR}/sounds
VOICEDIR=${CSPIDIR}/voice
SCRIPTCONFFILE=${CSPIDIR}/ScriptSettings.json
GENERALCONFFILE=${CSPIDIR}/Settings.json

JQUERY=jquery-3.1.1.min.js

SERVERVER=master

APT_UPDATE=0

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

function apt_update
{
    if [ $APT_UPDATE -eq 0 ]; then
        $APT update
        APT_UPDATE=1
    fi
}

function os_update
{
    apt_update
    $APT full-upgrade -y
}

function set_timezone
{
    $TIMEDATECTL set-timezone Asia/Tokyo
}

function install_pigpiod
{
    apt_update
    $APT install -y pigpio python-pigpio
    $SYSTEMCTL enable pigpiod.service
    $SYSTEMCTL restart pigpiod.service
}

function install_apache
{
    apt_update
    $APT install -y apache2

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
    if [ ! -x $PHP ]; then
        apt_update
        $APT install -y php5
    fi

    if [ ! -x $RSYNC ]; then
        apt_update
        $APT install -y rsync
    fi

    if [ ! -x $JQ ]; then
        apt_update
        $APT install -y jq
    fi

    if [ ! -x $OPENJTALK ]; then
        apt_update
        $APT install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
    fi

    if [ ! -x $ESPEAK ]; then
        apt_update
        $APT install -y espeak
    fi

    RESTORE=0
    TEMP=$($MKTEMP)
    $CURL -s 'http://localhost/ctrl/?json=1' > $TEMP
    $JQ . $TEMP > /dev/null 2>&1

    if [ $? -eq 0 ]; then
       INFO=$($JQ -r .info $TEMP)
       REPEAT=$($JQ -r .repeat $TEMP)
       MODE=$($JQ -r .mode $TEMP)
       PERIOD=$($JQ -r .period $TEMP)
       RED=$($JQ -r .color[0] $TEMP)
       GREEN=$($JQ -r .color[1] $TEMP)
       BLUE=$($JQ -r .color[2] $TEMP)
       ACK=$($JQ -r .ack $TEMP)
       RESTORE=1
    fi

    $RM $TEMP

    $WGET -O ${WORKDIR}/crystal-signal.tar.gz "https://github.com/infiniteloop-inc/crystal-signal/archive/${SERVERVER}.tar.gz"

    $TAR xf ${WORKDIR}/crystal-signal.tar.gz -C $WORKDIR

    $CHMOD +x ${WORKDIR}/crystal-signal-${SERVERVER}/bin/*
    $RSYNC -avz ${WORKDIR}/crystal-signal-${SERVERVER}/bin/ /usr/local/bin/

    # install button & alert scripts
    if [ ! -d "${CSPIDIR}" ]; then
        $MKDIR ${CSPIDIR}
    fi

    if [ ! -d "${SCRIPTDIR}" ]; then
        $MKDIR ${SCRIPTDIR}
    fi

    if [ ! -d "${SOUNDSDIR}" ]; then
        $MKDIR ${SOUNDSDIR}
    fi

    if [ ! -d "${VOICEDIR}" ]; then
        $MKDIR ${VOICEDIR}
    fi

    # install version file
    $CP ${WORKDIR}/crystal-signal-${SERVERVER}/VERSION ${CSPIDIR}

    # install sample scripts
    $CHMOD +x ${WORKDIR}/crystal-signal-${SERVERVER}/scripts/*
    $RSYNC -avz ${WORKDIR}/crystal-signal-${SERVERVER}/scripts/ $SCRIPTDIR

    # install sample sound files
    $RSYNC -avz ${WORKDIR}/crystal-signal-${SERVERVER}/sounds/ $SOUNDSDIR

    # install HTS Voice
    $RSYNC -avz ${WORKDIR}/crystal-signal-${SERVERVER}/voice/ $VOICEDIR

    # install default config file
    if [ ! -f $GENERALCONFFILE ]; then
        $CAT > $GENERALCONFFILE <<EOF
{"brightness": 43}
EOF
    fi

    if [ ! -f $SCRIPTCONFFILE ]; then
        $CAT > $SCRIPTCONFFILE <<EOF
{"dropdown4": "---", "dropdown5": "---", "dropdown1": "---", "dropdown2": "Ack.sh", "dropdown3": "---"}
EOF
    fi

    # install systemd service
    $CAT > /etc/systemd/system/LEDController.service <<EOF
[Unit]
Description=LED Controller
After=pigpiod.service

[Service]
ExecStart=/usr/local/bin/LEDController.py

[Install]
WantedBy=multi-user.target
EOF

    # delete index.html files
    $RM -f ${DOCUMENTROOT}/index.html

    # install .php / .py files
    $RSYNC -avz ${WORKDIR}/crystal-signal-${SERVERVER}/html/ ${DOCUMENTROOT}/
    $CHMOD +x ${CGIDIR}/*.py

    # delete working directory
    $RM -rf ${WORKDIR}/crystal-signal-${SERVERVER}

    # install jQuery
    if [ ! -d "${DOCUMENTROOT}/js" ]; then
        $MKDIR ${DOCUMENTROOT}/js
    fi

    if [ ! -f "${DOCUMENTROOT}/js/${JQUERY}" ]; then
        $WGET -O ${DOCUMENTROOT}/js/${JQUERY} "https://code.jquery.com/${JQUERY}"
    fi

    # install bootstrap
    if [ ! -d "${DOCUMENTROOT}/css" ]; then
        $MKDIR ${DOCUMENTROOT}/css
    fi

    if [ ! -f "${DOCUMENTROOT}/css/bootstrap-3.3.7.min.css" ]; then
        $WGET -O ${DOCUMENTROOT}/css/bootstrap-3.3.7.min.css "https://raw.githubusercontent.com/infiniteloop-inc/bootstrap/v3-dev/dist/css/bootstrap.min.css"
    fi
    if [ ! -f "${DOCUMENTROOT}/js/bootstrap-3.3.7.min.js" ]; then
        $WGET -O ${DOCUMENTROOT}/js/bootstrap-3.3.7.min.js "https://raw.githubusercontent.com/infiniteloop-inc/bootstrap/v3-dev/dist/js/bootstrap.min.js"
    fi

    # install bootstrap-slider
    if [ ! -f "${DOCUMENTROOT}/css/bootstrap-slider-9.5.1.min.css" ]; then
        $WGET -O ${DOCUMENTROOT}/css/bootstrap-slider-9.5.1.min.css "https://raw.githubusercontent.com/infiniteloop-inc/bootstrap-slider/master/dist/css/bootstrap-slider.min.css"
    fi
    if [ ! -f "${DOCUMENTROOT}/js/bootstrap-slider-9.5.1.min.js" ]; then
        $WGET -O ${DOCUMENTROOT}/js/bootstrap-slider-9.5.1.min.js "https://raw.githubusercontent.com/infiniteloop-inc/bootstrap-slider/master/dist/bootstrap-slider.min.js"
    fi

    $SYSTEMCTL enable LEDController.service
    $SYSTEMCTL restart LEDController.service

    if [ $RESTORE -eq 1 ]; then
        $SLEEP 3
        $CURL -s "http://localhost/ctrl/?color=${RED},${GREEN},${BLUE}&mode=${MODE}&repeat=${REPEAT}&period=${PERIOD}&info=${INFO}&ack=${ACK}&noscript=1" > /dev/null
    fi
}

function clean_up_old_html
{
    version=1.0
    if [ -f "${CSPIDIR}/VERSION" ]; then
        version=$(cat ${CSPIDIR}/VERSION)
    fi

    version_lt $version 1.3

    if [ $? -eq 0 ]; then
        for delfile in ${DOCUMENTROOT}/index.html ${DOCUMENTROOT}/log.html ${DOCUMENTROOT}/settings.html ${CGIDIR}/ctrl_LowerHalf.html ${CGIDIR}/ctrl_UpperHalf.html
        do
            if [ -f "${delfile}" ]; then
                $RM -f ${delfile}
            fi
        done
    fi
}

function version_lt
{
    [ "$(printf '%s\n' "$@" | $SORT -Vr | $HEAD -n 1)" != "$1" ]
}

case "$1" in
    "update")
        clean_up_old_html
        install_crystalsignal
        ;;
    "fullupdate")
        os_update
        clean_up_old_html
        install_crystalsignal
        ;;
    "install")
        install_pigpiod
        install_apache
        install_crystalsignal
        ;;
    "fullinstall")
        os_update
        set_timezone
        install_pigpiod
        install_apache
        install_crystalsignal
        ;;
    *)
        install_pigpiod
        install_apache
        install_crystalsignal
        ;;
esac

echo "FINISHED"
