# Architecture.md — System Structure

## 🧠 1. Στρατηγική Σχεδίασης
Το **AiSlop-Generation-finder** ακολουθεί μια "Hybrid Offline" αρχιτεκτονική. Όλη η επεξεργασία γίνεται τοπικά για μέγιστη προστασία της ιδιωτικότητας του χρήστη.

---

## 🏗️ 2. Τα 3 Επίπεδα (Layers)

### 1. React Frontend (The UI)
- **Τεχνολογία**: TypeScript + React + Vite.
- **Ευθύνη**: Διαχείριση της διεπαφής, εμφάνιση των αποτελεσμάτων, Monaco Editor για τον κώδικα.
- **State Management**: **Zustand** για ελαφρύ και γρήγορο state.

### 2. Tauri Shell (The Bridge)
- **Τεχνολογία**: Rust.
- **Ευθύνη**: Ασφαλής επικοινωνία με το filesystem, διαχείριση του Python Sidecar, IPC (Inter-Process Communication).
- **Plugins**: `tauri-plugin-shell` για το τρέξιμο της μηχανής ανάλυσης.

### 3. Python Sidecar (The Engine)
- **Τεχνολογία**: Python + Tree-Sitter + Pydantic + Scipy/Numpy (για στατιστικά).
- **Ευθύνη**: 
    - **AST Analysis Layer**: Parsing και δομικός έλεγχος μέσω Tree-Sitter.
    - **Statistical Layer**: Υπολογισμός εντροπίας, n-grams και burstiness.
    - **Scoring Layer**: Στάθμιση των 5 Πυλώνων και παραγωγή JSON Findings.
- **Packaging**: Standalone executable μέσω **PyInstaller**.

---

## 🔄 3. Ροή Δεδομένων (Data Flow)

1. **Input**: Ο χρήστης επικολλά κώδικα στον Monaco Editor.
2. **Invoke**: Το Frontend καλεί την Rust εντολή `analyze_code`.
3. **Spawn**: Η Rust σηκώνει το Python Sidecar και του στέλνει τον κώδικα μέσω `stdin` (JSON).
4. **Analysis**: Η Python αναλύει το AST και παράγει Findings.
5. **Score**: Η Python υπολογίζει τα 5 Pillars και επιστρέφει το JSON αποτέλεσμα μέσω `stdout`.
6. **Display**: Το Frontend λαμβάνει το JSON και ενημερώνει το Dashboard.

---

## 📂 4. Project Structure (Key Paths)

- `/src`: React Frontend Source.
- `/src-tauri`: Rust & Tauri Configuration.
- `/analyzer`: Python Engine Logic.
- `/projectrules`: Documentation & Guidelines (You are here).
- `/scripts`: Automation & Bundling scripts.
