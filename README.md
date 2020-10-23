# OmniDB 3.0.0 Beta

## Release Date: *October 23, 2020*

## Release Notes

- New features:
  - PostgreSQL 13 support
  - Optional authentication method through Active Directory / LDAP
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


**Website**: https://omnidb.org

**Full Documentation**: https://omnidb.readthedocs.io

![](https://raw.githubusercontent.com/OmniDB/doc/master/img/omnidb_3/dashboard.png)
