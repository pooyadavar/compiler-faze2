from deobfuscator.ast import *

class ControlFlowSimplifier:


    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if not isinstance(node, ASTNode): return node
        for field, value in vars(node).items():
            if isinstance(value, list):
                new_list = [self.visit(item) for item in value]
                setattr(node, field, new_list)
            elif isinstance(value, ASTNode):
                setattr(node, field, self.visit(value))
        return node

    def _flatten_body(self, body: list) -> list:

        flat_list = []
        for stmt in body:
            if isinstance(stmt, Block):
                flat_list.extend(self._flatten_body(stmt.items))
            else:
                flat_list.append(stmt)
        return flat_list

    def visit_Function(self, node: Function):

        flat_body = self._flatten_body(node.body)

        artifacts = self._find_flattening_artifacts(flat_body)
        if not artifacts:
            return node

        print(f"INFO: Control flow flattening detected in function '{node.name}'. Simplifying...")
        state_var_name, switch_node = artifacts

        code_blocks = self._extract_code_blocks(flat_body)


        reordered_stmts = self._reorder_blocks(switch_node, code_blocks, state_var_name)

        final_body = []
        for stmt in flat_body:
            if isinstance(stmt, VariableDecl):
                if stmt.name != state_var_name:
                    final_body.append(stmt)
        
        final_body.extend(reordered_stmts)
        node.body = final_body
        return node

    def _find_flattening_artifacts(self, body: list):
        for stmt in body:
            if isinstance(stmt, Switch):
                if isinstance(stmt.expr, Variable):
                    return stmt.expr.name, stmt
        return None

    def _extract_code_blocks(self, body: list) -> dict:
        blocks = {}
        current_label = None
        for stmt in body:
            if isinstance(stmt, Label):
                current_label = stmt.name
                blocks[current_label] = []
            elif current_label:
                if not (isinstance(stmt, Goto) and "dispatcher" in stmt.label):
                    blocks[current_label].append(stmt)
        return blocks

    def _reorder_blocks(self, switch_node: Switch, code_blocks: dict, state_var_name: str) -> list:
        state_to_label_map = {}
        for case in switch_node.cases:
            if isinstance(case.value, Literal) and isinstance(case.body, Block) and case.body.items and isinstance(case.body.items[0], Goto):
                state = case.value.value
                label = case.body.items[0].label
                state_to_label_map[state] = label

        current_state = 0
        reordered_body = []
        
        visited_states = set() 

        while current_state in state_to_label_map and current_state not in visited_states:
            visited_states.add(current_state)
            current_label = state_to_label_map[current_state]
            
            if "end" in current_label:
                break
            
            block_stmts = code_blocks.get(current_label, [])
            next_state_found = False
            for stmt in block_stmts:
                
                is_state_update_stmt = False
                
                if isinstance(stmt, ExpressionStmt) and isinstance(stmt.expr, Assignment):
                    
                    assignment_expr = stmt.expr
                    
                    target_name = None
                    if isinstance(assignment_expr.target, Variable):
                        target_name = assignment_expr.target.name
                    elif isinstance(assignment_expr.target, str):
                        target_name = assignment_expr.target
                    
                    if target_name == state_var_name:
                        is_state_update_stmt = True
                        if isinstance(assignment_expr.value, Literal):
                            current_state = assignment_expr.value.value
                            next_state_found = True
                        else:
                            current_state = -1 
                
                
                if not is_state_update_stmt:
                    reordered_body.append(stmt)
                

            if not next_state_found:
                break
                
        return reordered_body