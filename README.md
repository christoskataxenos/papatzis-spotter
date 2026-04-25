# Papatzis Spotter: The AI-Slop Generation Finder

![Version](https://img.shields.io/badge/version-beta-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey)

[🇬🇷 Ελληνικά](#ελληνικά) | [🇬🇧 English](#english) | [🚀 Download Beta](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/beta)

---

<a name="ελληνικά"></a>
## 🇬🇷 Ελληνικά: Το Motivation πίσω από το Project

### Από το "Vibe" στα Δεδομένα
Η ιδέα για το **Papatzis Spotter** γεννήθηκε από μια πραγματική ανάγκη για τεχνική τεκμηρίωση απέναντι στο "ψηφιακό gaslighting". 

Όλα ξεκίνησαν όταν κλήθηκα να αξιολογήσω κώδικα που παρουσιάστηκε ως "ακαδημαϊκό πρότυπο". Ως developer, παρατήρησα αμέσως την έλλειψη "ανθρώπινου αποτυπώματος":
- **Υπερβολική Φλυαρία:** Σχόλια που εξηγούσαν τα αυτονόητα με αποστειρωμένη ευγένεια.
- **Μηχανική Δομή:** Μια τέλεια αλλά "άψυχη" οργάνωση που θύμιζε default output των LLMs.

Μετά από δοκιμές στο δικό μου tech stack (local LLMs σε Proxmox server), η ετυμηγορία ήταν ομόφωνη: **High-dose AI Slop.** Το Papatzis Spotter μετατρέπει αυτή τη διαίσθηση σε **συγκεκριμένα metrics**.

---

### 🔬 Τεχνικά Χαρακτηριστικά
Ο μηχανισμός ανάλυσης "ξεκοιλιάζει" τον κώδικα μέσω AST:
- **Structural Analysis:** Εντοπισμός "LLM-isms" στη δομή.
- **Comment Analysis:** Αξιολόγηση πυκνότητας και ύφους.
- **Statistical Entropy:** Μέτρηση προβλεψιμότητας του κώδικα.
- **Naming Conventions:** Ανίχνευση μηχανικά παραγόμενων ονομάτων.

---

<a name="english"></a>
## 🇬🇧 English: Developer Motivation

### From "Vibe" to Data
**Papatzis Spotter** was built to provide technical documentation against "digital gaslighting." 

Reviewing code presented as "academic standard" revealed a clear lack of "human scent":
- **Verbosity Overload:** Sterile comments explaining the obvious.
- **Mechanical Structure:** "Soulless" organization mirroring default LLM outputs.

Verified through local LLM testing (Proxmox stack), the verdict was clear: **High-dose AI Slop.** This tool converts gut feelings into **concrete metrics**.

---

### 🛠️ Installation & Setup

#### 🚀 Automated Solution (Windows)
For a quick start, simply run:
- **`run_orchestrator.bat`**

#### 📦 Download Beta
You can find the latest portable release here:
[**Papatzis Spotter Beta Release**](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/beta)

---

### 🖥️ CLI Example Output

**Case A: Human-crafted code**
```bash
[OK] Slop Score: 12.4%
[OK] Humanity shield active.
[OK] Craftsmanship detected.
[READY] Safe for production.
```

**Case B: Detected Slop**
```bash
[FAIL] Slop Score: 98.3%
[!] Pillar: Robotic Uniformity (93.3)
[!] Finding: Architecture Overkill detected.
[STATUS] High Risk: AI-Generated Slop.
```

---
*Built to bring objectivity to code origin analysis.*
