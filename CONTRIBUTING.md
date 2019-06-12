# Contributing to OmniDB

We love your input! We want to make contributing to this project as easy and
transparent as possible, whether it's:

- Reporting a bug
- Asking questions
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer


## OmniDB Database Support

Currently OmniDB supports `PostgreSQL`, `Oracle`, `MySQL` and `MariaDB`. We plan
to support `Firebird`, `MSSQL Server`, `SQLite` and `IBM DB2` in the foreseeable
future. Suggestions and even pull requests for other databases are welcome.


## OmniDB Operating System Support

We currently build OmniDB for Debian, CentOS, Windows and OSX. Deployment for
different Linux distributions such as openSUSE, Arch Linux, Gentoo and RaspBian
is in our roadmap, but it requires time. You can suggest other operating systems
or architectures and even perform pull requests, we will appreciate that.


## OmniDB Repositories

- [https://github.com/OmniDB/OmniDB](https://github.com/OmniDB/OmniDB): Main
application and server, deployment scripts and tests.
- [https://github.com/OmniDB/doc](https://github.com/OmniDB/doc): OmniDB
documentation.
- [https://github.com/OmniDB/monitors](https://github.com/OmniDB/monitors)
Monitors (charts, grids) for the Monitoring Dashboard.
- [https://github.com/OmniDB/plugins](https://github.com/OmniDB/plugins): OmniDB
official plugins.


## We Develop with Github

We use GitHub to host code, to track issues and feature requests, as well as
accept pull requests.

1. Fork the repo.
2. Checkout `dev` branch.
3. If you've added code that should be tested, add tests.
4. If you've changed APIs, update the documentation.
5. Ensure the test suite passes.
5. Issue that pull request to the `dev` branch.

Note that the `dev` branch is only used in the main repo. For other repos, issue
your pull request to the `master` branch.


## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be
under the same [MIT License](http://choosealicense.com/licenses/mit/) that
covers the project. Feel free to contact the maintainers if that's a concern.


## Report bugs using Github's [issues](https://github.com/OmniDB/OmniDB/issues)

We use GitHub issues to track public bugs. Report a bug by
[opening a new issue](https://github.com/OmniDB/OmniDB/issues/new); it's that
easy!


## Write bug reports with detail

**Great Bug Reports** tend to have:

- A quick summary and/or background
- OmniDB flavor you are using (app or server) and version
- Operating system and version
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)
