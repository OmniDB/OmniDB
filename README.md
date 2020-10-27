# OmniDB 3.0.0 Beta

## Release Date: *October 23, 2020*

## Release Notes

- New features:
  - PostgreSQL 13 support
  - Database structure tree and Properties/DDL tabs with support to additional PostgreSQL objects
  - Option to use Active Directory / LDAP to authenticate OmniDB's users
  - Option to use PostgreSQL as OmniDB's backend database
  - Additional monitoring units
  - Omnis UI helper component (offering walkthroughs)
  - OmniDB's own graphical explain component (displaying Explain and Explain Analyze)
  - Option to share connections between OmniDB users


- Improvements:
  - Core Changes
    - ~~Websocket~~ > Long Polling
    - Better handling of database connections, reusing connection when appropriate
    - Shared tunnels
    - Updated python and javascript libraries (security + stability)
    - ~~Electron~~ > NWJS (New desktop technology)
    - Enhanced shortcuts, allowing users to maintain shortcuts per OS
  - UX/UI improvements for several elements (Connections management, Autocomplete, Global snippet panel with quick-[save/load], contextual menus).

# OmniDB 3.0.1 Beta

## Release Date: *October 26, 2020*

## Improvements

- Added snippets and custom monitoring units to the OmniDB 2 to 3 automatic migration process

OmniDB 3.0.0 only automatically migrated users and connections from 2.x. Users are encouraged to upgrade to 3.0.1, which will now migrate snippets and custom monitoring units from a previous 2.x installation

## Bug fixes

- Fixed an issue in the long polling mechanism
- Dark theme colors on autocomplete selection

**Website**: https://omnidb.org

**Full Documentation**: https://omnidb.readthedocs.io

![](https://raw.githubusercontent.com/OmniDB/doc/master/img/omnidb_3/dashboard.png)
