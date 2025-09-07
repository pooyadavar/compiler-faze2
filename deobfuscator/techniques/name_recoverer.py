# deobfuscator/techniques/semantic_name_recoverer.py
from deobfuscator.ast import *
from typing import List, Dict, Set

class SemanticNameRecoverer:
    """
    Combined semantic + recovery renamer:
      - rename function defs to func1, func2... (except skip list)
      - rename params to a,b,c...
      - rename declared locals -> t0,t1.. then friendly names (x,y,m...)
      - rename undeclared-but-used (orphans) -> tN and then friendly names
      - update all function call names to mapped function names
    """

    def __init__(self):
        self.func_count = 0
        self.skip_names = {"main", "printf", "scanf", "puts", "putchar",
                           "strlen", "malloc", "free", "NULL"}
        self.friendly_locals = ["x", "y", "m", "n", "z"]

    def recover(self, prog: Program):
        # 1) Build function name map first (original -> new) so we can update call sites later
        func_name_map: Dict[str, str] = {}
        for f in prog.functions:
            original = f.name
            if original in self.skip_names:
                func_name_map[original] = original
            else:
                self.func_count += 1
                new_name = f"func{self.func_count}"
                func_name_map[original] = new_name
                f.name = new_name

        # 2) For each function, recover local names and params
        for f in prog.functions:
            self._rename_function(f)

        # 3) After all functions renamed, update all function call names across program
        self._update_all_func_calls(prog, func_name_map)

    # -------------------------
    # Per-function renaming
    # -------------------------
    def _rename_function(self, func: Function):
        # 1. Parameter rename: record old -> new and set on Function.params
        param_old = [p.name for p in func.params]
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
        param_map = {old: new for old, new in zip(param_old, param_new)}

        # 2. Collect declared locals (declaration order)
        declared = list(self._collect_declared_names(func.body))
        # Ensure params considered declared
        declared_set = set(declared) | set(param_new)

        # 3. Collect used identifiers in first-appearance order
        used_ordered = self._collect_used_ordered(func.body)

        # 4. Detect undeclared-but-used identifiers (orphans)
        undeclared = []
        seen = set()
        for name in used_ordered:
            if name in declared_set:
                continue
            if name in param_old:  # original parameter name, ignore (we'll apply param_map later)
                continue
            if name in seen:
                continue
            seen.add(name)
            undeclared.append(name)

        # 5. Build mapping for declared locals -> t0,t1...
        mapping_temp: Dict[str, str] = {}
        counter = 0
        for name in declared:
            if name in self.skip_names:
                continue
            if name.startswith("unused"):
                mapping_temp[name] = f"_unused_{counter}"
            else:
                mapping_temp[name] = f"t{counter}"
            counter += 1

        # 6. Continue counter for undeclared (orphans)
        for name in undeclared:
            if name in mapping_temp or name in self.skip_names:
                continue
            if name.startswith("unused"):
                mapping_temp[name] = f"_unused_{counter}"
            else:
                mapping_temp[name] = f"t{counter}"
            counter += 1

        # 7. Apply t-mapping (normalize both declarations and uses)
        for old, new in mapping_temp.items():
            self._apply_mapping_to_block(func.body, old, new)

        # 8. Convert tN -> friendly names (avoid collision with params)
        t_names = [v for k, v in sorted(mapping_temp.items(), key=lambda kv: int(kv[1][1:]) if kv[1].startswith('t') else 10**9)]
        # Keep ordering unique and t* only
        t_names_filtered = [t for t in t_names if t.startswith("t")]
        local_map: Dict[str, str] = {}
        used_final = set(param_new)
        idx = 0
        for t in t_names_filtered:
            chosen = None
            if idx < len(self.friendly_locals):
                cand = self.friendly_locals[idx]
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

        # 9. Finally propagate parameter renaming to the body
        for old, new in param_map.items():
            self._apply_mapping_to_block(func.body, old, new)

    # -------------------------
    # Helper collectors
    # -------------------------
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
        def add(n):
            if not n:
                return
            if n not in seen:
                seen.add(n); order.append(n)
        def walk_expr(e):
            if e is None: return
            if isinstance(e, Variable):
                add(e.name)
            elif isinstance(e, str):
                add(e)
            elif isinstance(e, BinaryOp):
                walk_expr(e.left); walk_expr(e.right)
            elif isinstance(e, UnaryOp):
                walk_expr(e.operand)
            elif isinstance(e, FuncCall):
                # include function name usage too? we will handle function mapping separately
                for a in e.args: walk_expr(a)
            elif isinstance(e, Assignment):
                if isinstance(e.target, Variable): add(e.target.name)
                elif isinstance(e.target, str): add(e.target)
                walk_expr(e.value)
        def walk_stmt(s):
            if s is None: return
            if isinstance(s, VariableDecl):
                if s.init_expr: walk_expr(s.init_expr)
            elif isinstance(s, Assignment):
                if isinstance(s.target, Variable): add(s.target.name)
                elif isinstance(s.target, str): add(s.target)
                walk_expr(s.value)
            elif isinstance(s, ExpressionStmt):
                walk_expr(s.expr)
            elif isinstance(s, Return):
                walk_expr(s.value)
            elif isinstance(s, IfStmt):
                walk_expr(s.condition); walk_stmt(s.then_branch)
                if s.else_branch: walk_stmt(s.else_branch)
            elif isinstance(s, WhileStmt):
                walk_expr(s.condition); walk_stmt(s.body)
            elif isinstance(s, ForStmt):
                if s.init: walk_expr(s.init)
                if s.cond: walk_expr(s.cond)
                if s.update: walk_expr(s.update)
                walk_stmt(s.body)
            elif isinstance(s, Block):
                for it in s.items: walk_stmt(it)
            elif isinstance(s, Print):
                for a in s.args: walk_expr(a)
            elif isinstance(s, Switch):
                walk_expr(s.expr)
                for case in s.cases:
                    if case.body and isinstance(case.body, Block):
                        for st in case.body.items:
                            walk_stmt(st)
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
        if isinstance(e, str):
            # raw identifier string: convert to Variable (rename if needed)
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
            # keep function name as-is here (function name mapping is applied globally later)
            args = [self._apply_mapping_to_expr(a, old, new) for a in e.args]
            return FuncCall(e.name, args)
        if isinstance(e, Assignment):
            # normalize target
            targ = e.target
            if isinstance(targ, str):
                if targ == old:
                    targ = Variable(new)
                else:
                    targ = Variable(targ)
            elif isinstance(targ, Variable) and targ.name == old:
                targ = Variable(new)
            val = self._apply_mapping_to_expr(e.value, old, new)
            return Assignment(targ, val)
        return e

    # -------------------------
    # Function call name update (global)
    # -------------------------
    def _update_all_func_calls(self, prog: Program, func_name_map: Dict[str, str]):
        # walk all functions and replace function call names
        for f in prog.functions:
            new_items = []
            for s in f.body:
                new_items.append(self._replace_func_calls_in_stmt(s, func_name_map))
            f.body = new_items

    def _replace_func_calls_in_stmt(self, s, func_name_map: Dict[str, str]):
        if s is None:
            return s
        if isinstance(s, VariableDecl):
            if s.init_expr:
                s.init_expr = self._replace_func_calls_in_expr(s.init_expr, func_name_map)
            return s
        if isinstance(s, Assignment):
            s.value = self._replace_func_calls_in_expr(s.value, func_name_map)
            return s
        if isinstance(s, ExpressionStmt):
            s.expr = self._replace_func_calls_in_expr(s.expr, func_name_map)
            return s
        if isinstance(s, Return):
            s.value = self._replace_func_calls_in_expr(s.value, func_name_map)
            return s
        if isinstance(s, IfStmt):
            s.condition = self._replace_func_calls_in_expr(s.condition, func_name_map)
            s.then_branch = self._replace_func_calls_in_stmt(s.then_branch, func_name_map)
            if s.else_branch:
                s.else_branch = self._replace_func_calls_in_stmt(s.else_branch, func_name_map)
            return s
        if isinstance(s, WhileStmt):
            s.condition = self._replace_func_calls_in_expr(s.condition, func_name_map)
            s.body = self._replace_func_calls_in_stmt(s.body, func_name_map)
            return s
        if isinstance(s, ForStmt):
            if s.init: s.init = self._replace_func_calls_in_expr(s.init, func_name_map)
            if s.cond: s.cond = self._replace_func_calls_in_expr(s.cond, func_name_map)
            if s.update: s.update = self._replace_func_calls_in_expr(s.update, func_name_map)
            s.body = self._replace_func_calls_in_stmt(s.body, func_name_map)
            return s
        if isinstance(s, Block):
            s.items = [self._replace_func_calls_in_stmt(it, func_name_map) for it in s.items]
            return s
        if isinstance(s, Print):
            s.args = [self._replace_func_calls_in_expr(a, func_name_map) for a in s.args]
            return s
        if isinstance(s, Switch):
            s.expr = self._replace_func_calls_in_expr(s.expr, func_name_map)
            for case in s.cases:
                if case.body and isinstance(case.body, Block):
                    case.body.items = [self._replace_func_calls_in_stmt(st, func_name_map) for st in case.body.items]
            return s
        return s

    def _replace_func_calls_in_expr(self, e, func_name_map: Dict[str, str]):
        if e is None:
            return None
        if isinstance(e, Variable):
            return e
        if isinstance(e, BinaryOp):
            return BinaryOp(e.op,
                            self._replace_func_calls_in_expr(e.left, func_name_map),
                            self._replace_func_calls_in_expr(e.right, func_name_map))
        if isinstance(e, UnaryOp):
            return UnaryOp(e.op, self._replace_func_calls_in_expr(e.operand, func_name_map))
        if isinstance(e, FuncCall):
            name = e.name
            if name in func_name_map:
                name = func_name_map[name]
            return FuncCall(name, [self._replace_func_calls_in_expr(a, func_name_map) for a in e.args])
        if isinstance(e, Assignment):
            targ = e.target
            if isinstance(targ, str):
                targ = Variable(targ)
            elif isinstance(targ, Variable):
                targ = targ
            return Assignment(targ, self._replace_func_calls_in_expr(e.value, func_name_map))
        return e


