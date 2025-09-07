# deobfuscator/techniques/name_recoverer.py
from typing import List, Set, Dict
from deobfuscator.ast import *

# do not remap these
_BUILTINS = {"printf", "scanf", "true", "false"}

class NameRecoverer:
    """
    Robust name recovery:
      - rename function parameters to a,b,c...
      - detect undeclared used identifiers and map them to t0,t1...
      - convert first few temps to friendly names (x,y,m,...)
      - apply mappings everywhere, handling both Variable nodes and raw str identifiers
    """

    def recover(self, prog: Program):
        for func in prog.functions:
            self._rename_function(func)

    def _rename_function(self, func: Function):
        # 1) capture original parameter names
        param_old = [p.name for p in func.params]

        # 2) create new parameter names and set them on Function.params
        param_new = []
        for i, p in enumerate(func.params):
            if i == 0:
                new = "a"
            elif i == 1:
                new = "b"
            elif i == 2:
                new = "c"
            else:
                new = f"p{i}"
            param_new.append(new)
            p.name = new

        # map old param name -> new param name
        param_old_to_new = {old: new for old, new in zip(param_old, param_new)}

        # 3) collect declared local names (not including params)
        declared = set(self._collect_declared_names(func.body))
        # include param new names so they are treated as declared
        declared.update(param_new)

        # 4) collect used identifier names in order of first appearance
        used_ordered = self._collect_used_ordered(func.body)

        # filter out builtins and function name itself
        used_ordered = [u for u in used_ordered if u not in _BUILTINS and u != func.name]

        # 5) detect undeclared-but-used names (exclude param_old to avoid mapping params)
        undeclared = []
        seen = set()
        for name in used_ordered:
            if name in declared: 
                continue
            if name in param_old:  # a true parameter name in body - don't treat as undeclared
                continue
            if name in seen:
                continue
            seen.add(name)
            undeclared.append(name)

        # 6) map undeclared -> t0,t1,...
        temp_map: Dict[str, str] = {}
        counter = 0
        for u in undeclared:
            if u.startswith("unused_"):
                temp_map[u] = f"_unused_{counter}"
                counter += 1
                continue
            temp_map[u] = f"t{counter}"
            counter += 1

        # 7) apply temp_map (rename "orphans" -> tX) first
        for old, new in temp_map.items():
            self._apply_mapping_to_block(func.body, old, new)

        # 8) convert tX -> friendly local names, avoiding param names
        friendly = ["x", "y", "m", "n", "z"]
        t_names = sorted(set(temp_map.values()))
        local_map: Dict[str, str] = {}
        used_final = set(param_new)  # avoid collisions with param names
        idx = 0
        for t in t_names:
            chosen = None
            if idx < len(friendly):
                cand = friendly[idx]
                if cand not in used_final:
                    chosen = cand
            if not chosen:
                # fallback to v#
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

        for old, new in local_map.items():
            self._apply_mapping_to_block(func.body, old, new)

        # 9) finally apply param_old -> param_new mapping to body (last step)
        # This ensures original parameter identifiers are restored to a,b inside body.
        for old, new in param_old_to_new.items():
            self._apply_mapping_to_block(func.body, old, new)

    # -------------------------
    # Collectors
    # -------------------------
    def _collect_declared_names(self, stmts) -> List[str]:
        names = []
        for s in stmts:
            if isinstance(s, VariableDecl):
                names.append(s.name)
            elif isinstance(s, Block):
                names.extend(self._collect_declared_names(s.items))
            elif isinstance(s, IfStmt):
                # in many ASTs then_branch may be Block or Statement
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
        def add(n):
            if n is None:
                return
            if n not in seen:
                seen.add(n); order.append(n)
        def walk_expr(e):
            if e is None:
                return
            if isinstance(e, Variable):
                add(e.name)
            elif isinstance(e, str):
                # raw identifier string
                add(e)
            elif isinstance(e, BinaryOp):
                walk_expr(e.left); walk_expr(e.right)
            elif isinstance(e, UnaryOp):
                walk_expr(e.operand)
            elif isinstance(e, FuncCall):
                # do not add function name, only arguments
                for a in e.args: walk_expr(a)
            elif isinstance(e, Assignment):
                # assignment-as-expression
                if isinstance(e.target, Variable):
                    add(e.target.name)
                elif isinstance(e.target, str):
                    add(e.target)
                walk_expr(e.value)
        def walk_stmt(s):
            if s is None:
                return
            if isinstance(s, VariableDecl):
                if s.init_expr:
                    walk_expr(s.init_expr)
            elif isinstance(s, Assignment):
                if isinstance(s.target, Variable):
                    add(s.target.name)
                elif isinstance(s.target, str):
                    add(s.target)
                walk_expr(s.value)
            elif isinstance(s, ExpressionStmt):
                walk_expr(s.expr)
            elif isinstance(s, Return):
                walk_expr(s.value)
            elif isinstance(s, IfStmt):
                walk_expr(s.condition)
                walk_stmt(s.then_branch)
                if s.else_branch:
                    walk_stmt(s.else_branch)
            elif isinstance(s, WhileStmt):
                walk_expr(s.condition)
                walk_stmt(s.body)
            elif isinstance(s, ForStmt):
                if s.init: walk_expr(s.init)
                if s.cond: walk_expr(s.cond)
                if s.update: walk_expr(s.update)
                walk_stmt(s.body)
            elif isinstance(s, Block):
                for it in s.items:
                    walk_stmt(it)
            elif isinstance(s, Print):
                for a in s.args: walk_expr(a)
            elif isinstance(s, Switch):
                walk_expr(s.expr)
                for case in s.cases:
                    if case.body and isinstance(case.body, Block):
                        for st in case.body.items:
                            walk_stmt(st)
            # unknown node types ignored
        for st in stmts:
            walk_stmt(st)
        return order

    # -------------------------
    # Mapping application (robust)
    # -------------------------
    def _apply_mapping_to_block(self, stmts, old: str, new: str):
        for i, s in enumerate(stmts):
            stmts[i] = self._apply_mapping_to_stmt(s, old, new)

    def _apply_mapping_to_stmt(self, s, old: str, new: str):
        if s is None:
            return s
        if isinstance(s, VariableDecl):
            if s.name == old:
                s.name = new
            if s.init_expr:
                s.init_expr = self._apply_mapping_to_expr(s.init_expr, old, new)
            return s
        if isinstance(s, Assignment):
            # normalize string targets
            if isinstance(s.target, str):
                if s.target == old:
                    s.target = Variable(new)
                else:
                    s.target = Variable(s.target)
            elif isinstance(s.target, Variable):
                if s.target.name == old:
                    s.target.name = new
            s.value = self._apply_mapping_to_expr(s.value, old, new)
            return s
        if isinstance(s, ExpressionStmt):
            if isinstance(s.expr, Assignment):
                # assignment inside expression
                if isinstance(s.expr.target, str) and s.expr.target == old:
                    return None  # assignment to old (maybe unused_) -> remove entirely
                s.expr = self._apply_mapping_to_expr(s.expr, old, new)
            else:
                s.expr = self._apply_mapping_to_expr(s.expr, old, new)
            return s
        if isinstance(s, Return):
            s.value = self._apply_mapping_to_expr(s.value, old, new)
            return s
        if isinstance(s, IfStmt):
            s.condition = self._apply_mapping_to_expr(s.condition, old, new)
            s.then_branch = self._apply_mapping_to_stmt(s.then_branch, old, new)
            if s.else_branch:
                s.else_branch = self._apply_mapping_to_stmt(s.else_branch, old, new)
            return s
        if isinstance(s, WhileStmt):
            s.condition = self._apply_mapping_to_expr(s.condition, old, new)
            s.body = self._apply_mapping_to_stmt(s.body, old, new)
            return s
        if isinstance(s, ForStmt):
            if s.init: s.init = self._apply_mapping_to_expr(s.init, old, new)
            if s.cond: s.cond = self._apply_mapping_to_expr(s.cond, old, new)
            if s.update: s.update = self._apply_mapping_to_expr(s.update, old, new)
            s.body = self._apply_mapping_to_stmt(s.body, old, new)
            return s
        if isinstance(s, Block):
            new_items = []
            for it in s.items:
                mapped = self._apply_mapping_to_stmt(it, old, new)
                if mapped is None:
                    continue
                new_items.append(mapped)
            s.items = new_items
            return s
        if isinstance(s, Print):
            s.args = [self._apply_mapping_to_expr(a, old, new) for a in s.args]
            return s
        if isinstance(s, Switch):
            s.expr = self._apply_mapping_to_expr(s.expr, old, new)
            for case in s.cases:
                if case.body and isinstance(case.body, Block):
                    new_items = []
                    for st in case.body.items:
                        mapped = self._apply_mapping_to_stmt(st, old, new)
                        if mapped is None:
                            continue
                        new_items.append(mapped)
                    case.body.items = new_items
            return s
        return s

    def _apply_mapping_to_expr(self, e, old: str, new: str):
        if e is None:
            return None
        # raw identifier string: convert to Variable node (and rename if needed)
        if isinstance(e, str):
            if e == old:
                return Variable(new)
            return Variable(e)
        if isinstance(e, Variable):
            if e.name == old:
                return Variable(new)
            return e
        if isinstance(e, BinaryOp):
            left = self._apply_mapping_to_expr(e.left, old, new)
            right = self._apply_mapping_to_expr(e.right, old, new)
            return BinaryOp(e.op, left, right)
        if isinstance(e, UnaryOp):
            operand = self._apply_mapping_to_expr(e.operand, old, new)
            return UnaryOp(e.op, operand)
        if isinstance(e, FuncCall):
            # function name should not be remapped; only map args
            args = [self._apply_mapping_to_expr(a, old, new) for a in e.args]
            return FuncCall(e.name, args)
        if isinstance(e, Assignment):
            # assignment used as expression
            # normalize target
            if isinstance(e.target, str):
                if e.target == old:
                    targ = Variable(new)
                else:
                    targ = Variable(e.target)
            else:
                targ = e.target
                if isinstance(targ, Variable) and targ.name == old:
                    targ = Variable(new)
            val = self._apply_mapping_to_expr(e.value, old, new)
            return Assignment(targ, val)
        # fallback: unknown expr type -> return as-is
        return e
