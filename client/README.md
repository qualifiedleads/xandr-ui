## Client application

#### Setup locally
````
1. Installing Node.js and Npm From Source on Ubuntu 14.04
apt-get install make g++ libssl-dev git
wget https://nodejs.org/dist/v4.4.7/node-v4.4.7.tar.gz
tar -xvf node-v4.4.7.tar.gz
cd node-v4.4.7
./configure
make && make install

2. Install npm module and global install gulp, bower 
cd ..../rtbstats/client 
sudo npm install gulp -g
sudo npm install bower -g
npm install
bower install

3. Build dist
gulp

4. Launch Angular front-end app with live reload
gulp serve

````