# from deobfuscator.ast import *

# class SemanticRenamer:
#     """
#     AST-based semantic renamer.
#     Replaces variable and function names with cleaner, consistent names
#     while skipping reserved/standard identifiers.
#     """

#     def __init__(self):
#         self.name_map = {}      # original -> new name
#         self.func_count = 0
#         self.var_count = 0
#         self.skip_names = {"main", "printf", "scanf", "puts", "putchar", "strlen", "malloc", "free", "NULL"}

#     def rename(self, prog: Program):
#         for func in prog.functions:
#             self._rename_function(func)

#     def _generate_func_name(self, original):
#         if "print" in original.lower():
#             return "printHelper"
#         self.func_count += 1
#         return f"func{self.func_count}"

#     def _generate_var_name(self, original):
#         base_names = ["x", "y", "z", "a", "b", "c"]
#         if self.var_count < len(base_names):
#             name = base_names[self.var_count]
#         else:
#             name = f"var{self.var_count}"
#         self.var_count += 1
#         return name

#     def _rename_function(self, func: Function):
#         # rename function name
#         if func.name not in self.skip_names:
#             func.name = self._rename(func.name, is_func=True)

#         # rename parameters
#         for p in func.params:
#             if p.name not in self.skip_names:
#                 p.name = self._rename(p.name, is_func=False)

