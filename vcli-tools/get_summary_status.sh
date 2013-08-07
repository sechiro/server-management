#!/bin/bash
set -ue
export PERL_LWP_SSL_VERIFY_HOSTNAME=0

VCLI_PATH=/usr/lib/vmware-vcli/apps
_DEBUG=${_DEBUG:-"0"}
user=readonly_user
password=password

usage(){
    local _line_index=$(( ${#BASH_LINENO[@]} - 2 ))
    if [ $_DEBUG = 1 ];then
        echo -n "[`basename $0`: LineNo: ${BASH_LINENO[$_line_index]}] " 1>&2
    fi
    echo "Usage: ./`basename $0` [-m mode(summary, network, all)] esx_hostname" >&2
    exit 1
}
mode=summary
while getopts "m:" OPT
do
    case $OPT in
        m) mode=$OPTARG;;
        *) usage $LINENO;;
    esac
done
# cut options from arguments
shift $(( $OPTIND - 1 ))

if [ $# != 1 ];then
    usage $LINENO
fi
if [[ $mode =~ ^(summary|network|all)$ ]];then
    perl get_summary_status.pl --username $user --password $password --server $1 --display $mode
else
    usage $LINENO
fi
