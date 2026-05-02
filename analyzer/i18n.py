# -*- coding: utf-8 -*-

TRANSLATIONS = {
    "EL": {
        "naming.enterprise_slop": {
            "message": "Οι ονοματολογίες '{name}' παραπέμπουν σε Enterprise Slop.",
            "human_alternative": "Αντικατάστησε το '{name}' με κάτι απλό. Η οικονομία λέξεων είναι δείγμα εμπειρίας. Για παραδειγμα, πες 'TextValidator' αντί για 'SymmetricalTextualEntityValidatorFactory'.",
            "rationale": "Τα AI μοντέλα 'εκπαιδεύονται' να είναι υπερ-επαγγελματικά, χρησιμοποιώντας τεράστια ονόματα ακόμα και για απλές λειτουργίες."
        },
        "naming.generic": {
            "message": "Τυπικό (generic) AI naming: '{name}'",
            "human_alternative": "Γίνε πιο συγκεκριμένος. Τι ακριβώς περιέχει το '{name}'; Αν είναι λίστα χρηστών, πες το 'users'.",
            "rationale": "Το AI συχνά χρησιμοποιεί λέξεις-πασπαρτού όπως 'data', 'info' ή 'value' όταν βαριέται να σκεφτεί το context."
        },
        "naming.camel_case_slop": {
            "message": "CamelCase Μεταβλητή '{name}': Μη-παραδοσιακό naming για C.",
            "human_alternative": "Χρησιμοποίησε snake_case (π.χ. `validation_result`).",
            "rationale": "Ο CamelCase στη C είναι ισχυρό αποτύπωμα LLM, καθώς μεταφέρουν συμβάσεις από Java/JS."
        },
        "naming.dummy": {
            "message": "Τυπικό (dummy) όνομα: '{name}'",
            "human_alternative": "Δώστε πιο συγκεκριμένο όνομα αν ο κώδικας είναι παραγωγής.",
            "rationale": "Κοινά ονόματα σε dummy scripts και AI παραδείγματα."
        },
        "suspicion.verbosity": {
            "message": "Φλύαρος Σχολιασμός (AI Verbosity)",
            "human_alternative": "Αφαίρεσε τα αυτονόητα σχόλια. Αν ο κώδικας είναι `x = 5`, δεν χρειάζεται docstring 10 γραμμών.",
            "rationale": "Τα AI μοντέλα συχνά παράγουν τεράστιες επεξηγήσεις για πολύ απλό κώδικα."
        },
        "suspicion.abstraction_slop": {
            "message": "Abstraction Over-engineering",
            "human_alternative": "Keep it Simple. Μην χτίζεις 'καθεδρικούς ναούς' για να λύσεις ένα πρόβλημα 5 γραμμών.",
            "rationale": "Το AI προσπαθεί να εντυπωσιάσει εφαρμόζοντας enterprise patterns ακόμα και σε απλά scripts."
        },
        "suspicion.chat_boilerplate": {
            "message": "AI Chat Boilerplate",
            "human_alternative": "Διέγραψε αυτές τις φράσεις. Προδίδουν copy-paste από chat.",
            "rationale": "Φράσεις όπως 'As an AI language model' είναι η απόλυτη σφραγίδα του AI."
        },
        "structural.logic_verbosity": {
            "message": "Δομική Φλυαρία (Logic Verbosity)",
            "human_alternative": "Αντικατάστησε το if/else με ένα άμεσο return. Π.χ. `return x > 5`.",
            "rationale": "Το AI έχει την τάση να είναι υπερβολικά αναλυτικό για να φαίνεται επεξηγηματικό."
        },
        "structural.proxy_function": {
            "message": "Άδεια Συνάρτηση (Wrapper Slop)",
            "human_alternative": "Αφαίρεσε τη συνάρτηση-περιτύλιγμα αν δεν προσθέτει business logic.",
            "rationale": "Τα LLMs δημιουργούν συχνά 'άδειες' συναρτήσεις που απλώς πασάρουν δεδομένα."
        },
        "structural.gpt_error_pattern": {
            "message": "Τυπικό AI Error Handling Template",
            "human_alternative": "Μην μένεις στο `print(e)`. Χρησιμοποίησε σωστό logger ή custom exception.",
            "rationale": "Το pattern `try: ... except: print(e)` είναι η εύκολη λύση του AI."
        },
        "structural.low_depth_variance": {
            "message": "Χαμηλή Διακύμανση Βάθους (Flat Logic)",
            "human_alternative": "Ενισχύστε τη δομή του κώδικα με πιο φυσικές διακυμάνσεις.",
            "rationale": "Ο ανθρώπινος κώδικας τείνει να έχει 'κορυφές' και 'κοιλάδες' πολυπλοκότητας."
        },
        "structural.low_node_entropy": {
            "message": "Χαμηλή Εντροπία Δομής",
            "human_alternative": "Εμπλουτίστε τον κώδικα με πιο φυσικές προγραμματιστικές δομές.",
            "rationale": "Τα LLMs συχνά ανακυκλώνουν τις ίδιες δομικές μονάδες."
        },
        "structural.high_assignment_ratio": {
            "message": "Υψηλό Ratio Αναθέσεων/Loops",
            "human_alternative": "Εμπλουτίστε τη λογική με δυναμικές δομές ελέγχου.",
            "rationale": "Το AI τείνει να 'ξεδιπλώνει' λογική σε πολλές αναθέσεις αντί για loops."
        },
        "comment.gpt_style": {
            "message": "GPT-Style Φλύαρα Σχόλια",
            "human_alternative": "Αποφύγετε τα σχόλια που περιγράφουν το προφανές.",
            "rationale": "Το AI σχολιάζει κάθε γραμμή κώδικα με textbook ύφος."
        },
        "comment.obvious": {
            "message": "Περιττά Σχόλια Σύνταξης",
            "human_alternative": "Αφαιρέστε σχόλια που επαναλαμβάνουν τη σύνταξη της γλώσσας.",
            "rationale": "Οι έμπειροι προγραμματιστές σχολιάζουν το 'γιατί', όχι το 'τι'."
        },
        "comment.textbook_style": {
            "message": "Textbook Style Σχόλιο",
            "human_alternative": "Γράψτε πιο άμεσα σχόλια για το συγκεκριμένο context.",
            "rationale": "Σχόλια που ξεκινούν με ορισμούς χωρίς αναφορά στην υλοποίηση είναι δείγμα AI Slop."
        },
        "comment.wikipedia_style": {
            "message": "Wikipedia-Style Slop",
            "human_alternative": "Συνοψίστε τη θεωρία. Ο κώδικας πρέπει να είναι αυτο-επεξηγηματικός.",
            "rationale": "Τα LLMs συχνά κάνουν 'κήρυγμα' μέσα στα σχόλια."
        },
        "redundancy.unreachable": {
            "message": "Εντοπίστηκε μη προσβάσιμος κώδικας",
            "human_alternative": "Αφαιρέστε τον περιττό κώδικα μετά το return.",
            "rationale": "Τα LLMs αφήνουν συχνά debug κώδικα που δεν εκτελείται."
        },
        "redundancy.over_abstraction": {
            "message": "Over-abstraction: Κλάση με μία μέθοδο",
            "human_alternative": "Αντικαταστήστε την κλάση με μια απλή συνάρτηση.",
            "rationale": "Το AI δημιουργεί κλάσεις για τα πάντα, ακόμα και όταν δεν χρειάζονται."
        },
        "similarity.robotic_uniformity": {
            "message": "Ρομποτική Ομοιομορφία: Cluster {count} όμοιων blocks",
            "human_alternative": "Ενισχύστε την ποικιλομορφία. Αποφύγετε τα επαναλαμβανόμενα templates.",
            "rationale": "Η δομική ομοιότητα (>80%) σπάνια συμβαίνει σε άνθρωπο χωρίς copy-paste."
        },
        "similarity.high_global_entropy": {
            "message": "Υψηλή Καθολική Ομοιότητα ({mean_jaccard})",
            "human_alternative": "Προσθέστε 'ανθρώπινο θόρυβο' και διαφοροποιήστε τις δομές.",
            "rationale": "Η μέση ομοιότητα είναι πολύ υψηλή, υποδεικνύοντας ενιαίο generator."
        },
        "integrity.violation": {
            "message": "Παραβίαση Template: Λείπει το '{identifier}'",
            "human_alternative": "Μην διαγράφετε στοιχεία του template. Το '{identifier}' είναι απαραίτητο.",
            "rationale": "Η αλλοίωση του template υποδηλώνει απρόσεκτη χρήση AI."
        },
        "logic.manual_strlen": {
            "message": "Algorithmic Slop: Χειροκίνητο strlen loop",
            "human_alternative": "Χρησιμοποίησε την strlen() από την <string.h>.",
            "rationale": "Το AI γράφει συχνά δικά του loops αντί για standard βιβλιοθήκες."
        },
        "logic.heap_abuse": {
            "message": "Memory Slop: Περιττό malloc",
            "human_alternative": "Δήλωσε το struct στο stack αντί για το heap.",
            "rationale": "Το AI κάνει malloc τα πάντα. Στη C, αυτό προσθέτει ρίσκο leaks."
        },
        "logic.javafication": {
            "message": "Java-fication: Υπερβολικά Struct Names",
            "human_alternative": "Χρησιμοποίησε πιο άμεση ονοματολογία (π.χ. 'User').",
            "rationale": "Τα LLMs 'πακετάρουν' τα πάντα σε structs με Java-style ονόματα."
        },
        "statistical.low_token_entropy": {
            "message": "Χαμηλή Εντροπία Tokens",
            "human_alternative": "Ενισχύστε την ποικιλία στην ονοματολογία.",
            "rationale": "Η χαμηλή εντροπία υποδηλώνει την ομοιόμορφη κατανομή tokens των LLMs."
        },
        "statistical.low_burstiness": {
            "message": "Χαμηλή Διακύμανση (Uniform Line Lengths)",
            "human_alternative": "Αποφύγετε την ομοιομορφία στο μήκος των εντολών.",
            "rationale": "Ο μηχανικός ρυθμός είναι στατιστικό αποτύπωμα των LLMs."
        },
        "statistical.high_repetition": {
            "message": "Υψηλή Επανάληψη N-gram",
            "human_alternative": "Αποφύγετε τις επαναλαμβανόμενες λεκτικές δομές.",
            "rationale": "Τα LLMs εγκλωβίζονται σε συγκεκριμένες λεκτικές ακολουθίες."
        },
        "statistical.info": {
            "message": "Engine Mode: {lang}",
            "human_alternative": "Σημείωση: Η λειτουργία Generic Code είναι πειραματική.",
            "rationale": "Η ανάλυση εκτελείται με κανόνες για {lang}."
        },
        "language.generic": {
            "message": "Generic Code",
            "human_alternative": "Πειραματική υποστήριξη για άγνωστες γλώσσες.",
            "rationale": ""
        },
        "statistical.error": {
            "message": "Σφάλμα Αναλυτή ({analyzer}): {error}",
            "human_alternative": "",
            "rationale": "Ένας από τους αναλυτές απέτυχε. Τα υπόλοιπα αποτελέσματα είναι έγκυρα."
        },
        "statistical.fake_metric": {
            "message": "Εντοπίστηκε Fake Metric: '{metric_name}'",
            "human_alternative": "Αφαιρέστε τα ψεύτικα metrics.",
            "rationale": "Το AI εφευρίσκει μεταβλητές όπως 'accuracy_metric' για να φαίνεται 'επιστημονικό'."
        },
        "statistical.stupid_logic": {
            "message": "Εντοπίστηκε Anti-pattern Logic",
            "human_alternative": "Χρησιμοποίησε τις δυνατότητες της γλώσσας αντί για 'τεμπέλικες' λύσεις.",
            "rationale": "Το AI προτείνει λύσεις που φαίνονται σωστές αλλά είναι κακές προγραμματιστικά."
        },
        "statistical.async_slop": {
            "message": "Async Enterprise Slop",
            "human_alternative": "Αφαιρέστε τις τεχνητές καθυστερήσεις.",
            "rationale": "Boilerplate async logic χωρίς λόγο ύπαρξης."
        },
        "statistical.buzzwords": {
            "message": "Εντοπίστηκαν Buzzwords: {words}",
            "human_alternative": "Αποφύγετε τους εταιρικούς όρους σε τεχνικό κώδικα.",
            "rationale": "Τα AI μοντέλα χρησιμοποιούν corporate-speak που σπανίζει σε ανθρώπινο κώδικα."
        },
        "comments.ai_style": {
            "message": "GPT Buzzword: '{word}'",
            "human_alternative": "Αφαίρεσε τους βαρύγδουπους όρους.",
            "rationale": "Λέξεις όπως 'synergistic' χρησιμοποιούνται από το GPT για 'padding'."
        },
        "template.integrity": {
            "message": "Παραβίαση Ακεραιότητας Template: λείπουν {count} γραμμές",
            "human_alternative": "Επαναφέρετε τη δομή του template.",
            "rationale": "Η αλλαγή του template προδίδει προσπάθεια προσαρμογής κώδικα AI."
        },
        "humanity.shield": {
            "message": "Ανθρώπινο Αποτύπωμα: '{marker}'",
            "human_alternative": "",
            "rationale": "Ενδείξεις ανθρώπινης πρόθεσης (TODO, FIXME)."
        },
        "semantic.high_uniformity": {
            "message": "Υψηλή Σημασιολογική Ομοιότητα ({avg_sim})",
            "human_alternative": "Ενισχύστε τη μοναδικότητα κάθε συνάρτησης.",
            "rationale": "Το AI ανακυκλώνει τα ίδια λεκτικά μοτίβα."
        },
        "semantic.template_functions": {
            "message": "Εντοπίστηκαν συναρτήσεις-καλούπια (Templates)",
            "human_alternative": "Αποφύγετε το copy-paste logic.",
            "rationale": "Τα LLMs παράγουν πανομοιότυπες συναρτήσεις αλλάζοντας μόνο μεταβλητές."
        },
        "critical_error": {
            "message": "Κρίσιμο Σφάλμα Ανάλυσης: {error}",
            "human_alternative": "Εσωτερικό σφάλμα. Ελέγξτε αν ο κώδικας είναι έγκυρος.",
            "rationale": "{trace}"
        },
        "scoring.honest_code": {
            "message": "Τίμιος Κώδικας",
            "human_alternative": "",
            "rationale": "Ο κώδικας φαίνεται αυθεντικός, με οργανική πολυπλοκότητα και ανθρώπινη λογική."
        },
        "scoring.petty_scammer": {
            "message": "Ψιλικατζής",
            "human_alternative": "",
            "rationale": "Υπάρχουν ενδείξεις AI βοηθείας, αλλά με κάποια προσπάθεια ενσωμάτωσης."
        },
        "scoring.professional_papatzis": {
            "message": "Επαγγελματίας Παπατζής",
            "human_alternative": "",
            "rationale": "Βαριά χρήση AI με τυπικά enterprise patterns και ρομποτική δομή."
        },
        "scoring.amateur_slop": {
            "message": "Ερασιτέχνης (100% Slop)",
            "human_alternative": "",
            "rationale": "Ακατέργαστο copy-paste από LLM. Ο κώδικας είναι 100% στατιστικά προβλέψιμος."
        }
    },
    "EN": {
        "naming.enterprise_slop": {
            "message": "Enterprise Slop: '{name}'",
            "human_alternative": "Replace '{name}' with something simple. Conciseness is a sign of experience. For example, if it's a validator, just call it 'TextValidator' instead of 'SymmetricalTextualEntityValidatorFactory'.",
            "rationale": "AI models are trained to be hyper-professional, leading to oversized names (Factories, Entities, Managers) even for simple functions. Humans write code to be read, not to impress."
        },
        "naming.generic": {
            "message": "Lazy AI Naming: '{name}'",
            "human_alternative": "Be more specific. What exactly does this '{name}' contain? If it's a list of users, name it 'users' or 'user_list'.",
            "rationale": "AI often gets lazy thinking about context and uses catch-all words like 'data', 'info', or 'value'. This makes the code hard for humans to understand."
        },
        "naming.camel_case_slop": {
            "message": "CamelCase Variable '{name}': Non-traditional naming for C.",
            "human_alternative": "Use snake_case (e.g., `validation_result`).",
            "rationale": "CamelCase in C is a strong LLM footprint, as models tend to carry over conventions from other languages (Java/JS)."
        },
        "naming.dummy": {
            "message": "Typical (dummy) name: '{name}'",
            "human_alternative": "If this is production code, provide a more specific name.",
            "rationale": "These names are common in human dummy scripts but also in AI examples. Low severity."
        },
        "suspicion.verbosity": {
            "message": "Chatty AI Verbosity",
            "human_alternative": "Remove self-explanatory comments. If code is `x = 5`, you don't need a 10-line docstring explaining variable assignment.",
            "rationale": "AI models are 'paid' to be chatty. They often produce massive explanations for simple code, which an experienced dev avoids to not bury the logic."
        },
        "suspicion.abstraction_slop": {
            "message": "Abstraction Over-engineering",
            "human_alternative": "Keep it Simple. Don't build 'cathedrals' (Managers, Factories) for a problem solvable with a 5-line function.",
            "rationale": "Classic AI behavior: trying to impress by applying enterprise patterns (like Factory Pattern) even to a simple script."
        },
        "suspicion.chat_boilerplate": {
            "message": "AI Chat Boilerplate",
            "human_alternative": "Delete these phrases immediately. They betray that code is a chat copy-paste that hasn't been human-verified.",
            "rationale": "Phrases like 'As an AI language model' are the absolute 'stamp' of AI. They show a lack of attention to detail."
        },
        "structural.logic_verbosity": {
            "message": "Structural Verbosity (Logic)",
            "human_alternative": "Replace if/else with a direct `return condition`. E.g.: `return x > 5` instead of `if x > 5: return True else: return False`.",
            "rationale": "AI tends to be overly verbose to seem explanatory. An experienced dev prefers elegance and avoiding redundant branching."
        },
        "structural.proxy_function": {
            "message": "Empty Proxy Function (Wrapper Slop)",
            "human_alternative": "If the function doesn't add any abstraction or business logic, remove it and call the internal function directly.",
            "rationale": "LLMs sometimes create 'empty' wrapper functions that just pass data along."
        },
        "structural.gpt_error_pattern": {
            "message": "Standard AI Error Handling Template",
            "human_alternative": "Don't just `print(e)`. Use a proper logger, raise a custom exception, or add meaningful error recovery.",
            "rationale": "The `try: ... except Exception as e: print(e)` pattern is the 'easy way out' AI takes if not instructed otherwise."
        },
        "structural.low_depth_variance": {
            "message": "Low Depth Variance",
            "human_alternative": "Enhance code structure with more natural variations in logic depth.",
            "rationale": "Human code tends to have complexity 'peaks' and 'valleys', while AI often produces eerily uniform structures."
        },
        "structural.low_node_entropy": {
            "message": "Low Node Type Entropy",
            "human_alternative": "Enrich the code with more natural programming structures.",
            "rationale": "LLMs often recycle the same structural units, leading to statistically 'flat' code."
        },
        "structural.high_assignment_ratio": {
            "message": "High Assignment-to-Loop Ratio",
            "human_alternative": "Enrich the logic with dynamic control structures.",
            "rationale": "AI tends to 'unroll' logic into many individual assignments instead of compact loops."
        },
        "logic.manual_strlen": {
            "message": "Algorithmic Slop: Manual strlen loop",
            "human_alternative": "Use `strlen()` from <string.h>.",
            "rationale": "AI often writes its own null-terminator loops instead of using the standard library."
        },
        "logic.heap_abuse": {
            "message": "Memory Slop: Unnecessary malloc for local data",
            "human_alternative": "Declare the struct on the stack (e.g., `DataManager data;`) instead of the heap.",
            "rationale": "AI tends to malloc everything (Java-style). In C, this adds unnecessary complexity and memory leak risks."
        },
        "logic.javafication": {
            "message": "Java-fication: Over-engineered Struct Naming",
            "human_alternative": "Use more direct naming (e.g., 'User' instead of 'UserDataEntity').",
            "rationale": "LLMs 'package' everything into structs with Java-style names that don't fit the C ecosystem."
        },
        "similarity.robotic_uniformity": {
            "message": "Robotic Uniformity: Cluster of {count} highly similar blocks",
            "human_alternative": "Increase variety in your code. Avoid using repetitive templates generated by AI.",
            "rationale": "The structural similarity between these blocks is suspiciously high (> 80%), which rarely happens in human code without copy-pasting."
        },
        "similarity.high_global_entropy": {
            "message": "High Global Similarity ({mean_jaccard})",
            "human_alternative": "Add 'human noise' and differentiate your function structures.",
            "rationale": "The average similarity between all blocks is very high, indicating a single generator (LLM) was used."
        },
        "redundancy.unreachable": {
            "message": "Unreachable Code detected",
            "human_alternative": "Remove redundant code after the `return` statement.",
            "rationale": "AI sometimes leaves boilerplate or debug code that is never executed."
        },
        "redundancy.over_abstraction": {
            "message": "Over-abstraction: Single-method class",
            "human_alternative": "Consider if the class can be replaced by a simple function.",
            "rationale": "AI tends to create classes for everything (Java-style), even when a function suffices."
        },
        "integrity.violation": {
            "message": "Template Violation: Missing '{identifier}'",
            "human_alternative": "Do not delete or rename template elements. '{identifier}' is required.",
            "rationale": "Altering the template structure (e.g., deleting required headers or functions) often indicates careless AI use."
        },
        "comment.gpt_style": {
            "message": "GPT-Style Verbose Comments",
            "human_alternative": "Avoid overly explanatory comments that describe the obvious.",
            "rationale": "AI tends to comment every line of code with a textbook style."
        },
        "comment.obvious": {
            "message": "Obvious Syntax Comments",
            "human_alternative": "Remove comments that simply repeat the language syntax.",
            "rationale": "Experienced developers comment on 'why', not 'what' (which is visible from the code)."
        },
        "comment.textbook_style": {
            "message": "Textbook Style Comment",
            "human_alternative": "Write direct comments that relate to the specific code context.",
            "rationale": "Comments that start with definitions without referring to the implementation are a sign of AI Slop."
        },
        "comment.wikipedia_style": {
            "message": "Wikipedia-Style Slop (Verbiage)",
            "human_alternative": "Summarize the theory or remove it entirely. Code should be self-explanatory.",
            "rationale": "LLMs often 'preach' in comments, explaining entire theories."
        },
        "statistical.low_token_entropy": {
            "message": "Low Token Entropy",
            "human_alternative": "Increase variety in naming and structure.",
            "rationale": "Low entropy in large files indicates the uniform token distribution characteristic of LLMs."
        },
        "statistical.low_burstiness": {
            "message": "Low Burstiness (Uniform Line Lengths)",
            "human_alternative": "Avoid excessive uniformity in command lengths.",
            "rationale": "The 'mechanical' rhythm (similar line lengths) is a statistical footprint of LLMs."
        },
        "statistical.high_repetition": {
            "message": "High N-gram Repetition",
            "human_alternative": "Avoid repetitive naming structures.",
            "rationale": "LLMs often get trapped in specific verbal sequences during generation."
        },
        "statistical.info": {
            "message": "Engine Mode: {lang}",
            "human_alternative": "Note: Generic Code mode is experimental.",
            "rationale": "Analysis performed using {lang} specialized rules."
        },
        "language.generic": {
            "message": "Generic Code",
            "human_alternative": "Experimental support for unknown languages.",
            "rationale": ""
        },
        "statistical.error": {
            "message": "Analyzer Error ({analyzer}): {error}",
            "human_alternative": "",
            "rationale": "One of the specialized analyzers failed. The rest of the results are still valid."
        },
        "statistical.fake_metric": {
            "message": "Fake Metric Detected: '{metric_name}'",
            "human_alternative": "Remove fake metrics. If you need real logging, use standard libraries.",
            "rationale": "AI often 'invents' variables like `ai_confidence_score` or `accuracy_metric` to make the code look more 'scientific', without them having any actual function."
        },
        "statistical.stupid_logic": {
            "message": "Anti-pattern Logic Detected",
            "human_alternative": "Use modern language features instead of 'lazy' solutions (e.g., string conversion for indexing).",
            "rationale": "AI sometimes suggests solutions that look correct but are poor programming practice."
        },
        "statistical.async_slop": {
            "message": "Async Enterprise Slop",
            "human_alternative": "Remove fake delays.",
            "rationale": "Boilerplate async logic produced by AI without a clear purpose."
        },
        "statistical.buzzwords": {
            "message": "Buzzwords detected: {words}",
            "human_alternative": "Avoid using overly generic or corporate terms in technical code.",
            "rationale": "AI models often use 'corporate-speak' that is rarely found in human-written code."
        },
        "comments.ai_style": {
            "message": "GPT Buzzword: '{word}'",
            "human_alternative": "Remove high-sounding terms. Accuracy matters more than marketing.",
            "rationale": "Words like 'synergistic' or 'holistic' are used by GPT to 'pad' the text."
        },
        "template.integrity": {
            "message": "Template Integrity Violation: {count} lines missing",
            "human_alternative": "Restore the template structure. Do not change function or struct names.",
            "rationale": "Altering the template indicates an attempt to 'fit' AI-generated code or a disregard for instructions."
        },
        "humanity.shield": {
            "message": "Human Marker: '{marker}'",
            "human_alternative": "",
            "rationale": "Evidence of human intent or frustration (e.g., TODO, FIXME)."
        },
        "semantic.high_uniformity": {
            "message": "High Semantic Uniformity ({avg_sim})",
            "human_alternative": "Enhance the uniqueness and specialization of each function.",
            "rationale": "AI often 'recycles' the same verbal patterns and naming structures."
        },
        "semantic.template_functions": {
            "message": "Template Generated Functions: Template-like functions detected.",
            "human_alternative": "Avoid copy-paste logic with minor changes.",
            "rationale": "LLMs often produce series of functions that are identical, changing only 1-2 variables."
        },
        "critical_error": {
            "message": "Critical Analysis Error: {error}",
            "human_alternative": "An internal error occurred during analysis. Please check if the code is valid for the selected language.",
            "rationale": "{trace}"
        },
        "scoring.honest_code": {
            "message": "Honest Code",
            "human_alternative": "",
            "rationale": "The code appears authentic, with organic complexity and human logic."
        },
        "scoring.petty_scammer": {
            "message": "Petty Scammer",
            "human_alternative": "",
            "rationale": "Evidence of AI assistance, but with some effort to integrate it."
        },
        "scoring.professional_papatzis": {
            "message": "Professional Papatzis",
            "human_alternative": "",
            "rationale": "Heavy AI usage with typical enterprise patterns and robotic structure."
        },
        "scoring.amateur_slop": {
            "message": "Amateur (100% Slop)",
            "human_alternative": "",
            "rationale": "Raw copy-paste from LLM. The code is 100% statistically predictable."
        }
    }
}

def translate(key, ui_lang="EN", **kwargs):
    lang = ui_lang.upper() if ui_lang else "EN"
    if lang not in TRANSLATIONS:
        lang = "EN"
    
    entry = TRANSLATIONS[lang].get(key, TRANSLATIONS["EN"].get(key))
    if not entry:
        return {"message": key, "human_alternative": "", "rationale": ""}
    
    # Format strings safely
    try:
        return {
            "message": entry["message"].format(**kwargs),
            "human_alternative": entry["human_alternative"].format(**kwargs),
            "rationale": entry["rationale"].format(**kwargs)
        }
    except KeyError as e:
        # If a key is missing, return the raw message or a fallback
        return {
            "message": entry["message"],
            "human_alternative": entry["human_alternative"],
            "rationale": entry["rationale"]
        }
