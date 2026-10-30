# Security reporting

Report suspected vulnerabilities privately to [craig@nh3.biz](mailto:craig@nh3.biz).
Do not put exploit details, credentials, personal data or private archives in
public issues or pull requests. Use synthetic data and an environment you own or
are authorized to assess.

Useful report information includes:

- The affected version or full commit ID and component.
- Minimal reproduction steps, environment and expected versus actual behavior.
- The security impact and any suggested mitigation.

This policy covers the harness repository. It does not authorize testing SWG
Source services, game servers or other third-party systems. For ordinary bugs
without sensitive security implications, use [Issues](https://github.com/Akilleez-QA/swg-source-harness/issues).

As described in [README.md](README.md), local reports are unsigned, never grant
review eligibility and do not authenticate contributor claims. The CLI does not
execute submitted test commands. Git inspection is not a sandbox for hostile
repositories. Keep these boundaries intact when assessing or reporting a problem.

This policy promises no supported-version window, response deadline or bounty.
Include the exact affected revision rather than assuming a release is supported.
