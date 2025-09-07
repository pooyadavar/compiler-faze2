## 📌 Project Title

**Design and Implementation of a Mini-C Code Deobfuscator**

---

## 🧠 Project Objective

This project is the reverse of the Mini-C **Obfuscator**.
It takes **obfuscated (dirty) Mini-C code** produced by the obfuscator and **restores a clean, human-readable version** of the original source code.

The **goal** is to undo obfuscation transformations while preserving **functional equivalence**.

---

## ⚙️ Features

The deobfuscator pipeline removes/undoes:

1. **Control-Flow Flattening Recovery**

   * Detects dispatcher/state-machine patterns and reconstructs `if`, `while`, and `for` statements.
2. **Function Inlining Recovery**

   * Detects inlined function bodies and reconstructs original function calls.
3. **Dead Code Removal**

   * Removes unused variables (`unused_*`) and `if(0)` blocks.
4. **Expression Simplification**

   * Converts `a - (-b)` back to `a + b`,
   * Simplifies redundant conditions (e.g., `!(x != y)` → `x == y`).
5. **Name Recovery**

   * Renames meaningless variable names (`abc123`, `t0`, `t1`, …) back into consistent, short readable ones (`x, y, result`).
6. **Code Generation**

   * Outputs clean Mini-C code (`output_clean.mc`) that compiles and behaves like the original input.

---

## 📂 Project Structure

```
MiniC-Deobfuscator/
│── deobfuscator/
│   ├── ast.py                # AST definitions
│   ├── ast_builder.py        # Builds AST from parse tree
│   ├── parser/               # ANTLR-generated parser files
│   ├── code_generator.py     # Emits cleaned Mini-C code
│   └── techniques/
│       ├── dead_code_remover.py
│       ├── expr_simplifier.py
│       ├── name_recoverer.py
│       ├── controlflow_unflattener.py
│       └── inline_reconstructor.py
│── input/
│   └── input_dirty.mc        # Obfuscated input code
│── output/
│   └── output_clean.mc       # Clean generated output
│── grammar/
│   └── ObfuMiniC.g4          # ANTLR grammar for Mini-C
│── run_antlr.bat             # Script to regenerate parser (Windows)
│── main.py                   # Entry point for deobfuscation
│── README.md                 # This file
```

---

## 🛠️ Tools & Technologies

* **Python 3.10+**
* **ANTLR 4.12.0** (Python3 target)
* **Windows** (tested) – works on Linux/Mac with slight adjustments
* Compiler for testing: **GCC / Clang**

---

## ▶️ How to Run

1. **Install Requirements**

   ```bash
   uv init
   uv venv
   uv sync
   ```

2. **Generate Parser**

   ```bash
   cd grammar
   run_antlr.bat
   ```

3. **Run Deobfuscator**

   ```bash
   python main.py
   ```

   * Input: `input/input_dirty.mc`
   * Output: `output/output_clean.mc`

---

## 📊 Example

### Input (dirty code)

```c
int nuf349(int rru329, int gmd878) {
    int _f0_state = 0;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
    }
    {
    _f0_case_0:
        int yzy830 = (rru329 - (-gmd878));
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_case_1:
        return yzy830;
    }
}
int main() {
    int vai767 = 5;
    int pmn398 = 10;
    int ymt230 = nuf349(vai767, pmn398);
    printf("%d\n", ymt230);
    return 0;
}
```

### Output (cleaned code)

```c
int add(int a, int b) {
    int result = a + b;
    return result;
}

int main() {
    int x = 5;
    int y = 10;
    int sum = add(x, y);
    printf("%d\n", sum);
    return 0;
}
```

---

## ✅ Evaluation Criteria

* **Correctness** – Clean output must compile and run with the same behavior.
* **Completeness** – All obfuscation patterns must be reverted.
* **Code Quality** – Clean, consistent formatting and naming.
* **Automation** – Fully automatic recovery, no manual editing needed.

---

## 👥 Team
Mobin Rozati
Pooya Davar
Amirreza Dadashzadeh
* Course: Compiler Project – Phase 2 (Mini-C Deobfuscator)

