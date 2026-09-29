# POODO skill package

Read SKILL.md and invoke this skill explicitly for consequential or ambiguous work. Keep references, agents, scripts and evals together when copying it into your tool's skill directory. Host capabilities and user authorization remain controlling.

Reading the skill requires no Python dependency. The optional structural validators require Python 3.9+ and PyYAML. In an isolated environment, install the adjacent requirements.txt, then run:

```sh
python scripts/validate_skill.py
python -m unittest discover -s evals -v
```

Run from this skill directory. Use the Python executable for the environment where you installed PyYAML. Scripts do not require Unix executable permissions. Capsule checks establish structure only, not truth, runtime success or model performance. Behavioral evaluation cases have not been run as part of packaging.
