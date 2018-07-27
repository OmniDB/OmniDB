## Next Release: *2.11.0 - August 16, 2018*

# OmniDB 2.10.0

## Release Date: *July 26, 2018*

## Release Notes

- New feature:
  - Support to Foreign Data Wrappers, Foreign Servers, User Mappings and Foreign Tables (PostgreSQL)
- Improvements:
  - Monitoring Dashboard: Save current chart disposition per connection
  - Monitoring Dashboard: Monitoring units that require plpythonu no longer have this requirement (PostgreSQL)
  - Monitoring Dashboard: Improved current charts and added new ones (PostgreSQL)
  - Renamed "Data Mining" feature with "Advanced Object Search" (PostgreSQL)
  - Advanced Object Search: Only shows a line when finds something, does not show "No match" (PostgreSQL)
- Bug fixes:
  - Fixed "Failed to find conversion function from unknown to regprocedure" (PostgreSQL, [#591](https://github.com/OmniDB/OmniDB/issues/591))
  - Fixed "Unsupported regnamespace type" (PostgreSQL, [#605](https://github.com/OmniDB/OmniDB/issues/605))
  - Fixed "Object object" error message when using Query Data (Oracle, [#611](https://github.com/OmniDB/OmniDB/issues/611))

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