#         # rename inside body
#         self._rename_block(func.body)

#     def _rename_block(self, stmts):
#         for stmt in stmts:
#             self._rename_stmt(stmt)

#     def _rename_stmt(self, s):
#         if isinstance(s, VariableDecl):
#             if s.name not in self.skip_names:
#                 s.name = self._rename(s.name, is_func=False)
#             if s.init_expr:
#                 s.init_expr = self._rename_expr(s.init_expr)
#         elif isinstance(s, Assignment):
#             if isinstance(s.target, Variable):
#                 if s.target.name not in self.skip_names:
#                     s.target.name = self._rename(s.target.name)
#             elif isinstance(s.target, str):
#                 s.target = Variable(self._rename(s.target))
#             s.value = self._rename_expr(s.value)
#         elif isinstance(s, ExpressionStmt):
#             if s.expr:
#                 s.expr = self._rename_expr(s.expr)
#         elif isinstance(s, Return):
#             if s.value:
#                 s.value = self._rename_expr(s.value)
#         elif isinstance(s, IfStmt):
#             s.condition = self._rename_expr(s.condition)
#             self._rename_stmt(s.then_branch)
#             if s.else_branch:
#                 self._rename_stmt(s.else_branch)
#         elif isinstance(s, WhileStmt):
#             s.condition = self._rename_expr(s.condition)
#             self._rename_stmt(s.body)
#         elif isinstance(s, ForStmt):
#             if s.init: s.init = self._rename_expr(s.init)
#             if s.cond: s.cond = self._rename_expr(s.cond)
#             if s.update: s.update = self._rename_expr(s.update)
#             self._rename_stmt(s.body)
#         elif isinstance(s, Block):
#             self._rename_block(s.items)
#         elif isinstance(s, Print):
#             s.args = [self._rename_expr(a) for a in s.args]

