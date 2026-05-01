# Papatzis Spotter GUI V3 - Design Document

## 1. Vision & Purpose
To transform **Papatzis Spotter** from a diagnostic CLI tool into a **Pedagogical IDE**. The application helps users identify AI-Slop, understands the underlying patterns, and provides guidance for rewriting code with a "Human Touch".

## 2. Core Layout (T-Shape Dashboard)
The application follows an integrated dashboard layout optimized for a minimum resolution of **1280x720 (720p)**.

- **Top Navigation Bar**: Centralized menu for switching between main modules (Home, Analyze, Batch Scan, Settings).
- **Left Panel (Control Center)**: 
    - Configuration cards for analysis sensitivity.
    - Toggle switches for active analyzers.
    - Large **"RUN SCAN"** trigger button.
- **Center Panel (Interactive Editor)**:
    - High-performance `QPlainTextEdit`.
    - Line numbers and syntax highlighting.
    - **Click-to-Reveal**: Clicking on highlighted slop reveals an educational popup.
- **Right Panel (Audit Log)**:
    - Grouped list of findings categorized by "Pillars" (Naming, Structural, Statistical, GPT-Style).
    - Severity-based color coding (Red = Critical, Orange = Warning, Yellow = Info).

## 3. Concurrency & Performance
- **Multiprocessing Engine**: Utilizes `CPU_THREADS - 2` to ensure the host system remains responsive.
- **Parallel Analyzers**: Each Slop-detection module runs in its own process.
- **Async Communication**: `QThread` manages the lifecycle of the analysis pool, updating the UI via signals to prevent GUI freezing.

## 4. Educational Interaction Flow
1. **Detection**: Scan reveals problematic patterns.
2. **Review**: User clicks a finding in the list or editor.
3. **Instruction**: A popup explains:
    - **Rationale**: Why this code is considered AI-Slop (the "AI Psychology").
    - **Human Alternative**: Principles for rewriting the code to be more human and professional.
4. **Action**: User edits the code in the interactive editor.
5. **Validation**: User re-scans to verify the "Humanity Score" improvement.

## 5. Design Decisions (Log)
- **Interactive Editor**: Chosen over read-only viewer to facilitate the "Cleaning" process.
- **Integrated Dashboard**: Preferred over modular windows for a cohesive "Premium" user experience.
- **Generic Instruction Library**: Used instead of hard-coded patches to teach coding principles and avoid out-of-context fixes.
- **720p Minimum Target**: Ensures accessibility for users with older hardware ("πατάτες").

---
*Created during Brainstorming Session - May 2026*
