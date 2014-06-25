Read Yaml based configuration files.
====================================

This module provides a Config class and a load function as an alternate API to
create and itinitialize it from a Yaml config file. The confile file format
supports importing environment variables, defining local variables, and also
optionally exporting variables to the environment. Simple string based variable
substitution is also supported.

This module is meant to be imported into the target application, but can also
be run as a script to read and print the config file.

Classes:

    Config

Functions:

    load_yaml(file_name) -> object

Yaml config file example:
----------------------------------------
    import:
    - HOME
    - PATH

    local:
    - APP_VERSION : "0.7"
    - APP_PATH    : "{HOME}/myapp-{APP_VERSION}/bin"

    export:
    - PATH : "{PATH}:{APP_PATH}"

License
-------
Copyright (c) 2013 Rohit Rathi &lt;rrathi.appdev@gmail.com&gt;

config-utils is provided under the MIT License. See the `LICENSE` file for details.
