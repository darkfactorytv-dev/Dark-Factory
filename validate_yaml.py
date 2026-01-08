import yaml, sys, os

try:
    filepath = '.github/workflows/test.yml'
    print(f"Checking file: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Primeiro verifique linhas problemáticas
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if '<<' in line and 'EOF' in line:
            print(f"Warning: Line {i} has heredoc: {line}")
    
    # Tente carregar YAML
    data = yaml.safe_load(content)
    
    print("✅ YAML IS VALID!")
    print(f"Workflow name: {data.get('name')}")
    print(f"Number of jobs: {len(data.get('jobs', {}))}")
    
    # Verificar steps
    for job_name, job in data.get('jobs', {}).items():
        print(f"Job: {job_name}")
        print(f"  Steps: {len(job.get('steps', []))}")
        
except yaml.YAMLError as e:
    print(f"❌ YAML ERROR: {e}")
    if hasattr(e, 'problem_mark'):
        mark = e.problem_mark
        print(f"  Line {mark.line+1}, Column {mark.column+1}")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    sys.exit(1)
