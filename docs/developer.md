## Development

### Add a new platform/tool/programming language

All supported platforms are located in infraform/platforms directory and this where you should add any new tool/platform support.
Each platform has the following files in that directory:

1. infraform/platforms/<name>.py - The class of the platform that must inherit from Platform class (defined in platform.py)
2. infraform/platforms/vars/<name>.py - The variables of the platform. Variables like:
  * RUN - how to make use of the platform / run it
  * READINESS_CHECK - how to check if the host has the platform and ready to make use of it
  * REMOVE - how to undo/delete platform's output/result
  * PACKAGE - which packages install the platform
  * BINARY - what is the binary of the platform

### Add a new CLI sub command

If you would like to add a new CLI command like `run` or `list` follow these steps:

1. Create a new directory in infraform/cli called as the sub command. So infraform/cli/<name_of_the_sub_command>
2. Under the new directory add the following files:
  * cli.py with a main function
  * parser.py which defines the arguments supported by the sub command

### Adding a scenario

A scenario can be:

1. A File that ends with .ifr suffix
2. An entire directory which still has to include .ifr file and the directory has to be named exactly as the scenario

Structure of a new scenario

```
execute: |
  command x
  command y
```

`execute` directive describes what to execute
