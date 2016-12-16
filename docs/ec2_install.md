EC2 Instance:
ssh -i ~/.ssh/zgreyn-ds-or.pem ubuntu@ec2-54-200-118-123.us-west-2.compute.amazonaws.com

---- On EC2 Instance ---
* git clone https://github.com/zreyn/vegf.git
* chmod +x vegf/src/install.sh
* vegf/src/install.sh

scp -i ~/.ssh/zgreyn-ds-or.pem ~/.aws/config ubuntu@ec2-54-200-118-123.us-west-2.compute.amazonaws.com:.aws/.

scp -i ~/.ssh/zgreyn-ds-or.pem ~/.aws/zgreyn-credentials ubuntu@ec2-54-200-118-123.us-west-2.compute.amazonaws.com:.aws/credentials

* tmux
* python vegf/src/create_tiles.py
