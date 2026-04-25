# Papatzis Spotter: The AI-Slop Generation Finder

[🇬🇷 Ελληνικά](#ελληνικά) | [🇬🇧 English](#english)

---

<a name="ελληνικά"></a>
## 🇬🇷 Ελληνικά: Το Μανιφέστο του Παπατζή

### "Αυτό είναι AI, το καταλαβαίνω από το vibe."
Όλα ξεκίνησαν με αυτή τη φράση. Ένας καθηγητής, μια διπλωματική εργασία, και η αυθαίρετη απόρριψη βασισμένη όχι σε αποδείξεις, αλλά σε μια "διαίσθηση". Ο ψηφιακός παπατζής είχε μόλις εμφανιστεί στην αίθουσα, παίζοντας το παιχνίδι "πού είναι η αλήθεια" με την καριέρα ενός φοιτητή.

Το **Papatzis Spotter** γεννήθηκε από την ανάγκη να αντιστρέψουμε τους όρους. Αν οι άνθρωποι πρόκειται να κατηγορούν άλλους για "Slop" (ψηφιακή σαβούρα παραγόμενη από LLMs), ας το κάνουν με δεδομένα, όχι με μαντεψιές.

### Τι είναι το Papatzis Spotter;
Είναι ένας εξελιγμένος μηχανισμός ανάλυσης κώδικα (Python/C/TS) που δεν ψάχνει απλά για "AI ίχνη", αλλά αναλύει την **ψυχή** του κώδικα:
- **Δομική Ανάλυση (Structural):** Ψάχνει για τα επαναλαμβανόμενα μοτίβα που λατρεύουν τα LLMs.
- **Ανάλυση Σχολίων (Comments):** Εντοπίζει την υπερβολικά ευγενική και επεξηγηματική "φλυαρία" της τεχνητής νοημοσύνης.
- **Στατιστική Πιθανότητα (Statistical):** Μετράει την εντροπία και τη μεταβλητότητα του κώδικα.
- **Naming Patterns:** Ξεσκεπάζει τα "τέλεια" ονόματα μεταβλητών που κανένας άνθρωπος δεν θα χρησιμοποιούσε στις 3 το πρωί.

### Γιατί το χρειαζόμαστε;
Γιατί ο "Ψηφιακός Παπατζής" είναι παντού:
1. Στον καθηγητή που βαριέται να διορθώσει και πετάει μια ρετσινιά "AI".
2. Στον developer που γεμίζει το repo με ασυνάρτητο κώδικα από το ChatGPT.
3. Στην ανάγκη μας για αλήθεια σε έναν κόσμο γεμάτο Slop.

---

### Τεχνική Εγκατάσταση
1. **Προαπαιτούμενα:** Python 3.10+, Node.js (για το UI).
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

<a name="english"></a>
## 🇬🇧 English: The Papatzis Manifesto

### "This is AI, I can feel the vibe."
It all started with those words. A professor, a final thesis, and an arbitrary rejection based not on evidence, but on a "hunch." The digital shell game player (The "Papatzis") had just entered the room, playing "find the truth" with a student's future.

**Papatzis Spotter** was born from the need to flip the script. If people are going to accuse others of "Slop" (low-quality, LLM-generated content), let them do it with data, not guesses.

### What is Papatzis Spotter?
It is a sophisticated code analysis engine (Python/C/TS) that doesn't just look for "AI traces" but analyzes the **soul** of the code:
- **Structural Analysis:** Searches for the repetitive patterns that LLMs love.
- **Comment Analysis:** Identifies the overly polite and verbose "chatter" of AI.
- **Statistical Probability:** Measures code entropy and variability.
- **Naming Patterns:** Unmasks the "perfect" variable names that no human would use at 3 AM.

### Why do we need it?
Because the "Digital Papatzis" is everywhere:
1. In the professor who is too lazy to grade and just slaps an "AI-generated" label.
2. In the developer who fills the repo with incoherent ChatGPT output.
3. In our need for truth in a world drowning in Slop.

---

### Technical Setup
1. **Prerequisites:** Python 3.10+, Node.js (for the UI).
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
*Created to fight academic arbitrariness and digital laziness.*
