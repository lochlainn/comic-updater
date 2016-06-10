# cum

[![Build Status](https://travis-ci.org/Hamuko/cum.svg?branch=master)](https://travis-ci.org/Hamuko/cum)
[![codecov.io](https://img.shields.io/codecov/c/github/Hamuko/cum.svg?maxAge=2592000)](https://codecov.io/github/Hamuko/cum?branch=master)
[![PyPI](https://img.shields.io/pypi/v/cum.svg?maxAge=2592000)](https://pypi.python.org/pypi/cum)

comic updater, mangafied

## Description

cum (comic updater, mangafied) is a tool designed for automated manga downloads from various online manga aggregate sites. It is inspired by some of the popular package managers used with Linux distributions and OS X. The file naming scheme is partially based Daiz's [Manga Naming Scheme](https://gist.github.com/Daiz/bb8424cfedd0f05b7386).

## Installation

The easiest way to install the latest release of cum is by downloading and installing it from [Python Package Index](https://pypi.python.org/pypi/cum) with the command

    pip install cum

If you want to get the latest and (possibly) the greatest, you can install the master branch version with

    pip install git+https://github.com/Hamuko/cum

Users of Arch Linux can install release versions from [the AUR](https://aur.archlinux.org/packages/cum/).

Please note that cum currently requires **Python 3.3** or newer.

## Usage

To print out a list of available commands, use `cum --help`. For help with a particular command, use `cum COMMAND --help`.

### Configuration

Configuration is stored at `~/.cum/config.json` (`%APPDATA%\cum\config.json` for Windows) and overwrites the following default values. cum will not write login information supplied by the user at run-time back to the config file, but will store session cookies if any exist. Configuration can get read with the command `cum config get [SETTING]` and set using `cum config set [SETTING] [VALUE]`.

See the [Configuration](../../wiki/Configuration) wiki page for more details and available settings.

### Commands

```
alias      Assign a new alias to series.
chapters   List all chapters for a manga series.
config     Get or set configuration options.
download   Download all available chapters.
follow     Follow a series.
  --directory TEXT  Directory which download the series chapters into.
  --download        Downloads the chapters for the added follows.
  --ignore          Ignores the chapters for the added follows.
follows    List all follows.
get        Download chapters by URL or by alias:chapter.
  --directory TEXT  Directory which download chapters into.
ignore     Ignore chapters for a series.
latest     List most recent chapter addition for series.
  --relative        Uses relative times instead of absolute times.
new        List all new chapters.
open       Open the series URL in a browser.
repair-db  Runs an automated database repair.
unfollow   Unfollow manga.
unignore   Unignore chapters for a series.
update     Gather new chapters from followed series.
```

### Examples

```bash
# Update the database with possible new chapters for followed series.
$ cum update

# List all new, non-ignored chapters.
$ cum new

# Add a follow for a manga series.
$ cum follow http://bato.to/comic/_/comics/gakkou-gurashi-r9554

# Print out the chapter list for the added series.
$ cum chapters gakkou-gurashi

# Ignore the first three chapters for the added series.
$ cum ignore gakkou-gurashi 2 3 1

# Change the alias for the added series.
$ cum alias gakkou-gurashi school-live

# Download all new, non-ignored chapters for the added series using the new alias.
$ cum download school-live
```

## Supported sites

See the [Supported sites](../../wiki/Supported-sites) wiki page for details.

## Dependencies

* [alembic](https://pypi.python.org/pypi/alembic)
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [click](https://pypi.python.org/pypi/click/4.0)
* [natsort](https://pypi.python.org/pypi/natsort/4.0.3)
* [requests](https://pypi.python.org/pypi/requests/2.7.0)
* [SQLAlchemy](https://pypi.python.org/pypi/SQLAlchemy/1.0.6)

## Contribution

If you wish to contribute to cum, please consult the [Contribution Guide](CONTRIBUTING.md) first to make everything a bit easier.

## Community

There is an IRC channel for cum, `#cu` on `irc.rizon.net`, where cum development and issues are occasionally discussed.
