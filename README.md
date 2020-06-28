| :exclamation: | I am not developing nor maintaining this code anymore. Use at your own risk. |
| --------------| ---------------------------------------------------------------------------- |


spiders
==============

If you are running the spiders under Mac OS X you probably first need to start
the Tor service:

````
tor
````

Under Linux, Tor typically runs as a service so you will not need to start it
manually. If for whatever reason you need to (re)start Tor under Linux you can
use `systemctl` (I am assuming an ArchLinux distro):

````
systemctl restart tor.service
````

You will also need to start the Polipo proxy server:

````
polipo
````

Finally, you can run a crawler (e.g. the momondo crawler) using:

````
cd momondo
scrapy crawl momondo -o output.csv
````
