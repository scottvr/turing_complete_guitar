import ast
import inspect
import textwrap

class GuitarTranslator:
    def __init__(self):
        self.basic_chords = ['Em', 'G', 'C', 'D', 'Am']
        self.special_progressions = {
            'if': ['Em', 'G'],
            'else': ['Am', 'C'],
            'while': ['D', 'Em', 'D'],
            'return': ['G', 'Em', 'C'],
            'assignment': ['C', 'G'],
        }
        self.operator_maps = {
            'Add': ['G', 'C'],
            'Sub': ['Em', 'Am'],
            'Mult': ['D', 'G'],
            'Div': ['Am', 'Em'],
            'Eq': ['C', 'C'],
        }
    
    def _value_to_chord(self, value):
        if isinstance(value, bool):
            return 'Em' if value else 'Am'
        if isinstance(value, int):
            return self.basic_chords[value % len(self.basic_chords)]
        if isinstance(value, str):
            return self.basic_chords[len(value) % len(self.basic_chords)]
        return 'C'

    def _process_node(self, node):
        if isinstance(node, ast.Num):
            return [self._value_to_chord(node.n)]
        
        elif isinstance(node, ast.Name):
            return [self.basic_chords[hash(node.id) % len(self.basic_chords)]]
        
        elif isinstance(node, ast.Assign):
            chords = []
            chords.extend(self.special_progressions['assignment'])
            chords.extend(self._process_node(node.value))
            return chords
        
        elif isinstance(node, ast.If):
            chords = []
            chords.extend(self.special_progressions['if'])
            chords.extend(self._process_node(node.test))
            for stmt in node.body:
                chords.extend(self._process_node(stmt))
            if node.orelse:
                chords.extend(self.special_progressions['else'])
                for stmt in node.orelse:
                    chords.extend(self._process_node(stmt))
            return chords
        
        elif isinstance(node, ast.Compare):
            chords = []
            chords.extend(self._process_node(node.left))
            chords.extend(self.operator_maps['Eq'])
            for comparator in node.comparators:
                chords.extend(self._process_node(comparator))
            return chords
        
        elif isinstance(node, ast.Return):
            chords = []
            chords.extend(self.special_progressions['return'])
            if node.value:
                chords.extend(self._process_node(node.value))
            return chords
        
        elif isinstance(node, ast.BinOp):
            chords = []
            chords.extend(self._process_node(node.left))
            op_type = type(node.op).__name__
            if op_type in self.operator_maps:
                chords.extend(self.operator_maps[op_type])
            chords.extend(self._process_node(node.right))
            return chords
        
        return ['Em']

    def function_to_guitar(self, func):
        source = inspect.getsource(func)
        source = textwrap.dedent(source)
        
        tree = ast.parse(source)
        timed_chords = []
        
        def add_chord(description, chords):
            for chord in chords:
                timed_chords.append((description, chord))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for stmt in node.body:
                    if isinstance(stmt, ast.If):
                        # For FizzBuzz & Fizz & Buzz checks
                        if isinstance(stmt.test, ast.BoolOp):  # FizzBuzz case
                            add_chord("Testing if divisible by 3 and 5", ['Em', 'G'])
                            add_chord("FizzBuzz case", ['E5', 'A5', 'D5'])
                            add_chord("Return FizzBuzz", self.special_progressions['return'])
                        else:  # Fizz or Buzz case
                            if '3' in ast.dump(stmt.test):
                                add_chord("Testing if divisible by 3", ['Em', 'G'])
                                add_chord("Fizz case", ['E5', 'A5'])
                                add_chord("Return Fizz", self.special_progressions['return'])
                            else:
                                add_chord("Testing if divisible by 5", ['Em', 'G'])
                                add_chord("Buzz case", ['A5', 'D5'])
                                add_chord("Return Buzz", self.special_progressions['return'])
                    elif isinstance(stmt, ast.Return):
                        add_chord("Default case - return number", ['E5'])
                        add_chord("Return statement", self.special_progressions['return'])
        
        return timed_chords

def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return n

# Test it out
translator = GuitarTranslator()
guitar_tab = translator.function_to_guitar(fizzbuzz)
print("// FizzBuzz implementation in power chords")
print("// Time signature: 4/4")
print("// Tempo: 120 BPM")
print("// Base position: Standard tuning")
print()
for description, chord in guitar_tab:
    print(f"// {description}")
    print(f"- {chord} [sustain]")
    print()