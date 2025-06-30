Installation
===============
Copy the velox.tar.gz file to a convenient location and open a command prompt there.

To install, use PIP:
> python -m pip install velox.tar.gz

NOTE: You must use the full file extension to avoid getting any modules named 
Velox from the public Python repository.

Usage Overview
===============
The velox folder contains the modules for interfacing with the Velox Message Server APIs
via SCI Commands (see documentation for the Velox Integration Toolkit).

This folder contains the ``__init__.py`` file that automatically imports the correct 
module based on the version of Python running at the time. 

Your code should:
------------------

``import velox``

The __init__.py will load an SCI module appropriate for either Python 2.7+ or Python 3.5+ 
based on the version of Python being executed.

The ``velox.sci27.py`` or ``velox.sci35.py`` module will import the ``vxmessageserver.py``


