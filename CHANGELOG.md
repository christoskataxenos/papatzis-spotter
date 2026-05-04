# Changelog

[English Version](#english-version) | [Ελληνική Έκδοση](#ελληνική-έκδοση)

---

<a name="english-version"></a>
## English Version

### [3.9.0] - 2026-05-04
#### Linux Distribution & Docker Optimization
- **Tauri v2 Compatibility:** Full support for Tauri v2 system dependencies on Linux (WebKitGTK 4.1 & libsoup 3.0).
- **Builder Evolution:** Upgraded persistent Docker builder image to `papatzis-builder-v2` with modern Linux headers.
- **Linux Native Support:** Enabled embedded sidecar extraction and execution for Linux environments.
- **Dynamic Permissions:** Implemented automatic executable permission setting for Linux binaries at runtime.
- **Ultra-Fast Builds:** Reduced Linux build time from 15 minutes to under 2 minutes using persistent cache.

### [3.8.0] - 2026-05-03
#### Documentation & Forensic Overhaul
- **Bilingual Support:** Full documentation available in both English and Greek.
- **Papatzis Manifesto:** Integrated the project's core philosophy and origin story.
- **Visual Forensic Guide:** Added new screenshots and side-by-side code comparisons.
- **Privacy First:** Documented the 100% offline nature and zero-API-call architecture.
- **Multithreaded Performance:** Backend scaling across CPU cores for faster local analysis.
- **Project Hardening:** Major cleanup of the repository root and archiving historical notes.

### [3.5.0] - 2026-05-01
#### Orchestrator & UI Evolution
- **Diagnostic Center:** New Laboratory section for automated testing and validation.
- **Aegean Day Theme:** High-contrast light mode for better accessibility.
- **Forensic Scoring:** Implemented exponential weighting (severity^1.4) for more accurate detection.

### [3.0.0] - 2026-04-25
#### The Engine Rebirth (V3)
- **Tauri Migration:** Transition from PyQt6 to Tauri for superior UI/UX flexibility and visualization.
- **Jaccard Similarity:** Pairwise block comparison to detect "Robotic Uniformity."
- **Entropy Analysis:** Shannon Entropy measurements to identify predictable AI output.
- **Embedded Engine:** 100% offline embedded sidecar architecture.

### [2.0.0] - 2026-04-10
#### The GUI Era (PyQt6)
- **PyQt6 GUI:** First graphical interface version, moving away from the terminal.
- **Radar Visualization:** Introduction of radar charts for visual slop diagnostics.
- **Batch Processing:** Capability to scan entire directories and generate aggregated reports.

### [1.0.0] - 2026-03-20
#### The CLI Foundation
- **Static Analysis:** First stable version of the pattern-matching detection engine.
- **Local LLM Testing:** Hardened through extensive testing using local Proxmox-hosted LLMs.

### [0.1.0] - 2026-03-05
#### The Spark (Prototype)
- **Initial Prototype:** Concept script born from "technical gaslighting" observations.
- **Boilerplate Fingerprinting:** Discovery of AI's obsession with enterprise-style boilerplate.

---

<a name="ελληνική-έκδοση"></a>
## Ελληνική Έκδοση

### [3.9.0] - 2026-05-04
#### Linux Distribution & Docker Optimization
- **Tauri v2 Compatibility:** Πλήρης συμβατότητα με Tauri v2 system libraries (WebKitGTK 4.1 & libsoup 3.0).
- **Builder Evolution:** Αναβάθμιση του persistent Docker image σε `papatzis-builder-v2` για απροβλημάτιστο compilation.
- **Linux Native Support:** Υποστήριξη για extraction και εκτέλεση της μηχανής Papatzis σε Linux.
- **Dynamic Permissions:** Αυτόματη ρύθμιση δικαιωμάτων εκτέλεσης (chmod +x) στα Linux binaries κατά το runtime.
- **Ultra-Fast Builds:** Μείωση χρόνου build για Linux από 15 λεπτά σε λιγότερο από 2 λεπτά μέσω persistent caching.

### [3.8.0] - 2026-05-03
#### Αναβάθμιση Documentation & Ιατροδικαστικής
- **Δίγλωσση Υποστήριξη:** Πλήρης τεκμηρίωση σε Αγγλικά και Ελληνικά.
- **Papatzis Manifesto:** Ενσωμάτωση της φιλοσοφίας και της ιστορίας γέννησης του project.
- **Οπτικός Οδηγός:** Νέα screenshots και συγκρίσεις κώδικα (AI Slop vs. Human Logic).
- **Ιδιωτικότητα:** Τεκμηρίωση της 100% offline λειτουργίας χωρίς χρήση AI APIs.
- **Ταχύτητα Multithreading:** Αξιοποίηση όλων των πυρήνων του επεξεργαστή για ταχύτατη τοπική ανάλυση.
- **Καθαρισμός Project:** Νοικοκύρεμα του κεντρικού φακέλου και αρχειοθέτηση παλαιότερων σημειώσεων.

### [3.5.0] - 2026-05-01
#### Εξέλιξη Orchestrator & UI
- **Διαγνωστικό Κέντρο:** Νέα ενότητα Laboratory για αυτοματοποιημένα unit tests και batch validation.
- **Aegean Day Theme:** Light mode υψηλής αντίθεσης για καλύτερη ορατότητα.
- **Forensic Scoring:** Νέος αλγόριθμος βαθμολόγησης (severity^1.4) για ακριβέστερο εντοπισμό μοτίβων AI.

### [3.0.0] - 2026-04-25
#### Η Αναγέννηση της Μηχανής V3
- **Μετάβαση σε Tauri:** Μεταφορά από PyQt6 σε Tauri για μεγαλύτερη ευελιξία κινήσεων και προηγμένα γραφικά.
- **Jaccard Similarity:** Συγκριτική ανάλυση blocks για τον εντοπισμό "Ρομποτικής Ομοιομορφίας".
- **Entropy Analysis:** Μέτρηση εντροπίας Shannon για τον εντοπισμό προβλέψιμου κώδικα AI.
- **Embedded Engine:** Πλήρως offline αρχιτεκτονική (embedded sidecar).

### [2.0.0] - 2026-04-10
#### Η Εποχή του UI (PyQt6)
- **PyQt6 GUI:** Η πρώτη έκδοση με γραφικό περιβάλλον (PyQt6), αφήνοντας πίσω το terminal.
- **Radar Visualization:** Εισαγωγή radar charts για οπτική διάγνωση του slop.
- **Μαζική Σάρωση:** Δυνατότητα ελέγχου ολόκληρων φακέλων και έκδοσης συγκεντρτικών reports.

### [1.0.0] - 2026-03-20
#### Θεμελίωση CLI
- **Στατική Ανάλυση:** Πρώτη σταθερή έκδοση της μηχανής ανίχνευσης βάσει patterns.
- **Local LLM Testing:** Θωράκιση μέσω εκτεταμένων δοκιμών σε local LLMs (Proxmox server).

### [0.1.0] - 2026-03-05
#### Η Σπίθα (Πρωτότυπο)
- **Πρωτότυπο:** Αρχικό script που γεννήθηκε από την ανάγκη ξεσκεπάσματος της "ψηφιακής παπατζιάς".
- **Boilerplate Fingerprinting:** Εντοπισμός της εμμονής της AI με τον enterprise-style boilerplate κώδικα.

---
*Papatzis Spotter — Evolution of Objectivity.*
