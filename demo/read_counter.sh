set -e
sudo ./simple_switch_CLI --thrift-port $1 < rules/read_counter.txt
