#!/bin/bash
set -ue

script_dir=$(cd $(dirname $0);pwd)
source $script_dir/creds/defaultrc
source $script_dir/vcli-env.sh

hosts=${hosts:-"192.168.11.150 192.168.11.200"}

for i in $hosts
do
    echo "HOST: $i"
    $VCLI_PATH/vm/vminfo.pl --server $i
    echo ""
    echo ""
done