#     def _rename_expr(self, e):
#         if e is None:
#             return None
#         if isinstance(e, Variable):
#             return Variable(self._rename(e.name))
#         if isinstance(e, BinaryOp):
#             return BinaryOp(e.op, self._rename_expr(e.left), self._rename_expr(e.right))
#         if isinstance(e, UnaryOp):
#             return UnaryOp(e.op, self._rename_expr(e.operand))
#         if isinstance(e, FuncCall):
#             new_name = self._rename(e.name, is_func=True) if e.name not in self.skip_names else e.name
#             return FuncCall(new_name, [self._rename_expr(a) for a in e.args])
#         return e

#     def _rename(self, original, ctx=None, is_func=False):
#         if original in self.skip_names:
#             return original
#         if original not in self.name_map:
#             if is_func:
#                 self.name_map[original] = self._generate_func_name(original)
#             else:
#                 self.name_map[original] = self._generate_var_name(original)
#         return self.name_map[original]







# # # deobfuscator/techniques/name_recoverer.py
# # from typing import List, Set, Dict
# # from deobfuscator.ast import *

# # # do not remap these
# # _BUILTINS = {"printf", "scanf", "true", "false"}

# # class NameRecoverer:
# #     """
# #     Robust name recovery:
# #       - rename function parameters to a,b,c...
# #       - detect undeclared used identifiers and map them to t0,t1...
# #       - convert first few temps to friendly names (x,y,m,...)
# #       - apply mappings everywhere, handling both Variable nodes and raw str identifiers
# #     """

# #     def recover(self, prog: Program):
# #         for func in prog.functions:
# #             self._rename_function(func)

# #     def _rename_function(self, func: Function):
# #         # 1) capture original parameter names
# #         param_old = [p.name for p in func.params]

# #         # 2) create new parameter names and set them on Function.params
# #         param_new = []
# #         for i, p in enumerate(func.params):
# #             if i == 0:
# #                 new = "a"
# #             elif i == 1:
# #                 new = "b"
# #             elif i == 2:
# #                 new = "c"
# #             else:
# #                 new = f"p{i}"
# #             param_new.append(new)
# #             p.name = new

