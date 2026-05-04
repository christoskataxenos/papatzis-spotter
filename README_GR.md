# Papatzis Spotter
## Η Offline Μηχανή Ανίχνευσης AI-Slop

[![](https://img.shields.io/badge/version-3.9.0-2F5C8F?style=for-the-badge)](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/v3.9)
[![](https://img.shields.io/badge/license-MIT-333333?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/badge/python-3.10%2B-2F5C8F?style=for-the-badge)](https://python.org)

---

### [ 🌐 English Version ](README.md) | [ 📥 Download Stable ](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/v3.9) | [ 📜 Πλήρες Changelog ](CHANGELOG.md)

---

## 📍 Γρήγορη Πλοήγηση
*   [Η Ιστορία του Παπατζή](#η-ιστορία-του-παπατζή)
*   [100% Offline & Ιδιωτικότητα](#ιδιωτικότητα-και-ασφάλεια)
*   [Οι 5 Πυλώνες Ανίχνευσης](#οι-5-πυλώνες-ανίχνευσης)
*   [Πώς Λειτουργεί (Τα Μαθηματικά)](#πώς-λειτουργεί-τα-μαθηματικά)
*   [Εγκατάσταση](#εγκατάσταση)
*   [Screenshots](#screenshots)
*   [Το Οικοσύστημα](#το-οικοσύστημα)

---

<a name="η-ιστορία-του-papatzi"></a>
## 📖 Η Ιστορία του Papatzi: Από το "Vibe" στα Δεδομένα

Η ιδέα για το **Papatzis Spotter** γεννήθηκε από μια στιγμή καθαρής αμηχανίας. Όλα ξεκίνησαν όταν κλήθηκα να αξιολογήσω κώδικα που παρουσιάστηκε ως "ακαδημαϊκό πρότυπο", αλλά μόλις έριξα μια ματιά στο source code, κάτι μέσα μου άρχισε να "τσιρίζει". Ο κώδικας δεν είχε "μυρωδιά" ανθρώπου.

Είχε όλα εκείνα τα επαναλαμβανόμενα, υπερβολικά ευγενικά και αποστειρωμένα μοτίβα που προδίδουν την AI:
*   **Υπερβολική Φλυαρία:** Σχόλια που εξηγούσαν τα αυτονόητα με αποστειρωμένη ευγένεια.
*   **Μηχανική Δομή:** Μια τέλεια αλλά "άψυχη" οργάνωση που θύμιζε default output των LLMs.

Το Papatzis Spotter μετατρέπει αυτή τη διαίσθηση σε **συγκεκριμένα metrics**. Δεν είναι ένα εργαλείο "πολέμου" κατά της AI, αλλά ένας καθρέφτης που σου δείχνει κατάμουτρα τον "οχετό" (slop) που σου έφτυσε το LLM και σε αναγκάζει να πάρεις την ευθύνη του κώδικά σου.

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="ιδιωτικότητα-και-ασφάλεια"></a>
## 🔒 100% Offline & Private

Σε αντίθεση με άλλα εργαλεία, ο **Papatzis Spotter** σέβεται τον κώδικά σας:
*   **Καμία χρήση Internet:** Το εργαλείο λειτουργεί πλήρως offline.
*   **Κανένα AI API Call:** Δεν στέλνουμε δεδομένα σε OpenAI, Gemini ή Claude.
*   **Τοπική Ανάλυση:** Όλοι οι μαθηματικοί υπολογισμοί και το AST parsing γίνονται αποκλειστικά στον επεξεργαστή σας.
*   **Multithreaded Speed:** Η μηχανή ανάλυσης εκμεταλλεύεται όλους τους πυρήνες του συστήματός σας, προσφέροντας ταχύτητα που ξεπερνά τις cloud λύσεις.
*   **Zero Data Leaks:** Ο κώδικάς σας δεν φεύγει ποτέ από το σύστημά σας.

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="οι-5-πυλώνες-ανίχνευσης"></a>
## 🛡️ Οι 5 Πυλώνες Ανίχνευσης (Η Λογική)

Ο Analyzer δεν κάνει μαντεψιές. "Ξεκοιλιάζει" τον κώδικα και τον περνάει από 5 αμείλικτα φίλτρα:

### 1. Ρομποτική Ομοιομορφία (Architecture Overkill)
Το AI έχει μια εμμονή: θέλει να φαίνεται "enterprise-ready". Αυτό οδηγεί σε ένα τραγικό Ratio Λογικής προς Boilerplate. 

**❌ AI Slop (15 γραμμές για το τίποτα):**
```python
class IStringProcessor(ABC):
    @abstractmethod
    def process(self, s: str) -> str: pass

class IdentityProcessor(IStringProcessor):
    def process(self, s: str) -> str: return s.strip()

def factory(): return IdentityProcessor()

# 30 γραμμές μετά...
proc = factory()
result = proc.process(" hello ")
```

**✅ Human Logic (1 γραμμή που κάνει τη δουλειά):**
```python
def clean_text(s: str): return s.strip()

result = clean_text(" hello ")
```

*   **Διάγνωση:** Severe Structural Slop. Ο κώδικας γράφτηκε για να εντυπωσιάσει, όχι για να λύσει ένα πρόβλημα.

### 2. Στατιστική Φλυαρία (Hadouken Code)
Εντοπισμός υπερβολικά άκαμπτης δενδροειδούς δομής (nesting) και μεταβλητών που ακούγονται έξυπνες αλλά είναι κενές περιεχομένου.

### 3. Βαφτιστικό Slop (Enterprise Naming)
Κανένας άνθρωπος υπό πίεση δεν θα ονόμαζε μια συνάρτηση `execute_symmetrical_textual_entity_validation_sequence()`. Είναι το "επίσημο ένδυμα" της AI για να κρύψει την έλλειψη δημιουργικότητας.

### 4. GPT-Style Παπατζιλίκι (Linguistic DNA)
Ανίχνευση λέξεων-κλειδιών που είναι "σήμα κατατεθέν" των LLMs στα σχόλια (*delving into*, *holistic paradigm*, *robustness*).

### 5. Project Drift (Εντροπία)
Ο άνθρωπος είναι χαοτικός. Το AI είναι τρομακτικά συνεπές. Αν 100 αρχεία έχουν την ίδια "αποστειρωμένη" δομή, τότε είναι προϊόν generator, όχι project.

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="πώς-λειτουργεί-μαθηματικά"></a>
## 🧮 Πώς Λειτουργεί (Μαθηματικά)

### Jaccard Similarity: Η θεωρία με τις μπίλιες
Φαντάσου δύο σακούλες με χρωματιστές μπίλιες. Η Jaccard μετράει πόσες μπίλιες είναι **ακριβώς ίδιες** σε σχέση με το **σύνολο**.
*   Στον Papatzis Spotter, οι "μπίλιες" είναι τα μοτίβα του κώδικα.
*   Όσο πιο κοντά στο 1 είναι το σκορ, τόσο πιο "αντίγραφο" είναι ο κώδικας.

### Shannon Entropy (Στατιστική Εντροπία)
Μετράμε τον "θόρυβο" του κώδικα. Ο ανθρώπινος κώδικας έχει φυσικές ασυνέπειες. Ο AI κώδικας είναι συχνά "στατιστικά αποστειρωμένος" (χαμηλή εντροπία).

### Semantic Echo Mapping
Αναλύουμε τη "γεωμετρία" της λογικής (AST). Ακόμα κι αν αλλάξεις τα ονόματα των μεταβλητών, ο σκελετός της AI παραμένει ο ίδιος.

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="εγκατάσταση"></a>
## 🚀 Εγκατάσταση

### Windows (Αυτοματοποιημένα)
Απλά τρέξτε το script:
```powershell
./scripts/run_orchestrator.bat
```

### Linux / macOS
Απαιτείται Python 3.10+. Απλά τρέξτε:
```bash
./scripts/run_orchestrator.sh
```
*(Υποστήριξη πακέτων .deb και .rpm μέσω Orchestrator + Docker)*

[📥 Κατεβάστε την τελευταία έκδοση](https://github.com/christoskataxenos/papatzis-spotter/releases/tag/v3.9)

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="screenshots"></a>
## 📸 Screenshots

<p align="center">
  <img src="assets/screenshots/home.png" width="800" alt="Home Screen">
  <br>
  <i><b>The Neural Diagnostic Hub</b> — Εκεί που ξεκινάει το κυνήγι.</i>
</p>

<p align="center">
  <img src="assets/screenshots/results.png" width="800" alt="Analysis Results">
  <br>
  <i><b>Forensic Findings</b> — Ανάλυση σε βάθος με ομαδοποίηση ευρημάτων.</i>
</p>

<p align="center">
  <img src="assets/screenshots/help.png" width="800" alt="Help Guide">
  <br>
  <i><b>The Survival Guide</b> — Μαθαίνοντας τα μοτίβα της ψηφιακής παπατζιάς.</i>
</p>

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="το-οικοσύστημα"></a>
## 🌐 Το Οικοσύστημα

*   **Papatzis UI:** Premium εφαρμογή με Tauri & Rust και radar charts.
*   **Git Bouncer:** Ένας "πορτιέρης" (pre-commit hook) που μπλοκάρει το slop πριν ανέβει στο GitHub.
*   **Papatzoskill:** Το "εμβόλιο" για AI agents (Claude, Gemini) που τους αναγκάζει να γράφουν ποιοτικό κώδικα.

[⬆ Πίσω στην κορυφή](#papatzis-spotter)

---

<a name="φιλοσοφία-και-ηθική"></a>
## ⚖️ Φιλοσοφία: Audit, Learn, Master

Το **Papatzis Spotter** είναι ένα εργαλείο με διπλή φύση:

1.  **Για τον Ελεγκτή (Καθηγητή/Lead Dev):** Είναι ένας αδιάψευστος ιατροδικαστικός βοηθός που ξεσκεπάζει το "ψηφιακό gaslighting" και την προσπάθεια παρουσίασης ξένου κώδικα ως δικού τους.
2.  **Για τον Δημιουργό (Φοιτητή/Developer):** Είναι ένας **Μέντορας**. Μέσω των Mentor Hints, σε βοηθά να καταλάβεις πού η AI σε "πούλησε", προτείνοντας έναν πιο ανθρώπινο, ουσιαστικό και αποδοτικό τρόπο γραφής.

**Ηθικό Δίδαγμα:** Το πρόβλημα δεν είναι η χρήση της AI, αλλά η απώλεια του ελέγχου. Ο Papatzis Spotter σε βοηθά να πάρεις ξανά το τιμόνι στα χέρια σου.

---
*Built for objectivity in code origin analysis. No cloud, 100% offline.*
