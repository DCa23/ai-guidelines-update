# AI Guidelines update script

Inspired by laravel boost:update command. I find it very usefull to integrate teams using multiple agents.

But sometimes you are not working with laravel, so I wanted a script to integrate a similar functionality.

## Usage

The recommended way of using it is by adding the following .env values, and just executing the script

```
# To override the directory where the team writes the guidelines
GUIDELINES_DIR=.ai/guidelines

# To specify which agents to update (comma-separated)
GUIDELINES_AGENTS=all

# To also generate a guidelines.md file
GUIDELINES_MD=true
```

Otherwise you can modify the values by adding options on the command line

```bash
# Show help
python updateguidelines.py --help

# Use CLI options instead of env file
python updateguidelines.py --source opt

# Specify guidelines directory
python updateguidelines.py --guidelines-dir .ai/guidelines

# Specify which agents to update (comma-separated)
python updateguidelines.py --agents claude,cursor

# Also generate guidelines.md
python updateguidelines.py -g
```

### Agent File Locations

The script creates guidelines files in the following locations for each agent:

| Agent | File Path |
|-------|-----------|
| Claude | `CLAUDE.md` |
| Junie | `.ai/junie.md` |
| Cursor | `.cursor/rules/guidelines.md` |
| Windsurf | `.windsurf/rules.md` |
| Copilot | `.github/copilot-instructions.md` |
| Zed | `./rules/guidelines.md` |

### How It Works

1. The script reads all markdown files from the `GUIDELINES_DIR` directory
2. It concatenates them together (separated by newlines)
3. It writes the combined guidelines to each agent's specific file location

This allows teams to maintain a single source of truth for AI agent guidelines while automatically distributing them to each agent's expected configuration location.
