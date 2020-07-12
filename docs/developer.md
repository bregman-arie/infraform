## Development

### Add a new platform/tool/programming language

You would like to add more supported platforms/tools to Infraform? great!
All supported platforms/tools are located in infraform/platforms directory.

Structure of a new platform:

```
execute: |
  command x
  command y
```

`execute` directive describes what to execute


### Add a new CLI sub command

If you would like to add a new CLI command like `run` or `list` follow these steps:

1. Create a new directory in infraform/cli called as the sub command. So infraform/cli/<name_of_the_sub_command>
2. Under the new directory add the following files:
  * cli.py with a main function
  * parser.py wh
