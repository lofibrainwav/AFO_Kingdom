#!/usr/bin/env python3

import sys
import os
import subprocess

# Execute organs_truth.py directly as a subprocess to avoid import issues
script_dir = os.path.dirname(__file__)
organs_file = os.path.join(script_dir, 'packages', 'afo-core', 'AFO', 'health', 'organs_truth.py')

if __name__ == "__main__":
    print("Testing organs_truth.py configuration...")

    # Create a minimal test script that imports and runs the function
    test_code = '''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages', 'afo-core'))

# Import the function directly
from AFO.health.organs_truth import build_organs_final

if __name__ == "__main__":
    result = build_organs_final()
    print("Current probe configuration:")
    for organ, data in result['organs'].items():
        if any(keyword in organ for keyword in ['Redis', 'PostgreSQL', 'Ollama', 'Qdrant']):
            print(f"{organ}: {data['probe']}")

    print("")
    env_vars = ['REDIS_HOST', 'POSTGRES_HOST', 'QDRANT_HOST', 'OLLAMA_HOST', 'OLLAMA_BASE_URL']
    for var in env_vars:
        value = os.getenv(var)
        print(f"{var}: {value}")
'''

    # Write and execute the test
    with open('temp_test.py', 'w') as f:
        f.write(test_code)

    try:
        result = subprocess.run([sys.executable, 'temp_test.py'],
                              capture_output=True, text=True, cwd=script_dir)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Failed to run test: {e}")
    finally:
        if os.path.exists('temp_test.py'):
            os.remove('temp_test.py')
