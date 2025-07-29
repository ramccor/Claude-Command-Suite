# External Agents Directory

This directory contains AI agents from external sources that have been integrated into the Claude Command Suite.

## Structure

```
external/
├── README.md (this file)
└── wshobson/
    ├── ATTRIBUTION.md
    └── [44 agent files]
```

## Usage

External agents work identically to native agents. They can be invoked by name or triggered automatically based on context.

## Contributing External Agents

When adding external agents:
1. Create a subdirectory named after the source/author
2. Include an ATTRIBUTION.md file with proper credit
3. Preserve original agent functionality
4. Update the main agents README.md

## Current Collections

- **wshobson**: 44 specialized development agents from [wshobson/agents](https://github.com/wshobson/agents)