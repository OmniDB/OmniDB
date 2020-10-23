# OmniDB 3.0.0b

## Release Date: *October 23, 2020*

## Release Notes

- New features:
  - PostgreSQL 13 support.
  - Optional authentication method through Active Directory / LDAP.
  - OmniDB Database option, allowing PostgreSQL instead of default omnidb.db.
  - Additional monitoring units.
  - Omnis UI helper component (offering walkthroughs).
  - Graphical explain component (displaying Explain and Explain Analyze)
  - Option to share connections between OmniDB users.

- Improvements:
  - Core Changes
    - ~~Websocket~~ > Long Polling
    - Database connection reutilization
    - Shared tunnels
    - Updated python libraries (security + stability)
    - ~~Electron~~ > NWJS (New desktop technology)
  - UX/UI improvements for several elements (Connections management, Autocomplete, Global snippet panel with quick-[save/load], contextual menus).




**Full Documentation**: https://omnidb.readthedocs.io

![](https://raw.githubusercontent.com/OmniDB/doc/master/img/omnidb_3/dashboard.png)
