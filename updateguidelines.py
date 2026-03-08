#!/usr/bin/env python3

import argparse
import os

def readUserOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', choices=['env', 'opt'], default='env')
    parser.add_argument('--guidelines-dir', default='.ai/guidelines')
    parser.add_argument('--agents', default='all',
                        choices=['all', 'claude', 'junie', 'cursor', 'windsurf', 'copilot', 'zed'])
    parser.add_argument('-g', action='store_true')
    args = parser.parse_args()

    return {
        'source': args.source,
        'guidelines_dir': args.guidelines_dir,
        'agents': args.agents if args.agents == 'all' else [a.strip() for a in args.agents.split(',')],
        'guidelines_md': args.g,
    }


def readEnv():
    env = {}
    for filename in ['.env', '.env.local']:
        try:
            with open(filename) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, _, value = line.partition('=')
                    env[key.strip()] = value.strip()
        except FileNotFoundError:
            pass

    guidelines_dir = env.get('GUIDELINES_DIR') or '.ai/guidelines'
    agents_raw = env.get('GUIDELINES_AGENTS') or 'all'
    agents = agents_raw if agents_raw == 'all' else [a.strip() for a in agents_raw.split(',')]
    guidelines_md = env.get('GUIDELINES_MD', 'false').lower() == 'true'

    return {
        'guidelines_dir': guidelines_dir,
        'agents': agents,
        'guidelines_md': guidelines_md,
    }


def readGuidelines(options):
    complete = ""
    for root, dirs, files in os.walk(options['guidelines_dir']):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                complete += f.read()
    return complete

def writeAgentGuidelines(options, guidelinesStr):
    agent_paths = {
        'claude': 'CLAUDE.md',
        'junie': '.ai/junie.md',
        'cursor': '.cursor/rules/guidelines.md',
        'windsurf': '.windsurf/rules.md',
        'copilot': '.github/copilot-instructions.md',
        'zed': './rules/guidelines.md',
    }

    for agent, path in agent_paths.items():
        if options['agents'] == 'all' or agent in options['agents']:
            writeGuidelines(path, guidelinesStr)

    if (options['guidelines_md']):
        writeGuidelines('guidelines.md', guidelinesStr)


def writeGuidelines(path, guidelinesStr):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as f:
        f.write(guidelinesStr)

def main():
    options = readUserOptions()
    if options['source'] == 'env':
        options = readEnv()
    completeGuidelines = readGuidelines(options)
    writeAgentGuidelines(options,completeGuidelines)

if __name__ == "__main__":
    main()
