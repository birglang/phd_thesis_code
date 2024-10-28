sudo -i
cd ~
git clone https://github.com/mininet/mininet.git
export PYTHONPATH=$PYTHONPATH:$HOME/mininet


run controller on different port

ryu-manager --ofp-tcp-listen-port 6633 FirstController.py
ryu-manager --ofp-tcp-listen-port 6634 SecondController.py





