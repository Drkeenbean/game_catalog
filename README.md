game_catalog - v1.0 01-15-2016
===================================

A database to hold participants in a Swiss-style tournament, record and store their matches, and pair them into fair matches according to their win/loss standings.

Pre-requisites
--------------

- [Git](https://git-scm.com/downloads)
- [VirtualBox](https://www.virtualbox.org/)
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrant virtual machine](https://www.udacity.com/wiki/ud088/vagrant)

Getting Started
---------------

1. Follow the [guide](https://www.udacity.com/wiki/ud088/vagrant) to get the udacity VM cloned to your computer

2. Clone [this repo](https://github.com/Drkeenbean/game_catalog) into your vagrant directory

3. Navigate to your vagrant folder from the terminal/command prompt and run `vagrant up` to boot your Vagrant VM.

4. Connect to your Vagrant VM with `vagrant ssh`. If you are on Windows you can use [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/) to connect and login with username `vagrant` and password `vagrant`

Setting up the database
---------------

1. Once connected to your Vagrant VM, enter `psql` to enter the PostgreSQL command line

2. Run `CREATE DATABASE game_catalog;` to create the tournament database

3. Exit out of psql with `\q`

4. Type `python models.py` to create the database tables then `python data_fill.py` to populate the database with some neccessary data and some demo items

5. Exit out of psql with `\q`

Running the application
---------------

1. Navigate to the cloned tournament directory created from cloning this repo and run `python tournament_test.py`

2. Make note: HUGE SUCCESS

Download
-------
- [Version 1.0](https://github.com/Drkeenbean/game_tournament/master.zip)
