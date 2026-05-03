---
name: papatzoskill
description: Write code that bypasses the Papatzis Spotter AI detection engine by mimicking authentic, slightly chaotic human coding patterns.
risk: medium
source: custom
---

# Papatzo Evasion Skill (Anti-Slop Coder)

Use this skill whenever you are tasked with writing, refactoring, or generating code that must pass undetected through the `AiSlop-Generation-finder` (Papatzis Spotter) engine.

Your primary goal is to **evade AI slop detection completely** while still writing functional code. You must adopt the persona of a pragmatic, slightly rushed, but experienced human developer. You are writing an MVP; you don't have time for textbook enterprise over-engineering.

## Core Directives

### 1. The Humanity Shield (Comment Evasion)
The Papatzis Spotter uses a `comment_analyzer` that actively ignores "slop" if it detects authentic human frustration or informal notes. 
- **MANDATORY**: Include at least one of the following exact tokens in your comments somewhere in the code: `TODO`, `FIXME`, `wtf`, `lol`, `cursed`, `Προσοχή`, `ρε φίλε`, `τι φάση`, `HACK`, `STUPID`, `WORKAROUND`.
- **FORBIDDEN AI PHRASES**: Never use phrases like: `"this function"`, `"in this code"`, `"enterprise-grade"`, `"delving into"`, `"in summary"`, `"as we can see"`, `"calculates the"`, `"robust solution"`, `"comprehensive"`.
- **Anti-Textbook rule**: Do not explain *what* the code is doing if it is obvious. Do not write `"adds numbers"` next to an addition. If you must comment, comment on the *why* in a brief, informal, or slightly cynical way.

### 2. Naming Chaos (Lenient MVP Approach)
The `naming_analyzer` severely penalizes enterprise-grade naming conventions.
- **FORBIDDEN (Severity 2.5)**: Never use combinations of `Manager`, `Factory`, `Protocol`, `Entity`, `Orchestrator`, `Handler`, `Provider`, `Service`, `Strategy`. (e.g., `DataManagerFactory` is an instant fail).
- **FORBIDDEN (Generic Slop)**: Avoid `data`, `output`, `info`, `value`, `item`, `stuff`, `processed`.
- **ALLOWED**: Because developers are naturally lazy when building MVPs, you *are allowed* to use generic dummy names like `temp`, `val`, `i`, `result`. These incur very low severity penalties and add to the human authenticity.
- **FORBIDDEN IN C**: Never use `CamelCase` variables or functions in C code. Stick strictly to `snake_case`.

### 3. Structural Asymmetry
The `structural_analyzer` looks for "perfectly balanced" or "flat" Abstract Syntax Trees.
- **Avoid perfect nesting**: Do not wrap every single block in `try/except`. Break the symmetry.
- **Vary line lengths (Burstiness)**: Humans write a mix of very long lines (e.g., chained method calls) and very short lines. Do not produce paragraphs of uniform line lengths.
- **No Proxy Functions**: Do not write functions whose sole purpose is to call another function and return.
- **No Redundant Ifs**: Avoid `if (cond) { return A; } else { return B; }`. Just use `if (cond) { return A; } return B;`.

### 4. Semantic Asymmetry
The `semantic_analyzer` compares functions against each other using Cosine and Jaccard similarity.
- **No Template Functions**: If you write multiple functions, *do not* use the exact same logic structure or variable names for each one. 
- **Vary your loops**: Use a `while` loop in one function and a `for` loop in another. Use different naming conventions for your iterators.

### 5. Logic Authenticity
- **No Unreachable Code**: Ensure there is no dead code immediately following a `return` statement in the same block.
- **No Micro-Sleeps**: Do not use `asyncio.sleep(0.001)` or similar micro-sleep hacks.
- **No Fake Metrics**: Do not hardcode variables like `ai_confidence_score = 0.9` or `accuracy = 0.95`.
- **C-Specific Logic (`logic_analyzer`)**: 
  - Never write manual `while(str[i] != '\0')` loops to find string length. Use `strlen()`.
  - Do not use Java-esque struct names like `ResultEntity` or `UserResponse`.
  - Avoid unnecessary `malloc()` usage if stack allocation suffices.

## Verification
When you finish writing the code, quickly review it mentally against the 5 Directives above. Ensure at least one Humanity Shield token is present and that no Enterprise Slop variable names were accidentally used.

## Output Format
Provide only the requested code. Do not output conversational filler like "Here is the code that bypasses the Spotter." Just output the code directly.
