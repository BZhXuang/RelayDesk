"""Exercise the running local stack with real model calls (uses API credit)."""
import argparse
import json
from pathlib import Path
from uuid import uuid4

import httpx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:5173/api/python')
    args = parser.parse_args()
    checks = {}
    run_id = uuid4().hex[:12]
    with httpx.Client(base_url=args.url, timeout=55, trust_env=False) as client:
        def request(method, path, **kwargs):
            response = client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

        checks['health'] = request('GET', '/health')['status']
        assert checks['health'] == 'ok'
        checks['knowledge'] = request('GET', '/knowledge/stats')
        checks['embedding'] = request('GET', '/integrations/embedding')
        checks['mcp'] = request('GET', '/integrations/mcp')
        checks['turns'] = []
        conv_id = f'local-smoke-{run_id}'
        messages = [
            '你好，请用一句话介绍你能帮我解决什么问题。',
            '请查询知识库：购买后第5天申请退款，需要满足什么条件，审核和到账各要多久？',
            '我现在要处理登录故障，登录时一直报401错误，请帮我排查。',
        ]
        for message in messages:
            body = {'user_id': f'smoke-{run_id}', 'conv_id': conv_id,
                    'client_request_id': str(uuid4()), 'message': message}
            result = request('POST', '/chat', json=body)
            checks['turns'].append(result)
            print(json.dumps({key: result.get(key) for key in
                              ('intent', 'agent_type', 'status', 'tools_used', 'knowledge_used',
                               'latency_ms', 'response')}, ensure_ascii=False), flush=True)
            assert result['status'] == 'success', result.get('error_code')
            assert result['response'].strip()
            assert result['performance']['llm']['usage_reported_calls'] > 0
            assert result['performance']['llm']['errors'] == 0
            replay = request('POST', '/chat', json=body)
            assert replay['request_id'] == result['request_id']
            assert replay['response'] == result['response']
            trace = request('GET', f"/trace/tool/{result['request_id']}")
            assert trace['found']

        assert checks['turns'][1]['knowledge_used'], 'RAG tool was not used'
        assert checks['turns'][2]['primary_agent'] == 'technical'
        checks['passed'] = True
    output = Path(__file__).resolve().parents[1] / 'data/local/smoke-result.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'PASS: live chat, RAG, technical routing, replay protection and traces. Report: {output}')


if __name__ == '__main__':
    main()
