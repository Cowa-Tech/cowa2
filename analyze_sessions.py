import ast
import os

class SessionModificationAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.session_modifications = []

    def visit_Assign(self, node):
        if any(self.is_session_access(target) for target in node.targets):
            self.session_modifications.append(f'Assignment found: {ast.dump(node)}')
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if self.is_session_access(node):
            self.session_modifications.append(f'Session access found: {ast.dump(node)}')
        self.generic_visit(node)

    def is_session_access(self, node):
        if isinstance(node, ast.Attribute):
            return (isinstance(node.value, ast.Name) and node.value.id == 'request' and
                    node.attr in ['session', 'SESSION'])
        return False

def analyze_file(file_path, analyzer):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
        analyzer.visit(tree)

def analyze_project_directory(directory):
    analyzer = SessionModificationAnalyzer()
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    tree = ast.parse(content, filename=file_path)
                    analyzer.visit(tree)
                    for result in analyzer.session_modifications:
                        results.append(f'{file_path}: {result}')
                except Exception as e:
                    print(f'Error processing file {file_path}: {e}')
    return results

if __name__ == '__main__':
    # Use the directory where manage.py is located
    project_directory = os.path.dirname(os.path.abspath(__file__))
    results = analyze_project_directory(project_directory)
    
    if results:
        print('Potential session modification issues found:')
        for result in results:
            print(result)
    else:
        print('No potential session modification issues found.')
