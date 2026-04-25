# Papatzis Spotter: The AI-Slop Generation Finder

[🇬🇷 Ελληνικά](#ελληνικά) | [🇬🇧 English](#english)

---

<a name="ελληνικά"></a>
## 🇬🇷 Ελληνικά: Το Motivation πίσω από το Project

### Από το "Vibe" στα Δεδομένα
Η ιδέα για το **Papatzis Spotter** δεν γεννήθηκε σε θεωρητικό επίπεδο, αλλά από μια πραγματική ανάγκη για τεχνική τεκμηρίωση απέναντι στο "ψηφιακό gaslighting". 

Όλα ξεκίνησαν όταν κλήθηκα να αξιολογήσω έναν κώδικα που παρουσιάστηκε ως "πρότυπο ακαδημαϊκό έργο". Ως developer, η πρώτη επαφή με το source code μου προκάλεσε άμεση καχυποψία. Ο κώδικας δεν είχε "ανθρώπινο αποτύπωμα":
- **Υπερβολική Φλυαρία:** Σχόλια που εξηγούσαν τα αυτονόητα με μια αποστειρωμένη ευγένεια.
- **Μηχανική Δομή:** Μια τέλεια, αλλά "άψυχη" οργάνωση που θύμιζε έντονα το default output των LLMs.

Όταν η χρήση AI διαψεύστηκε κατηγορηματικά, αποφάσισα να το ερευνήσω με τα μέσα που διαθέτω. Πέρασα τα δείγματα από το δικό μου tech stack (local LLMs σε Proxmox server και cloud engines). Η ετυμηγορία ήταν ομόφωνη: **High-dose AI Slop.**

**Γιατί το έφτιαξα:**
Συνειδητοποίησα ότι στον ακαδημαϊκό και επαγγελματικό χώρο, η κρίση για το αν κάτι είναι "προϊόν AI" βασίζεται συχνά σε μια αόριστη διαίσθηση (το "vibe"). Αυτό οδηγεί σε δύο άκρα: 
1. Σε ανθρώπους που παρουσιάζουν Slop ως δικό τους έργο (οι "Παπατζήδες").
2. Σε εξεταστές που απορρίπτουν αυθαίρετα γνήσιο έργο φοιτητών επειδή "τους φαίνεται για AI".

Το Papatzis Spotter είναι το εργαλείο που μετατρέπει αυτή τη διαίσθηση σε **συγκεκριμένα metrics**, δίνοντας απαντήσεις βασισμένες σε δομική και στατιστική ανάλυση.

---

### Τεχνικά Χαρακτηριστικά
Ο μηχανισμός ανάλυσης επικεντρώνεται σε:
- **Structural Analysis:** Εντοπισμός επαναλαμβανόμενων μοτίβων και "LLM-isms" στη δομή.
- **Comment Analysis:** Αξιολόγηση της πυκνότητας και του ύφους των σχολίων.
- **Statistical Entropy:** Μέτρηση της μεταβλητότητας και της προβλεψιμότητας του κώδικα.
- **Naming Conventions:** Ανάλυση της πιθανότητας τα ονόματα των μεταβλητών να έχουν παραχθεί από μηχανή.

---

<a name="english"></a>
## 🇬🇧 English: Developer Motivation

### From "Vibe" to Data
The idea for **Papatzis Spotter** wasn't born from theory, but from a practical need for technical documentation against "digital gaslighting."

It all started when I reviewed code presented as a "model academic work." As a developer, my first look at the source code triggered immediate suspicion. The code lacked a "human scent":
- **Verbosity Overload:** Comments explaining the obvious with sterile, robotic politeness.
- **Mechanical Structure:** A perfect but "soulless" organization that mirrored default LLM outputs.

When AI involvement was flatly denied, I decided to verify it using my own tech stack (local LLMs on a Proxmox server and various cloud engines). The verdict was unanimous: **High-dose AI Slop.**

**Why I Built This:**
I realized that in both academic and professional environments, judging whether something is "AI-generated" often relies on a vague hunch (the "vibe"). This leads to two extremes:
1. People passing off "Slop" as their own work (the "Papatzis" or shell game players).
2. Examiners arbitrarily rejecting authentic student work because it "looks like AI."

Papatzis Spotter is the tool that converts that gut feeling into **concrete metrics**, providing answers based on structural and statistical analysis.

---

### Technical Overview
The analysis engine focuses on:
- **Structural Analysis:** Detecting repetitive patterns and "LLM-isms" in code structure.
- **Comment Analysis:** Evaluating comment density, tone, and verbosity.
- **Statistical Entropy:** Measuring code variability and predictability.
- **Naming Conventions:** Analyzing the probability of machine-generated identifiers.

---

### Installation & Setup

#### 🚀 Automated Solution (Windows)
For a quick start on Windows, simply run:
- **`run_orchestrator.bat`**
This script handles virtual environment creation, dependency installation, and starts the Orchestrator in the background.

#### 🛠️ Manual Installation
1. **Prerequisites:** Python 3.10+, Node.js.
2. **Setup:**
   ```bash
   pip install -r analyzer/requirements.txt
   npm install
   ```
3. **Run:**
   ```bash
   npm run tauri dev
   ```

---

### 🖥️ CLI Example Output
Όταν το Papatzis Spotter αναλύει ένα αρχείο, το output είναι ξεκάθαρο και άμεσο:

**Case A: Human-crafted code**
```bash
papatzis audit ./editor.py
[OK] Slop Score: 12.4%
[OK] Humanity shield active.
[OK] Craftsmanship detected.
[READY] Safe for production.
```

**Case B: Detected Slop**
```bash
papatzis audit ./generator.py
[FAIL] Slop Score: 98.3%
[!] Pillar: Robotic Uniformity (93.3)
[!] Finding: Architecture Overkill detected. Logic 8/10 Slop density.
[STATUS] High Risk: AI-Generated Slop.
```

---
*Built to bring objectivity to code origin analysis.*
