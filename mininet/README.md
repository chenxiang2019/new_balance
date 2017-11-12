# Mininet: Emulator for rapid prototyping of Software Defined Networks

This document showcases how to get start with mininet.

## Install Mininet

Here we are trying to install mininet on your OS environment. All the steps have been tested under the Ubuntu system.

There are two common steps to install mininet. One approach is to install mininet automatically by using `apt-get`. Another way is to get the state-of-the-art source codes and compile it manually.

### Using `apt-get` to install Mininet 

This approach is very simple. You just need to execute one command under your console:

```
$ sudo apt-get install mininet
```

### Getting the source codes to install Mininet

Before your getting the source codes from Github, you should execute the after-mentioned commands to install the dependencies.

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install git
```

Then get the source codes:

```
$ git clone git://github.com/mininet/mininet
```

Go to the directory of mininet and read the information of the file `INSTALL`:

```
$ cd mininet
$ cat INSTALL
```

You could choose one of the approaches provided by `INSTALL`. I recommend you to install all the related softwares by passing `-a` parameter to `util/install.sh`:

```
$ sudo ./util/install.sh
```

Typical `install.sh` options include:

- `-a`: install everything that is included in the Mininet VM, including dependencies like Open vSwitch as well the additions like the OpenFlow wireshark dissector and POX. By default these tools will be built in directories created in your home directory.
- `-nfv`: install Mininet, the OpenFlow reference switch, and Open vSwitch 
- `-s mydir`: use this option before other options to place source/build trees in a specified directory rather than in your home directory.

**Hint: For more information on installation, you could visit the official website at http://mininet.org/download/ .**

## Hello World Example

This step assumes that you have installed mininet on your environment. 

It's very convenience to get start with mininet. You are just required to apply one command to build your first mininet topologic:

```
$ sudo mn
```

Then you create a simple topologic which has two hosts and one switch. Besides, the topologic has a controller that controls the whole network. 

![img](http://mininet.org/images/frontpage_diagram.png)

To apply your first experiment on mininet, execute this command:

```
mininet> h1 ping h2
```

If the console prints the ping information, congratulations! You have done this work!

For further understanding mininet, you could try the examples showed in this directory. 

Enjoy Mininet!