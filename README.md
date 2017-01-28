[![Join the chat at https://gitter.im/OmniDB/Lobby](https://img.shields.io/badge/GITTER-JOIN%20CHAT-brightgreen.svg)](https://gitter.im/OmniDB/Lobby)

# Introduction

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

![](http://www.omnidb.com.br/images_article/topo.png)

Technologies:

- ASP.NET
- C#
- HTML + CSS + JavaScript

Supported Platforms:

- Linux
- Windows
- OS X

Supported DBMS:

- MySQL
- Oracle
- PostgreSQL
- Firebird
- SQLite
- Microsoft SQL Server
- Microsoft Access
- Microsoft SQL Compact (Windows only)

# Database Schema Management

OmniDB is designed for easy database management. Here are some features:

- Tree view showing database structure
  - Included structures:
    - Columns and Tables
    - Key Constraints: primary, foreign and unique
    - Index (unique and non-unique)

![](http://www.omnidb.com.br/images_article/image_6_01.png)

- Powerful table creation
  - Editing capabilities:
    - Tables' names
    - Columns: name, type and nullable
    - Primary keys and respective columns
    - Foreign keys with either table and reference columns, including updating rules and removal as well
    - Indexes

![](http://www.omnidb.com.br/images_article/image_5_05.png)
![](http://www.omnidb.com.br/images_article/image_5_06.png)

- Table editing: Edit table structure according to DBMS limitations
- Data management: Add, edit and remove records

![](http://www.omnidb.com.br/images_article/image_7_04.png)

- SQL Editing
  - Customizable Features:
    - Syntax highlighting for SQL
    - SQL code completion for table columns and subquery
    - Multiple themes to be selected

![](http://www.omnidb.com.br/images_article/image_8_02.png)

- Other features:
  - Querying organized in tables
  - DDL commands execution
  - Multiple sequenced command execution (scripts)
  - Bar charts demonstrating registry numbers contained in the denser tables (limited to 100)
  - Graphs displaying tables and their relations
  - Graphs displaying tables, relations and color scale based on record density

![](http://www.omnidb.com.br/images_article/image_9_06.png)

  - Graphs displaying complete ER diagram

![](http://www.omnidb.com.br/images_article/image_9_09.png)

# Database Schema Conversion

Since version 1.3, OmniDB is able to convert one schema to another, regardless of the DBMS. It is very useful to convert databases, from any supported DBMS to any supported DBMS.

Here are the structures supported by OmniDB database conversion:

- Tables
- Primary Keys
- Foreign Keys
- Uniques
- Indexes
- Table data

![](http://www.omnidb.com.br/images_article/image_10_03.png)
![](http://www.omnidb.com.br/images_article/image_10_06.png)
