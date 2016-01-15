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

OPTIONAL - Populate the database
-------

5. type `psql` again to get back into the PostgreSQL command line

6. type `\c game_catalog` to connect to the game_catalog database

7. type `\i game_catalog.sql` to populate the database with a bunch of demo items 

5. Exit out of psql with `\q`

Running the application
---------------

1. Navigate to the cloned directory created from cloning this repo and run `python application.py`

2. Open a web browser and navigate to [http://localhost:5000](http://localhost:5000)

2. Make note: HUGE SUCCESS. A WINNER IS YOU!
