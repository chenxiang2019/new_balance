set -e
sudo ./simple_switch_CLI --thrift-port 22222 < rules/default.txt
sudo ./simple_switch_CLI --thrift-port 22223 < rules/default.txt
sudo ./simple_switch_CLI --thrift-port 22224 < rules/default.txt
sudo ./simple_switch_CLI --thrift-port 22225 < rules/default.txt
sudo ./simple_switch_CLI --thrift-port 22226 < rules/default.txt