# #         # map old param name -> new param name
# #         param_old_to_new = {old: new for old, new in zip(param_old, param_new)}

# #         # 3) collect declared local names (not including params)
# #         declared = set(self._collect_declared_names(func.body))
# #         # include param new names so they are treated as declared
# #         declared.update(param_new)

# #         # 4) collect used identifier names in order of first appearance
# #         used_ordered = self._collect_used_ordered(func.body)

# #         # filter out builtins and function name itself
# #         used_ordered = [u for u in used_ordered if u not in _BUILTINS and u != func.name]

# #         # 5) detect undeclared-but-used names (exclude param_old to avoid mapping params)
# #         undeclared = []
# #         seen = set()
# #         for name in used_ordered:
# #             if name in declared: 
# #                 continue
# #             if name in param_old:  # a true parameter name in body - don't treat as undeclared
# #                 continue
# #             if name in seen:
# #                 continue
# #             seen.add(name)
# #             undeclared.append(name)

# #         # 6) map undeclared -> t0,t1,...
# #         temp_map: Dict[str, str] = {}
# #         counter = 0
# #         for u in undeclared:
# #             if u.startswith("unused_"):
# #                 temp_map[u] = f"_unused_{counter}"
# #                 counter += 1
# #                 continue
# #             temp_map[u] = f"t{counter}"
# #             counter += 1

# #         # 7) apply temp_map (rename "orphans" -> tX) first
# #         for old, new in temp_map.items():
# #             self._apply_mapping_to_block(func.body, old, new)

# #         # 8) convert tX -> friendly local names, avoiding param names
# #         friendly = ["x", "y", "m", "n", "z"]
# #         t_names = sorted(set(temp_map.values()))
# #         local_map: Dict[str, str] = {}
# #         used_final = set(param_new)  # avoid collisions with param names
# #         idx = 0
# #         for t in t_names:
# #             chosen = None
# #             if idx < len(friendly):
# #                 cand = friendly[idx]
# #                 if cand not in used_final:
# #                     chosen = cand
# #             if not chosen:
# #                 # fallback to v#
# #                 k = 0
# #                 while True:
# #                     cand = f"v{k}"
# #                     if cand not in used_final:
# #                         chosen = cand
# #                         break
# #                     k += 1
# #             local_map[t] = chosen
# #             used_final.add(chosen)
# #             idx += 1

# #         for old, new in local_map.items():
# #             self._apply_mapping_to_block(func.body, old, new)

# #         # 9) finally apply param_old -> param_new mapping to body (last step)
# #         # This ensures original parameter identifiers are restored to a,b inside body.
# #         for old, new in param_old_to_new.items():
# #             self._apply_mapping_to_block(func.body, old, new)

# #     # -------------------------
# #     # Collectors
# #     # -------------------------
# #     def _collect_declared_names(self, stmts) -> List[str]:
# #         names = []
# #         for s in stmts:
# #             if isinstance(s, VariableDecl):
# #                 names.append(s.name)
# #             elif isinstance(s, Block):
# #                 names.extend(self._collect_declared_names(s.items))
# #             elif isinstance(s, IfStmt):
# #                 # in many ASTs then_branch may be Block or Statement
# #                 names.extend(self._collect_declared_names([s.then_branch]))
# #                 if s.else_branch:
# #                     names.extend(self._collect_declared_names([s.else_branch]))
# #             elif isinstance(s, WhileStmt):
# #                 names.extend(self._collect_declared_names([s.body]))
# #             elif isinstance(s, ForStmt):
# #                 names.extend(self._collect_declared_names([s.body]))
# #         return names

