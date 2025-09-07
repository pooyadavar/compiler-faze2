# deobfuscator/techniques/name_recoverer.py
from typing import List, Set, Dict
from deobfuscator.ast import *

# helper: builtin names we should not remap
_BUILTINS = {"printf", "scanf", "true", "false"}

class NameRecoverer:
    """
    Robust single-pass NameRecoverer:
    - Step A: rename parameters to a,b,p2...
    - Step B: collect declared names + used names (order-preserving)
    - Step C: undeclared-but-used -> t0,t1,... per-function
    - Step D: map first few tX -> x,y,m (avoid collisions with params)
    - Step E: apply mapping across function AST (assign targets, exprs, blocks)
    """

    def recover(self, prog: Program):
        for func in prog.functions:
            self._rename_function(func)

    def _rename_function(self, func: Function):
        # --- PARAMETER RENAMING (stable) ---
        param_old = [p.name for p in func.params]
        param_new = []
        for i, p in enumerate(func.params):
            if i == 0: new = "a"
            elif i == 1: new = "b"
            elif i == 2: new = "c"
            else: new = f"p{i}"
            param_new.append(new)
            p.name = new

        param_old_to_new = {old: new for old, new in zip(param_old, param_new)}

        # --- DECLARED LOCALS ---
        declared = set(self._collect_declared_names(func.body))
        # include param new names as declared for scope checks
        declared.update(param_new)

        # --- COLLECT USED NAMES (ordered by first appearance) ---
        used_ordered = self._collect_used_ordered(func.body)

        # filter out builtins and function name itself
        used_ordered = [u for u in used_ordered if u not in _BUILTINS and u != func.name]

        # --- UNDECLARED-BUT-USED: exclude names already declared or parameter-old names
        undeclared = []
        seen = set()
        for name in used_ordered:
            if name in declared or name in param_old_to_new.values() or name in param_old:
                continue
            if name in seen:
                continue
            seen.add(name)
            undeclared.append(name)

        # --- Map undeclared -> t0,t1,... (per-function)
        temp_map: Dict[str, str] = {}
        counter = 0
        for u in undeclared:
            if u.startswith("unused_"):
                # leave removal to DeadCodeRemover, but map to _unused if needed
                temp_map[u] = f"_unused_{counter}"
                counter += 1
                continue
            temp_map[u] = f"t{counter}"
            counter += 1

        # --- Compose full mapping: parameter-old -> param_new, undeclared->tX
        # IMPORTANT: param_old_to_new should be applied first (so param usage becomes a/b)
        full_map = {}
        full_map.update(param_old_to_new)   # old param names -> a,b,...
        full_map.update(temp_map)           # undeclared -> tX

        # --- APPLY mapping to function body (param mapping first)
        # Apply parameter mapping first so references inside body use a,b before t->x mapping
        for old, new in param_old_to_new.items():
            self._apply_mapping_to_block(func.body, old, new)

        # Now apply temp_map t0,t1... for undeclared original names
        for old, new in temp_map.items():
            self._apply_mapping_to_block(func.body, old, new)

        # --- Now convert tX -> human-friendly locals (x,y,m, ...)
        # choose base names in order, avoid conflicts with param_new
        friendly = ["x", "y", "m", "n", "z"]
        t_names = sorted(set(temp_map.values()))  # deterministic order
        local_map: Dict[str, str] = {}
        used_final = set(param_new)  # avoid param collisions
        idx = 0
        for t in t_names:
            # pick friendly or v# fallback
            chosen = None
            if idx < len(friendly):
                cand = friendly[idx]
                if cand not in used_final:
                    chosen = cand
            if not chosen:
                # find next v#
                k = 0
                while True:
                    cand = f"v{k}"
                    if cand not in used_final:
                        chosen = cand
                        break
                    k += 1
            local_map[t] = chosen
            used_final.add(chosen)
            idx += 1

        # Apply local_map renames
        for old, new in local_map.items():
            self._apply_mapping_to_block(func.body, old, new)

        # Done for this function

    # ------------------------------
    # Collectors (declarations and ordered uses)
    # ------------------------------
    def _collect_declared_names(self, stmts) -> List[str]:
        names = []
        for s in stmts:
            if isinstance(s, VariableDecl):
                names.append(s.name)
            elif isinstance(s, Block):
                names.extend(self._collect_declared_names(s.items))
            elif isinstance(s, IfStmt):
                names.extend(self._collect_declared_names([s.then_branch]))
                if s.else_branch:
                    names.extend(self._collect_declared_names([s.else_branch]))
            elif isinstance(s, WhileStmt):
                names.extend(self._collect_declared_names([s.body]))
            elif isinstance(s, ForStmt):
                names.extend(self._collect_declared_names([s.body]))
        return names

    def _collect_used_ordered(self, stmts) -> List[str]:
        seen = set()
        order = []
        def walk_stmt_list(lst):
            for st in lst:
                walk_stmt(st)
        def walk_stmt(st):
            if st is None:
                return
            if isinstance(st, VariableDecl):
                if st.init_expr:
                    walk_expr(st.init_expr)
            elif isinstance(st, Assignment):
                # target might be Variable or string
                if isinstance(st.target, Variable):
                    add_name(st.target.name)
                elif isinstance(st.target, str):
                    add_name(st.target)
                walk_expr(st.value)
            elif isinstance(st, ExpressionStmt):
                if st.expr:
                    walk_expr(st.expr)
            elif isinstance(st, Return):
                if st.value:
                    walk_expr(st.value)
            elif isinstance(st, IfStmt):
                walk_expr(st.condition)
                walk_stmt(st.then_branch)
                if st.else_branch:
                    walk_stmt(st.else_branch)
            elif isinstance(st, WhileStmt):
                walk_expr(st.condition)
                walk_stmt(st.body)
            elif isinstance(st, ForStmt):
                if st.init: walk_expr(st.init)
                if st.cond: walk_expr(st.cond)
                if st.update: walk_expr(st.update)
                walk_stmt(st.body)
            elif isinstance(st, Block):
                for it in st.items:
                    walk_stmt(it)
            elif isinstance(st, Print):
                for a in st.args:
                    walk_expr(a)
        def add_name(n):
            if n not in seen:
                seen.add(n); order.append(n)
        def walk_expr(e):
            if e is None: return
            if isinstance(e, Variable):
                add_name(e.name)
            elif isinstance(e, BinaryOp):
                walk_expr(e.left); walk_expr(e.right)
            elif isinstance(e, UnaryOp):
                walk_expr(e.operand)
            elif isinstance(e, FuncCall):
                # function name is not a local variable; record args names
                for a in e.args:
                    walk_expr(a)
        walk_stmt_list(stmts)
        return order

    # ------------------------------
    # Mapping application (recursive)
    # ------------------------------
    def _apply_mapping_to_block(self, stmts, old: str, new: str):
        for i, s in enumerate(stmts):
            stmts[i] = self._apply_mapping_to_stmt(s, old, new)

    def _apply_mapping_to_stmt(self, s, old: str, new: str):
        if s is None:
            return s
        # Variable declarations
        if isinstance(s, VariableDecl):
            if s.name == old:
                s.name = new
            if s.init_expr:
                s.init_expr = self._apply_mapping_to_expr(s.init_expr, old, new)
            return s
        # Assignment
        if isinstance(s, Assignment):
            # target might be Variable or plain string; convert plain strings to Variable
            if isinstance(s.target, Variable):
                if s.target.name == old:
                    s.target.name = new
            elif isinstance(s.target, str):
                if s.target == old:
                    s.target = Variable(new)
                else:
                    # convert into Variable node for consistent handling
                    s.target = Variable(s.target)
            s.value = self._apply_mapping_to_expr(s.value, old, new)
            return s
        # Expression statement
        if isinstance(s, ExpressionStmt):
            if s.expr:
                s.expr = self._apply_mapping_to_expr(s.expr, old, new)
            return s
        # Return
        if isinstance(s, Return):
            if s.value:
                s.value = self._apply_mapping_to_expr(s.value, old, new)
            return s
        # If
        if isinstance(s, IfStmt):
            s.condition = self._apply_mapping_to_expr(s.condition, old, new)
            s.then_branch = self._apply_mapping_to_stmt(s.then_branch, old, new)
            if s.else_branch:
                s.else_branch = self._apply_mapping_to_stmt(s.else_branch, old, new)
            return s
        # While
        if isinstance(s, WhileStmt):
            s.condition = self._apply_mapping_to_expr(s.condition, old, new)
            s.body = self._apply_mapping_to_stmt(s.body, old, new)
            return s
        # For
        if isinstance(s, ForStmt):
            if s.init: s.init = self._apply_mapping_to_expr(s.init, old, new)
            if s.cond: s.cond = self._apply_mapping_to_expr(s.cond, old, new)
            if s.update: s.update = self._apply_mapping_to_expr(s.update, old, new)
            s.body = self._apply_mapping_to_stmt(s.body, old, new)
            return s
        # Block
        if isinstance(s, Block):
            for i, it in enumerate(s.items):
                s.items[i] = self._apply_mapping_to_stmt(it, old, new)
            return s
        # Print
        if isinstance(s, Print):
            s.args = [self._apply_mapping_to_expr(a, old, new) for a in s.args]
            return s
        # Switch, cases (if you use them)
        if isinstance(s, Switch):
            s.expr = self._apply_mapping_to_expr(s.expr, old, new)
            for case in s.cases:
                if case.body and isinstance(case.body, Block):
                    for i, st in enumerate(case.body.items):
                        case.body.items[i] = self._apply_mapping_to_stmt(st, old, new)
            return s
        # default: unknown node type - return as-is
        return s

    def _apply_mapping_to_expr(self, e, old: str, new: str):
        if e is None:
            return None
        if isinstance(e, Variable):
            if e.name == old:
                return Variable(new)
            return e
        if isinstance(e, BinaryOp):
            return BinaryOp(e.op,
                            self._apply_mapping_to_expr(e.left, old, new),
                            self._apply_mapping_to_expr(e.right, old, new))
        if isinstance(e, UnaryOp):
            return UnaryOp(e.op, self._apply_mapping_to_expr(e.operand, old, new))
        if isinstance(e, FuncCall):
            return FuncCall(e.name, [self._apply_mapping_to_expr(a, old, new) for a in e.args])
        return e
