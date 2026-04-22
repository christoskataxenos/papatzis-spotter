# Design.md — Visual Identity & UX

## 🎨 1. Φιλοσοφία Σχεδίασης
Το **Papatzis Spotter** πρέπει να αποπνέει σοβαρότητα και επαγγελματισμό. Δεν είναι ένα παιχνίδι, είναι ένα διαγνωστικό εργαλείο υψηλής ποιότητας.

- **Clean & Sharp**: Καθαρές γραμμές, καθόλου περιττά στοιχεία.
- **Glassmorphism**: Subtle εφέ διαφάνειας για βάθος.
- **Human-Centric**: Χρώματα που καθοδηγούν, δεν τρομάζουν.

---

## 💎 2. Χρωματική Παλέτα

| Στοιχείο | Χρώμα (Hex) | Ρόλος |
| :--- | :--- | :--- |
| **Background** | `#0a0a0a` | Deep Space Black (Main BG) |
| **Surface** | `#111111` | Glass Panels |
| **Accent 1** | `#2F6FFF` | Electric Blue (Primary Actions) |
| **Accent 2** | `#A259FF` | Electric Purple (Analytics) |
| **Human OK** | `#2ECC71` | Emerald Green (High Score) |
| **Slop Warning** | `#FF6F5E` | Muted Coral (Low Score) |

---

## 🧩 3. Core UI Components

### 1. Dashboard Dial (Gauge)
- **Visual**: Ένα ημικύκλιο ή κύκλος που γεμίζει ανάλογα με το Score.
- **Animation**: Smooth easing (200-300ms) κατά το φόρτωμα.
- **Context**: Αλλάζει χρώμα από Πράσινο → Μπλε → Coral.

### 2. Pillar Cards
- **Design**: Glassmorphism επιφάνειες με ελαφρύ border.
- **Content**: Icon + Pillar Name + Score.
- **Interaction**: Hover scale (1.02x) για feedback.

### 3. Monaco Editor Integrations
- **Theme**: VS Dark (bespoke modifications).
- **Markers**: Υπογράμμιση των slop patterns μέσα στον κώδικα.

### 4. Explainability Widgets
- **Visual**: Μικρά γραφήματα (Sparklines) ή μπάρες προόδου που δείχνουν μετρικές όπως η εντροπία και η πολυπλοκότητα.
- **Context**: Βοηθούν τον χρήστη να καταλάβει το "γιατί" πίσω από ένα στατιστικό εύρημα.

---

## 📐 4. Typography & Spacing
- **Font**: Inter (Sans-serif) για το UI, Fira Code για τον editor.
- **Grid**: 4px baseline για σωστή ευθυγράμμιση.
- **Margins**: Γενναιόδωρο whitespace για να "αναπνέει" η ανάλυση.
