# Papatzis Spotter
## The Offline AI-Slop Detection Engine

[![](https://img.shields.io/badge/version-stable-2F5C8F?style=for-the-badge)](https://github.com/christoskataxenos/papatzis-spotter/releases)
[![](https://img.shields.io/badge/license-MIT-333333?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/badge/python-3.10%2B-2F5C8F?style=for-the-badge)](https://python.org)
[![](https://img.shields.io/badge/platform-windows%20%7C%20linux-333333?style=for-the-badge)](https://github.com/christoskataxenos/papatzis-spotter)

---

### [ Ελληνικά ](#ελληνικά) | [ English ](#english) | [ Download Stable ](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/stable_release)

---

<a name="ελληνικά"></a>
## Το Motivation πίσω από το Project

### Από το "Vibe" στα Δεδομένα
Η ιδέα για το **Papatzis Spotter** γεννήθηκε από μια πραγματική ανάγκη για τεχνική τεκμηρίωση απέναντι στο "ψηφιακό gaslighting". 

Όλα ξεκίνησαν όταν κλήθηκα να αξιολογήσω κώδικα που παρουσιάστηκε ως "ακαδημαϊκό πρότυπο". Ως developer, παρατήρησα αμέσως την έλλειψη "ανθρώπινου αποτυπώματος":
- **Υπερβολική Φλυαρία:** Σχόλια που εξηγούσαν τα αυτονόητα με αποστειρωμένη ευγένεια.
- **Μηχανική Δομή:** Μια τέλεια αλλά "άψυχη" οργάνωση που θύμιζε default output των LLMs.

Μετά από δοκιμές σε τοπικό tech stack (local LLMs σε Proxmox server), η ετυμηγορία ήταν ομόφωνη: **High-dose AI Slop.** Το Papatzis Spotter μετατρέπει αυτή τη διαίσθηση σε **συγκεκριμένα metrics**.

---

## Technical Architecture

Ο μηχανισμός ανάλυσης "ξεκοιλιάζει" τον κώδικα μέσω AST (Abstract Syntax Tree) και στατιστικών μοντέλων:

| Pillar | Description | Detection Logic |
| :--- | :--- | :--- |
| **Structural Analysis** | Σκελετός Λογικής | Εντοπισμός LLM-isms στη δομή και την ιεραρχία. |
| **Comment Analysis** | Πιστότητα Ύφους | Αξιολόγηση πυκνότητας, ύφους και "robotic" ευγένειας. |
| **Statistical Entropy** | Προβλεψιμότητα | Μέτρηση της στατιστικής εντροπίας (το AI είναι υπερβολικά ομοιόμορφο). |
| **Naming Conventions** | Μηχανική Ονοματολογία | Ανίχνευση ονομάτων που παράγονται από heuristics μηχανών. |

---

<a name="english"></a>
## Developer Motivation (EN)

### From "Vibe" to Data
**Papatzis Spotter** was built to provide technical documentation against "digital gaslighting." 

Reviewing code presented as "academic standard" revealed a clear lack of "human scent":
- **Verbosity Overload:** Sterile comments explaining the obvious.
- **Mechanical Structure:** "Soulless" organization mirroring default LLM outputs.

Verified through local LLM testing (Proxmox stack), the verdict was clear: **High-dose AI Slop.** This tool converts gut feelings into **concrete metrics**.

---

## Installation & Setup

### Automated Start (Windows)
```powershell
./run_orchestrator.bat
```

### Manual Download
Latest stable binaries are available in the [Releases](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/stable_release) section.

---

## Diagnostic Output Examples

### Case A: Human-crafted code
```bash
[OK] Slop Score: 12.4%
[OK] Humanity shield active.
[OK] Craftsmanship detected.
[READY] Safe for production.
```

### Case B: Detected Slop
```bash
[FAIL] Slop Score: 98.3%
[!] Pillar: Robotic Uniformity (93.3)
[!] Finding: Architecture Overkill detected.
[STATUS] High Risk: AI-Generated Slop.
```

---
*Built for objectivity in code origin analysis. No cloud, 100% offline.*

