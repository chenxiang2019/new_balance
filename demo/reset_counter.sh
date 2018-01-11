set -e
sudo ./simple_switch_CLI --thrift-port $1 < rules/reset_counter.txt
