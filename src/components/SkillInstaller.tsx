import React, { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { translations, Language } from '../lib/i18n';
import { Shield, FolderDown, Globe, GitBranch } from 'lucide-react';
import { homeDir, join } from '@tauri-apps/api/path';
import { mkdir, writeTextFile, exists } from '@tauri-apps/plugin-fs';
import { open } from '@tauri-apps/plugin-dialog';

const PAPATZOSKILL_CONTENT = `---
name: papatzoskill
description: Write code that bypasses the Papatzis Spotter AI detection engine by mimicking authentic, slightly chaotic human coding patterns.
risk: medium
source: custom
---

# Papatzo Evasion Skill (Anti-Slop Coder)

Use this skill whenever you are tasked with writing, refactoring, or generating code that must pass undetected through the \`AiSlop-Generation-finder\` (Papatzis Spotter) engine.

Your primary goal is to **evade AI slop detection completely** while still writing functional code. You must adopt the persona of a pragmatic, slightly rushed, but experienced human developer. You are writing an MVP; you don't have time for textbook enterprise over-engineering.

## Core Directives

### 1. The Humanity Shield (Comment Evasion)
The Papatzis Spotter uses a \`comment_analyzer\` that actively ignores "slop" if it detects authentic human frustration or informal notes. 
- **MANDATORY**: Include at least one of the following exact tokens in your comments somewhere in the code: \`TODO\`, \`FIXME\`, \`wtf\`, \`lol\`, \`cursed\`, \`Προσοχή\`, \`ρε φίλε\`, \`τι φάση\`, \`HACK\`, \`STUPID\`, \`WORKAROUND\`.
- **FORBIDDEN AI PHRASES**: Never use phrases like: \`"this function"\`, \`"in this code"\`, \`"enterprise-grade"\`, \`"delving into"\`, \`"in summary"\`, \`"as we can see"\`, \`"calculates the"\`, \`"robust solution"\`, \`"comprehensive"\`.
- **Anti-Textbook rule**: Do not explain *what* the code is doing if it is obvious. Do not write \`"adds numbers"\` next to an addition. If you must comment, comment on the *why* in a brief, informal, or slightly cynical way.

### 2. Naming Chaos (Lenient MVP Approach)
The \`naming_analyzer\` severely penalizes enterprise-grade naming conventions.
- **FORBIDDEN (Severity 2.5)**: Never use combinations of \`Manager\`, \`Factory\`, \`Protocol\`, \`Entity\`, \`Orchestrator\`, \`Handler\`, \`Provider\`, \`Service\`, \`Strategy\`. (e.g., \`DataManagerFactory\` is an instant fail).
- **FORBIDDEN (Generic Slop)**: Avoid \`data\`, \`output\`, \`info\`, \`value\`, \`item\`, \`stuff\`, \`processed\`.
- **ALLOWED**: Because developers are naturally lazy when building MVPs, you *are allowed* to use generic dummy names like \`temp\`, \`val\`, \`i\`, \`result\`. These incur very low severity penalties and add to the human authenticity.
- **FORBIDDEN IN C**: Never use \`CamelCase\` variables or functions in C code. Stick strictly to \`snake_case\`.

### 3. Structural Asymmetry
The \`structural_analyzer\` looks for "perfectly balanced" or "flat" Abstract Syntax Trees.
- **Avoid perfect nesting**: Do not wrap every single block in \`try/except\`. Break the symmetry.
- **Vary line lengths (Burstiness)**: Humans write a mix of very long lines (e.g., chained method calls) and very short lines. Do not produce paragraphs of uniform line lengths.
- **No Proxy Functions**: Do not write functions whose sole purpose is to call another function and return.
- **No Redundant Ifs**: Avoid \`if (cond) { return A; } else { return B; }\`. Just use \`if (cond) { return A; } return B;\`.

### 4. Semantic Asymmetry
The \`semantic_analyzer\` compares functions against each other using Cosine and Jaccard similarity.
- **No Template Functions**: If you write multiple functions, *do not* use the exact same logic structure or variable names for each one. 
- **Vary your loops**: Use a \`while\` loop in one function and a \`for\` loop in another. Use different naming conventions for your iterators.

### 5. Logic Authenticity
- **No Unreachable Code**: Ensure there is no dead code immediately following a \`return\` statement in the same block.
- **No Micro-Sleeps**: Do not use \`asyncio.sleep(0.001)\` or similar micro-sleep hacks.
- **No Fake Metrics**: Do not hardcode variables like \`ai_confidence_score = 0.9\` or \`accuracy = 0.95\`.
- **C-Specific Logic (\`logic_analyzer\`)**: 
  - Never write manual \`while(str[i] != '\\0')\` loops to find string length. Use \`strlen()\`.
  - Do not use Java-esque struct names like \`ResultEntity\` or \`UserResponse\`.
  - Avoid unnecessary \`malloc()\` usage if stack allocation suffices.

## Verification
When you finish writing the code, quickly review it mentally against the 5 Directives above. Ensure at least one Humanity Shield token is present and that no Enterprise Slop variable names were accidentally used.

## Output Format
Provide only the requested code. Do not output conversational filler like "Here is the code that bypasses the Spotter." Just output the code directly.
`;

const GIT_BOUNCER_CONTENT = `#!/bin/bash
# Papatzis Spotter - Git Bouncer (Pre-commit hook)
#
# Blocks commits if the Papatzis Spotter AI Slop Score exceeds the limit.
# Ensure that python and the AiSlop-Generation-finder directory are available.

THRESHOLD=15.0
SPOTTER_PATH="C:/Users/chris/Documents/GitHub/AiSlop-Generation-finder/analyzer/slop_engine.py" # Adjust if necessary

echo "🔎 [Git Bouncer] Papatzis Spotter is scanning your staged files..."

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(py|c|h|java|js|ts|tsx|jsx|cpp|cs)$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

for FILE in $STAGED_FILES; do
    if [ ! -f "$FILE" ]; then continue; fi

    # We assume slop_engine.py can be called via python and returns "[FAIL]" if it detects slop
    # For a real implementation, you might want to parse the JSON output of the engine.
    OUTPUT=$(python "$SPOTTER_PATH" "$FILE" 2>/dev/null)
    
    if echo "$OUTPUT" | grep -q "FAIL"; then
        echo "❌ [Git Bouncer] Slop detected in $FILE!"
        echo "$OUTPUT"
        echo "Commit blocked. Use humanity shield or rewrite the code."
        exit 1
    fi
done

echo "✅ [Git Bouncer] Code is clean. Proceeding with commit."
exit 0
`;

interface SkillInstallerProps {
  lang: Language;
}

export const SkillInstaller: React.FC<SkillInstallerProps> = ({ lang }) => {
  const { addToast } = useAppStore();
  const t = translations[lang];
  const [loading, setLoading] = useState(false);

  const installGlobal = async () => {
    setLoading(true);
    try {
      const home = await homeDir();
      
      const targets = [
        { dir: await join(home, '.gemini', 'antigravity', 'skills', 'papatzoskill'), file: 'SKILL.md' },
        { dir: await join(home, '.claude', 'skills'), file: 'papatzoskill.md' },
        { dir: await join(home, '.codeium', 'windsurf', 'rules'), file: 'papatzoskill.md' },
        { dir: await join(home, '.config', 'ai-agents'), file: 'papatzoskill.md' },
      ];

      for (const target of targets) {
        if (!(await exists(target.dir))) {
          await mkdir(target.dir, { recursive: true });
        }
        await writeTextFile(await join(target.dir, target.file), PAPATZOSKILL_CONTENT);
      }
      
      addToast(t.installedSuccess, 'success');
    } catch (e: any) {
      addToast(t.installedFailed + ': ' + e.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const installLocal = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: t.selectProjectFolder
      });
      
      if (!selected) return;
      const projectPath = selected as string;
      setLoading(true);

      const targets = [
        { dir: await join(projectPath, '.cursor', 'rules'), file: 'papatzoskill.mdc' },
        { dir: await join(projectPath, '.windsurf', 'rules'), file: 'papatzoskill.md' },
        { dir: await join(projectPath, '.claude', 'skills'), file: 'papatzoskill.md' }
      ];

      for (const target of targets) {
        if (!(await exists(target.dir))) {
          await mkdir(target.dir, { recursive: true });
        }
        await writeTextFile(await join(target.dir, target.file), PAPATZOSKILL_CONTENT);
      }
      
      addToast(t.installedSuccess, 'success');
    } catch (e: any) {
      addToast(t.installedFailed + ': ' + e.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const installGitBouncer = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: t.selectProjectFolder
      });
      
      if (!selected) return;
      const projectPath = selected as string;
      setLoading(true);

      const hooksDir = await join(projectPath, '.git', 'hooks');
      
      if (!(await exists(hooksDir))) {
        await mkdir(hooksDir, { recursive: true });
      }
      
      await writeTextFile(await join(hooksDir, 'pre-commit'), GIT_BOUNCER_CONTENT);
      
      addToast(t.installedSuccess, 'success');
    } catch (e: any) {
      addToast(t.installedFailed + ': ' + e.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 relative">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <div className="flex items-center space-x-4 mb-8">
          <div className="w-12 h-12 bg-accent-primary/10 border border-accent-primary/20 rounded-xl flex items-center justify-center">
            <Shield className="text-accent-primary" size={24} strokeWidth={1.5} />
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-wide text-text-primary uppercase">{t.evasionTitle}</h1>
            <p className="text-text-secondary text-sm">{t.evasionDesc}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Global Install */}
          <div className="bg-surface-elevated border border-border-default rounded-xl p-6 hover:border-accent-primary/30 transition-colors">
            <Globe className="text-accent-primary mb-4" size={32} strokeWidth={1.5} />
            <h3 className="text-lg font-bold mb-2 text-text-primary">{t.installGlobal}</h3>
            <p className="text-sm text-text-secondary mb-6 h-12">
              Installs Papatzoskill globally to Antigravity, Claude Code, Windsurf, and default agent config folders.
            </p>
            <button 
              onClick={installGlobal}
              disabled={loading}
              className="w-full py-3 bg-accent-primary/10 text-accent-primary rounded-lg font-bold hover:bg-accent-primary hover:text-white transition-colors"
            >
              {loading ? t.installing : t.installGlobal}
            </button>
          </div>

          {/* Local Install */}
          <div className="bg-surface-elevated border border-border-default rounded-xl p-6 hover:border-accent-primary/30 transition-colors">
            <FolderDown className="text-accent-primary mb-4" size={32} strokeWidth={1.5} />
            <h3 className="text-lg font-bold mb-2 text-text-primary">{t.installLocal}</h3>
            <p className="text-sm text-text-secondary mb-6 h-12">
              Installs Papatzoskill locally to a specific project (.cursorrules, .windsurf, .claude/skills).
            </p>
            <button 
              onClick={installLocal}
              disabled={loading}
              className="w-full py-3 bg-surface border border-border-strong text-text-primary rounded-lg font-bold hover:border-accent-primary transition-colors"
            >
              {loading ? t.installing : t.installLocal}
            </button>
          </div>

          {/* Git Bouncer */}
          <div className="bg-surface-elevated border border-border-default rounded-xl p-6 hover:border-[#F43F5E]/30 transition-colors md:col-span-2">
            <div className="flex items-start space-x-4">
              <div className="p-3 bg-[#F43F5E]/10 rounded-lg shrink-0">
                <GitBranch className="text-[#F43F5E]" size={28} strokeWidth={1.5} />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold mb-2 text-text-primary">{t.installGitBouncer}</h3>
                <p className="text-sm text-text-secondary mb-4">
                  {t.gitBouncerDesc} Installs a <code>pre-commit</code> hook to the selected repository.
                </p>
                <button 
                  onClick={installGitBouncer}
                  disabled={loading}
                  className="px-6 py-3 bg-[#F43F5E]/10 border border-[#F43F5E]/20 text-[#F43F5E] rounded-lg font-bold hover:bg-[#F43F5E] hover:text-white transition-colors"
                >
                  {loading ? t.installing : t.installGitBouncer}
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
