EC2 Instance:
ssh -i ~/.ssh/zgreyn-ds-or.pem ubuntu@ec2-54-200-118-123.us-west-2.compute.amazonaws.com

---- On EC2 Instance ---
* git clone https://github.com/zreyn/vegf.git
* chmod +x nfl/src/install.sh
* nfl/src/install.sh
* tmux
* modify ip address in src/app.py
* sudo python src/app.py   

Note: this sudo is a really bad idea.  It's required to bind port 80, but we need to proxy Flask from NginX.
