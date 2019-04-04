Last login: Thu Apr  4 12:27:04 on ttys003
Jason-Shieh:~ Jason$ ssh -i /Users/Jason/Downloads/aws-ohio.pem ubuntu@3.16.210.32
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-1032-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Apr  4 18:06:40 UTC 2019

  System load:  0.0               Processes:              86
  Usage of /:   18.0% of 7.69GB   Users logged in:        0
  Memory usage: 19%               IP address for eth0:    172.31.47.117
  Swap usage:   0%                IP address for docker0: 172.17.0.1

 * Ubuntu's Kubernetes 1.14 distributions can bypass Docker and use containerd
   directly, see https://bit.ly/ubuntu-containerd or try it now with

     snap install microk8s --classic

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

72 packages can be updated.
41 updates are security updates.


Last login: Thu Apr  4 16:27:08 2019 from 160.39.184.75
ubuntu@ip-172-31-47-117:~$ docker version
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.4
 Git commit:        e68fc7a
 Built:             Mon Oct  1 14:25:31 2018
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.4
  Git commit:       e68fc7a
  Built:            Mon Oct  1 14:25:33 2018
  OS/Arch:          linux/amd64
  Experimental:     false

##start mysql

docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7


