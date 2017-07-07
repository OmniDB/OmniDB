[![Join the chat at https://gitter.im/OmniDB/Lobby](https://img.shields.io/badge/GITTER-JOIN%20CHAT-brightgreen.svg)](https://gitter.im/OmniDB/Lobby)

# 0- OmniDB 2.0

OmniDB was completely rewritten to Python using the Django framework. Starting from version `2.0`, **OmniDB Python version** will receive new features and will be actively maintained.

The source code for the ASP.NET/C\# version is in the branch **csharp**. The next release of OmniDB C\# version is `1.7`, and it will only receive bug fixes.

Besides being written in Python, initial version of `OmniDB 2.0` contains the following main differences from the C\# version:

- Support to HTTPS;
- It allows query execution in background and cancellation through the use of *websockets*;
- Initially, only an improved support of PostgreSQL is implemented. More RDBMS support coming soon;
- There is a new `Snippet` feature.

# 1- Introduction

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

![](http://162.243.1.11/images/screenshots/screen00.png)

Technologies:

- Python (3.5+)
- Django

Supported Platforms:

- Linux
- Windows
- OS X

Supported DBMS:

- [X] PostgreSQL
- [ ] MySQL
- [ ] Oracle
- [ ] Firebird
- [ ] SQLite
- [ ] Microsoft SQL Server
- [ ] IBM DB2

# 2- Database Schema Management

OmniDB is designed for easy database management. Here are some features:

- Tree view showing database structure
  - Included structures:
    - Columns and Tables
    - Key Constraints: primary, foreign and unique
    - Index (unique and non-unique)

![](http://162.243.1.11/images/screenshots/treeview.png)

- Powerful table creation
  - Editing capabilities:
    - Tables' names
    - Columns: name, type and nullable
    - Primary keys and respective columns
    - Foreign keys with either table and reference columns, including updating rules and removal as well
    - Indexes

![](http://162.243.1.11/images/screenshots/screen05.png)

- Table editing: Edit table structure according to DBMS limitations
- Data management: Add, edit and remove records

![](http://162.243.1.11/images/screenshots/screen07.png)

- SQL Editing
  - Customizable Features:
    - Syntax highlighting for SQL
    - SQL code completion for table columns and subquery
    - Multiple themes to be selected

![](http://162.243.1.11/images/screenshots/screen06.png)

- Other features:
  - Querying organized in tables
  - DDL commands execution
  - Multiple sequenced command execution (scripts)
  - Graphs displaying tables and their relations

![](http://162.243.1.11/images/screenshots/screen02.png)

  - Graphs displaying complete ER diagram

![](http://162.243.1.11/images/screenshots/screen01.png)

# 3- Database Schema Conversion

This feature is being implemented in the Python version.
