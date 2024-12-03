import ast
import inspect
import textwrap
from typing import List, Tuple, Dict, Any, Optional

class GuitarCodeTranslator:
    def __init__(self, time_signature=(4, 4), tempo=120):
        # Basic power chord progressions for common operations
        self.chord_map = {
            'READ': 'E5',
            'WRITE': 'A5',
            'COMPUTE': 'D5',
            'BRANCH': 'G5',
            'LOOP': 'C5'
        }
        
        # Operation patterns for different AST nodes
        self.operation_patterns = {
            ast.Add: ['E5', 'A5'],
            ast.Sub: ['A5', 'D5'],
            ast.Mult: ['D5', 'G5'],
            ast.Div: ['G5', 'C5'],
            ast.Mod: ['C5', 'E5'],
            ast.Compare: ['E5', 'D5', 'A5']
        }
        
        self.time_signature = time_signature  # Tuple of (beats per measure, beat value)
        self.tempo = tempo
        self.current_measure = 1
        self.current_beat = 1
        self.tab_lines = []
	
    def _generate_timing(self) -> str:
	    """Generate timestamp in measure.beat format"""
	    return f"{self.current_measure}.{self.current_beat}"

    def _add_instruction(self, instruction: str, description: str):
        """Add a new instruction to the tab with proper timing"""
        self.tab_lines.append((self._generate_timing(), instruction.ljust(30), description))
        self.current_beat += 1
        if self.current_beat > self.time_signature[0]:
	        self.current_beat = 1
	        self.current_measure += 1

    def _process_operation(self, node: ast.AST) -> List[Tuple[str, str]]:
        """Process mathematical and logical operations"""
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.operation_patterns:
                progression = ' -> '.join(self.operation_patterns[op_type])
                return [(f"{progression} [sustain]", f"Process {op_type.__name__} operation")]
        return []

    def _process_control_flow(self, node: ast.AST) -> List[Tuple[str, str]]:
        """Process control flow statements (if/while/for)"""
        instructions = []
        
        if isinstance(node, ast.If):
            # Read condition
            instructions.append((f"Palm mute {self.chord_map['READ']}", "Read condition"))
            
            # Process condition
            if isinstance(node.test, ast.Compare):
                instructions.append((
                    f"{self.chord_map['BRANCH']} -> {self.chord_map['COMPUTE']} [sustain]",
                    "Evaluate condition"
                ))
                
        elif isinstance(node, (ast.For, ast.While)):
            # Loop initialization
            instructions.append((f"Palm mute {self.chord_map['LOOP']}", "Initialize loop"))
            
        return instructions

    def _process_function_body(self, body: List[ast.AST]) -> None:
        """Process function body nodes"""
        for node in body:
            # Read operation before any computation
            self._add_instruction(f"Palm mute {self.chord_map['READ']}", "Read input")
            
            # Process based on node type
            if isinstance(node, (ast.If, ast.While, ast.For)):
                for instruction, desc in self._process_control_flow(node):
                    self._add_instruction(instruction, desc)
                    
                # Process body recursively
                if hasattr(node, 'body'):
                    self._process_function_body(node.body)
                if hasattr(node, 'orelse'):
                    self._process_function_body(node.orelse)
                    
            elif isinstance(node, ast.Return):
                self._add_instruction(
                    f"{self.chord_map['WRITE']} [sustain]",
                    "Write output and return"
                )
                
            else:
                operations = self._process_operation(node)
                for instruction, desc in operations:
                    self._add_instruction(instruction, desc)

    def translate_function(self, func) -> str:
        """Translate a Python function into guitar tab notation"""
        # Reset state
        self.current_measure = 1
        self.current_beat = 1
        self.tab_lines = []
        
        # Parse function
        source = inspect.getsource(func)
        source = textwrap.dedent(source)
        tree = ast.parse(source)
        
        # Find the function definition
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._process_function_body(node.body)
                break
        
        # Generate tab with configurable time signature
        tab = ["// Guitar Code Translation",
               "// Time signature: {beats_per_measure}/{beat_value}",
               "// Tempo: {self.tempo} BPM",
               "// Standard tuning",
               ""]
        
        for timing, instruction, description in self.tab_lines:
            tab.append(f"{timing} - {instruction} // {description}")
            
        return '\n'.join(tab)

def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return n

translator = GuitarCodeTranslator()
print(translator.translate_function(fizzbuzz))