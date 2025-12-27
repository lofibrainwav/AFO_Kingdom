#!/usr/bin/env python3
"""Chancellor Graph 테스트 스크립트"""

import time

try:
    print('Loading Chancellor Graph...')
    start_time = time.time()
    from AFO.chancellor_graph import chancellor_graph
    load_time = time.time() - start_time
    print(f'✅ Chancellor Graph loaded in {load_time:.2f}s')

    # 간단한 테스트 실행
    print('Testing graph invocation...')
    test_start = time.time()
    config = {"configurable": {"thread_id": "test-thread-001"}}
    result = chancellor_graph.invoke({'query': 'test'}, config=config)
    test_time = time.time() - test_start
    print(f'✅ Graph invocation successful in {test_time:.2f}s')
    print(f'Result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}')

except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()