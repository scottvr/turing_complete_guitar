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
        # Get source and dedent it
        source = inspect.getsource(func)
        source = textwrap.dedent(source)
        
        tree = ast.parse(source)
        chords = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for stmt in node.body:
                    chords.extend(self._process_node(stmt))
        
        timed_chords = []
        for i, chord in enumerate(chords):
            timing = f"Bar {i//4 + 1}, Beat {i%4 + 1}"
            timed_chords.append((timing, chord))
            
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
for timing, chord in guitar_tab:
    print(f"{timing}: {chord}")