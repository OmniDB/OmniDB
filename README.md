## Next Release: *2.14.0 - February 14, 2019*

# OmniDB 2.13.0

## Release Date: *December 20, 2018*

## Release Notes

- New features:
  - Connection Groups: allow users to, for example, easily distinct Production and Test database servers
  - User and connection management via omnidb-config CLI utility, which helps with automated deploying
- Improvements:
  - Advanced Object Search now considers view and materialized view definition
  - Show trigger function when expanding the trigger node in the tree view
  - PostgreSQL: Improved \h command, which provides syntax help on SQL commands
  - Linux: OmniDB systemd service now uses configuration file in /etc/omnidb.conf
  - Converted all OmniDB users passwords into hashes in the OmniDB user database, improving security
  - OmniDB upgrade procedure now takes a backup of the user database (file omnidb.db)
  - Autocommit is now always enabled on Oracle/MySQL/MariaDB
  - User won't need to execute query again after password expiration / re-validation
  - OmniDB debugger plugin for PostgreSQL 11 for FreeBSD
- Bug fixes:
  - Fixed: Click index with WHERE clause: "Can only transpose a table with a single row"
  - Fixed: Export to XLSX/CSV does not consider all rows
  - Fixed: Error closing error window
  - Fixed: Monitoring Dashboard: Column widths are not adjusted when the monitoring tab doesn't have focus
  - Fixed: User Mapping is not being shown in the tree if there are no options
  - Fixed: Foreign Table DDL not being shown correctly if there are no options
  - Fixed: DDL for functions and procedures do not show a necessary comma after function body


# 1- Installation

## 1.1- Installation packages

Just go to [omnidb.org](https://omnidb.org), download the appropriate file for your
operating system and architecture and install it.

## 1.2- From source

### 1.2.1- On Debian >= 9 with `pip`

```
sudo apt install python3-pip
pip3 install pip --upgrade
pip3 install -r requirements.txt
```

### 1.2.2- On Debian/Ubuntu using `PyEnv`

```
sudo apt install git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.5.2
cd OMNIDB_FOLDER
pyenv local 3.5.2

pip install pip --upgrade
pip install -r requirements.txt
```

## 1.3- Running OmniDB

Download or clone OmniDB repo and extract it somewhere. To start Django server, enter into `OmniDB/OmniDB` folder and type:

```
python omnidb-server.py
```

# 2- Introduction

**OmniDB** is a web tool that simplifies database management focusing on interactivity, designed to be powerful and lightweight. Check-out some characteristics:

- **Web Tool**: Accessible from any platform, using a browser as a medium
- **Responsive Interface**: All available functions in a single page
- **Unified Workspace**: Different technologies managed in a single workspace
- **Simplified Editing**: Easy to add and remove connections
- **Safety**: Multi-user support with encrypted personal information
- **Interactive Tables**: All functionalities use interactive tables, allowing copying and pasting in blocks
- **Smart SQL Editor**: Contextual SQL code completion
- **Beautiful SQL Editor**: You can choose between many available color themes
- **Tabbed SQL Editor**: Easily add, rename or delete editor tabs

![](https://omnidb.org/images/screenshots/screen00.png)

Technologies:

- Python (3.5+)
- Django

Supported Platforms:

- Linux
- Windows
- OS X

Supported DBMS:

- [X] PostgreSQL
- [X] Oracle
- [X] MySQL / MariaDB
- [ ] Firebird
- [ ] SQLite
- [ ] Microsoft SQL Server
- [ ] IBM DB2

# 3- Database Schema Management

OmniDB is designed for easy database management. Here are some features:

- Tree view showing database structure

![](https://omnidb.org/images/screenshots/treeview.png)

- Powerful table creation
  - Editing capabilities:
    - Tables' names
    - Columns: name, type and nullable
    - Primary keys and respective columns
    - Foreign keys with either table and reference columns, including updating rules and removal as well
    - Indexes

![](https://omnidb.org/images/screenshots/screen05.png)

- Table editing: Edit table structure according to DBMS limitations
- Data management: Add, edit and remove records

![](https://omnidb.org/images/screenshots/screen07.png)

- SQL Editing
  - Syntax highlighting for SQL
  - SQL code completion for table columns and subquery
  - Multiple themes to be selected

![](https://omnidb.org/images/screenshots/screen06.png)

- Support for external tools:
  - [pglogical](https://www.2ndquadrant.com/en/resources/pglogical/)
  - [Postgres-BDR](https://www.2ndquadrant.com/en/resources/bdr/)
  - [Postgres-XL](https://www.2ndquadrant.com/en/resources/postgres-xl/)


- Other features:
  - Querying organized in tables
  - DDL commands execution
  - SQL history
  - Graphs displaying tables and their relations

![](https://omnidb.org/images/screenshots/screen02.png)

  - Graphs displaying complete ER diagram

![](https://omnidb.org/images/screenshots/screen01.png)

  - Visualization of explain plan

![](https://omnidb.org/images/screenshots/execution_plan.png)

  - PL/pgSQL function debugger (requires a plugin, please see [here](https://github.com/OmniDB/OmniDB/blob/master/omnidb_plugin/README.md))

![](https://omnidb.org/images/screenshots/debugger.png)

  - Monitoring dashboard

![](https://omnidb.org/images/screenshots/monitoring_dashboard.png)
