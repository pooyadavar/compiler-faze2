from deobfuscator.ast import *
from copy import deepcopy

class InlineReconstructor:
    """
    Heuristic re-constructor: detect small inlined blocks that correspond
    structurally to existing functions and replace them with a single call.
    Works on pattern:
      int a_0 = ARG1;
      int b_1 = ARG2;
      int result_N = (a_0 + b_1);
      target = result_N;
    It will try to find a function whose body (ignoring names) matches
    the small block, and rewrite it into: target = func(ARG1, ARG2);
    """
    def reconstruct(self, prog: Program):
        for func in prog.functions:
            func.body = self._process_block(func.body, prog)

    def _process_block(self, stmts, prog: Program):
        i = 0
        out = []
        while i < len(stmts):
            # try match pattern at i
            match_len, replacement = self._match_inlined_sequence(stmts, i, prog)
            if match_len:
                out.append(replacement)
                i += match_len
            else:
                s = stmts[i]
                if isinstance(s, Block):
                    s.items = self._process_block(s.items, prog)
                out.append(s)
                i += 1
        return out

    def _match_inlined_sequence(self, stmts, idx, prog):
        # minimum seq length check
        # pattern: one or more varDecls that initialize param placeholders,
        # then a varDecl (result), then an Assignment assigning that result to target var
        j = idx
        param_inits = []
        while j < len(stmts) and isinstance(stmts[j], VariableDecl):
            # variable with initializer
            if stmts[j].init_expr is None:
                break
            param_inits.append(stmts[j])
            j += 1
            # break if too many
            if len(param_inits) > 6:
                break
        # need at least two param_inits and then one varDecl result and assignment
        if len(param_inits) < 1 or j >= len(stmts) or not isinstance(stmts[j], Assignment):
            # maybe next is a result varDecl then assignment
            if j < len(stmts) and isinstance(stmts[j], VariableDecl):
                result_decl = stmts[j]
                k = j + 1
                if k < len(stmts) and isinstance(stmts[k], Assignment):
                    # candidate
                    pass
                else:
                    return 0, None
            else:
                return 0, None

        # more robust path: attempt to find sequence: param_inits (>=1), result_decl (VariableDecl),
        # assign_to_target (Assignment where value is Variable(result_decl.name))
        # We'll accept the simpler pattern
        # require at least 2 declarations including result
        if len(param_inits) < 1:
            return 0, None

        # ensure next is result decl
        if j >= len(stmts) or not isinstance(stmts[j], VariableDecl):
            return 0, None
        result_decl = stmts[j]
        k = j + 1
        if k >= len(stmts) or not isinstance(stmts[k], Assignment):
            return 0, None
        assign_stmt = stmts[k]
        # check assignment value is Variable of result_decl.name
        if not isinstance(assign_stmt.value, Variable) or assign_stmt.value.name != result_decl.name:
            # sometimes assignment uses the result value directly; try allowing assignment target = result_decl.init_expr
            # we'll require equality of textual shape - skip for now
            return 0, None

        # we have a candidate sequence length
        seq_len = (k - idx) + 1

        # Build arg expressions from param_inits initializers
        arg_exprs = [d.init_expr for d in param_inits]
        # find matching function in prog whose body equivalently returns combination of params
        candidate = self._find_matching_function(prog, result_decl, param_inits)
        if candidate is None:
            return 0, None

        # build replacement assignment: target = FuncCall(candidate.name, arg_exprs)
        target = assign_stmt.target if isinstance(assign_stmt.target, Variable) else Variable(assign_stmt.target.name if hasattr(assign_stmt.target, 'name') else str(assign_stmt.target))
        new_assign = Assignment(target, FuncCall(candidate.name, arg_exprs))
        return seq_len, new_assign

    def _find_matching_function(self, prog: Program, result_decl: VariableDecl, param_inits):
        """
        Find function whose body structure matches (simple heuristic):
         - function has same number of params as len(param_inits)
         - body has a VariableDecl (result) initialized by BinaryOp using param names
         - then a Return returning that result
        This is narrow but will match many of the small functions produced by the obfuscator.
        """
        for f in prog.functions:
            # skip trivially the same function (we do not want to match self)
            if not f.body:
                continue
            # need same param count
            if len(f.params) != len(param_inits):
                continue
            # try to find in function body a VariableDecl followed by Return of that var
            for idx, s in enumerate(f.body):
                if isinstance(s, VariableDecl) and (idx + 1) < len(f.body) and isinstance(f.body[idx+1], Return):
                    ret = f.body[idx+1]
                    # check returned variable name equals decl name
                    if isinstance(ret.value, Variable) and ret.value.name == s.name:
                        # candidate; now verify initialization uses function params
                        # extract variable names used in s.init_expr
                        names = self._collect_names(s.init_expr)
                        param_names = [p.name for p in f.params]
                        # if param names subset of names, consider match
                        if set(names).intersection(set(param_names)):
                            return f
        return None

    def _collect_names(self, expr):
        if expr is None:
            return set()
        if isinstance(expr, Variable):
            return {expr.name}
        if isinstance(expr, BinaryOp):
            return self._collect_names(expr.left) | self._collect_names(expr.right)
        if isinstance(expr, UnaryOp):
            return self._collect_names(expr.operand)
        if isinstance(expr, FuncCall):
            s = set()
            for a in expr.args:
                s |= self._collect_names(a)
            return s
        return set()
