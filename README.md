# OmniDB 3.0.3 Beta

## Release Date: *December 17, 2020*

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

- 3.0.1 changes
  - Bug Fixes
    - Fixed an issue in the long polling mechanism
    - Dark theme colors on autocomplete selection
  - Improvements
    - Added snippets and custom monitoring units to the OmniDB 2 to 3 automatic migration process

- 3.0.2 changes
  - Re-included
    - Explain visualizer component from OmniDB 2.x
    - Shortcuts for issueing Explain and Explain Analyze
  - Bug Fixes
    - Fixed missing dark theme colors on connection results when in full-view
    - Fixed conflict between the z-index of the new explain visualizer and the database tree context menus
  - Improvements
    - Added a toggle to switch between the old and new explain components
    - Improved client-side CPU usage performance (browser rendering gpu-intensive processes)
    - Added a new node-spin loading icon for dark themes with improved visibility

- 3.0.3 changes
  - Bug Fixes
    - Query Tab: Fixed editor key behaviours related to up/down arrows (skipping rows, text selection, text shifting, text indenting)
    - Console Tab: Fixed issue describe command for tables in PostgreSQL 12+
    - Console Tab: Fixed background theme color on console output when changing themes
  - Improvements
    - Reduced chances of having OmniDB being flagged as a threat by security tools (false-positives)
    - Outer Menu: Improved layout and behaviour, providing better awareness of the context
    - Result Grid: Improved resizing behaviours
    - Added password option on --createconnection



**Website**: https://omnidb.org

**Full Documentation**: https://omnidb.readthedocs.io

![](https://raw.githubusercontent.com/OmniDB/doc/master/img/omnidb_3/dashboard.png)