# #     def _collect_used_ordered(self, stmts) -> List[str]:
# #         seen = set()
# #         order = []
# #         def add(n):
# #             if n is None:
# #                 return
# #             if n not in seen:
# #                 seen.add(n); order.append(n)
# #         def walk_expr(e):
# #             if e is None:
# #                 return
# #             if isinstance(e, Variable):
# #                 add(e.name)
# #             elif isinstance(e, str):
# #                 # raw identifier string
# #                 add(e)
# #             elif isinstance(e, BinaryOp):
# #                 walk_expr(e.left); walk_expr(e.right)
# #             elif isinstance(e, UnaryOp):
# #                 walk_expr(e.operand)
# #             elif isinstance(e, FuncCall):
# #                 # do not add function name, only arguments
# #                 for a in e.args: walk_expr(a)
# #             elif isinstance(e, Assignment):
# #                 # assignment-as-expression
# #                 if isinstance(e.target, Variable):
# #                     add(e.target.name)
# #                 elif isinstance(e.target, str):
# #                     add(e.target)
# #                 walk_expr(e.value)
# #         def walk_stmt(s):
# #             if s is None:
# #                 return
# #             if isinstance(s, VariableDecl):
# #                 if s.init_expr:
# #                     walk_expr(s.init_expr)
# #             elif isinstance(s, Assignment):
# #                 if isinstance(s.target, Variable):
# #                     add(s.target.name)
# #                 elif isinstance(s.target, str):
# #                     add(s.target)
# #                 walk_expr(s.value)
# #             elif isinstance(s, ExpressionStmt):
# #                 walk_expr(s.expr)
# #             elif isinstance(s, Return):
# #                 walk_expr(s.value)
# #             elif isinstance(s, IfStmt):
# #                 walk_expr(s.condition)
# #                 walk_stmt(s.then_branch)
# #                 if s.else_branch:
# #                     walk_stmt(s.else_branch)
# #             elif isinstance(s, WhileStmt):
# #                 walk_expr(s.condition)
# #                 walk_stmt(s.body)
# #             elif isinstance(s, ForStmt):
# #                 if s.init: walk_expr(s.init)
# #                 if s.cond: walk_expr(s.cond)
# #                 if s.update: walk_expr(s.update)
# #                 walk_stmt(s.body)
# #             elif isinstance(s, Block):
# #                 for it in s.items:
# #                     walk_stmt(it)
# #             elif isinstance(s, Print):
# #                 for a in s.args: walk_expr(a)
# #             elif isinstance(s, Switch):
# #                 walk_expr(s.expr)
# #                 for case in s.cases:
# #                     if case.body and isinstance(case.body, Block):
# #                         for st in case.body.items:
# #                             walk_stmt(st)
# #             # unknown node types ignored
# #         for st in stmts:
# #             walk_stmt(st)
# #         return order

# #     # -------------------------
# #     # Mapping application (robust)
# #     # -------------------------
# #     def _apply_mapping_to_block(self, stmts, old: str, new: str):
# #         for i, s in enumerate(stmts):
# #             stmts[i] = self._apply_mapping_to_stmt(s, old, new)

