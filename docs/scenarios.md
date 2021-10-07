## Scenarios

Scenarios are YAML based files describing what infraform should set up, configure and run. A basic scenario looks like this:

```
description: Create virtual machines
platform:    terraform
files:
 - main.tf
 - file2
```
