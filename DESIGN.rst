riotgear is a front-end application for interacting with `RIOT`_. The goal is to
make the lives of developers and users of `RIOT`_ easier.

Functionality of this tool includes:

 - Code (boilerplate) generation.
 - Building `RIOT`_ applications.
 - Showing statistics and analysis of builds.
 - Flashing a build on a board.
 - Interacting with a RIOT deployment

Problem
#######

The current `RIOT`_ build system, while powerful, contains a lot of hidden
features and toggles. Functionality can be hidden away behind make targets and
make variables. 

Technical Design goals
######################

Riotgear is a library with a front-end
======================================

The riotgear application is designed as a library with a simple front-end CLI
application. By ensuring that the application remains a simple front-end,
different front-ends can be developed, this also ensures that complex
orchestration platforms can use Riotgear as a library.

Riotgear is a plugin manager
============================

Riotgear is designed as a simple plugin management system. This allows for
extending the functionality with different plugins

A plugin is based on at least two classes. The class inheriting from the
``BasePluginLoader`` provides the plugin registry with the required information
to call the plugin. It should not load any external imports, the goal is that
with a base Riotgear install, all plugin loaders can be imported. A plugin
should provide an implementation in ``loader.py``

The second part is the ``BasePlugin`` itself, implemented in ``plugin.py``. This
module is only loaded when the library calls the module. At this point the code
can assume that the caller wants to use the functionality provided by the
plugin. The plugin, at this point, may load any necessary python modules,
including external modules.

.. _RIOT: https://github.com/RIOT-OS/RIOT
