# Insapsula Cookie Generator
## What is Incapsula?
Incapsula is a antibot service. They load a JS file into the browser and collect user data.
Once they collected all the data they encrypt it and make it into a cookie to validate your session.

## How do I collect my own user data?
In the ``./Collector`` folder you can find a index.html file. Simply just open it in
your browser and you will see all your collector user data.

## How do I typecheck the code?
You need to insall mypy first.

```mypy --config-file mypy.conf --install-types main.py```

**UPDATE 03/03/23**
Currently rewriting this and adding Reese84 support. Rewrite will be in JS probably or maybe in PY with AST deobfuscation support.