# #     def _apply_mapping_to_stmt(self, s, old: str, new: str):
# #         if s is None:
# #             return s
# #         if isinstance(s, VariableDecl):
# #             if s.name == old:
# #                 s.name = new
# #             if s.init_expr:
# #                 s.init_expr = self._apply_mapping_to_expr(s.init_expr, old, new)
# #             return s
# #         if isinstance(s, Assignment):
# #             # normalize string targets
# #             if isinstance(s.target, str):
# #                 if s.target == old:
# #                     s.target = Variable(new)
# #                 else:
# #                     s.target = Variable(s.target)
# #             elif isinstance(s.target, Variable):
# #                 if s.target.name == old:
# #                     s.target.name = new
# #             s.value = self._apply_mapping_to_expr(s.value, old, new)
# #             return s
# #         if isinstance(s, ExpressionStmt):
# #             if isinstance(s.expr, Assignment):
# #                 # assignment inside expression
# #                 if isinstance(s.expr.target, str) and s.expr.target == old:
# #                     return None  # assignment to old (maybe unused_) -> remove entirely
# #                 s.expr = self._apply_mapping_to_expr(s.expr, old, new)
# #             else:
# #                 s.expr = self._apply_mapping_to_expr(s.expr, old, new)
# #             return s
# #         if isinstance(s, Return):
# #             s.value = self._apply_mapping_to_expr(s.value, old, new)
# #             return s
# #         if isinstance(s, IfStmt):
# #             s.condition = self._apply_mapping_to_expr(s.condition, old, new)
# #             s.then_branch = self._apply_mapping_to_stmt(s.then_branch, old, new)
# #             if s.else_branch:
# #                 s.else_branch = self._apply_mapping_to_stmt(s.else_branch, old, new)
# #             return s
# #         if isinstance(s, WhileStmt):
# #             s.condition = self._apply_mapping_to_expr(s.condition, old, new)
# #             s.body = self._apply_mapping_to_stmt(s.body, old, new)
# #             return s
# #         if isinstance(s, ForStmt):
# #             if s.init: s.init = self._apply_mapping_to_expr(s.init, old, new)
# #             if s.cond: s.cond = self._apply_mapping_to_expr(s.cond, old, new)
# #             if s.update: s.update = self._apply_mapping_to_expr(s.update, old, new)
# #             s.body = self._apply_mapping_to_stmt(s.body, old, new)
# #             return s
# #         if isinstance(s, Block):
# #             new_items = []
# #             for it in s.items:
# #                 mapped = self._apply_mapping_to_stmt(it, old, new)
# #                 if mapped is None:
# #                     continue
# #                 new_items.append(mapped)
# #             s.items = new_items
# #             return s
# #         if isinstance(s, Print):
# #             s.args = [self._apply_mapping_to_expr(a, old, new) for a in s.args]
# #             return s
# #         if isinstance(s, Switch):
# #             s.expr = self._apply_mapping_to_expr(s.expr, old, new)
# #             for case in s.cases:
# #                 if case.body and isinstance(case.body, Block):
# #                     new_items = []
# #                     for st in case.body.items:
# #                         mapped = self._apply_mapping_to_stmt(st, old, new)
# #                         if mapped is None:
# #                             continue
# #                         new_items.append(mapped)
# #                     case.body.items = new_items
# #             return s
# #         return s

# #     def _apply_mapping_to_expr(self, e, old: str, new: str):
# #         if e is None:
# #             return None
# #         # raw identifier string: convert to Variable node (and rename if needed)
# #         if isinstance(e, str):
# #             if e == old:
# #                 return Variable(new)
# #             return Variable(e)
# #         if isinstance(e, Variable):
# #             if e.name == old:
# #                 return Variable(new)
# #             return e
# #         if isinstance(e, BinaryOp):
# #             left = self._apply_mapping_to_expr(e.left, old, new)
# #             right = self._apply_mapping_to_expr(e.right, old, new)
# #             return BinaryOp(e.op, left, right)
# #         if isinstance(e, UnaryOp):
# #             operand = self._apply_mapping_to_expr(e.operand, old, new)
# #             return UnaryOp(e.op, operand)
# #         if isinstance(e, FuncCall):
# #             # function name should not be remapped; only map args
# #             args = [self._apply_mapping_to_expr(a, old, new) for a in e.args]
# #             return FuncCall(e.name, args)
# #         if isinstance(e, Assignment):
# #             # assignment used as expression
# #             # normalize target
# #             if isinstance(e.target, str):
# #                 if e.target == old:
# #                     targ = Variable(new)
# #                 else:
# #                     targ = Variable(e.target)
# #             else:
# #                 targ = e.target
# #                 if isinstance(targ, Variable) and targ.name == old:
# #                     targ = Variable(new)
# #             val = self._apply_mapping_to_expr(e.value, old, new)
# #             return Assignment(targ, val)
# #         # fallback: unknown expr type -> return as-is
# #         return e
