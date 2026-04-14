from flask import Flask, request, jsonify
from pipelines.finenroll.rag import run_finenroll_query
import time

app = Flask(__name__)

@app.route('/chat/completions', methods=['POST'])
def chat_completions():
    data = request.get_json()
    if not data or 'messages' not in data:
        return jsonify({'error': 'Missing messages in request'}), 400
    
    messages = data['messages']
    if not messages or messages[-1]['role'] != 'user':
        return jsonify({'error': 'Last message must be from user'}), 400
    
    question = messages[-1]['content']
    chat_history_id = data.get('user', 'openai_compat_session')
    
    try:
        response = run_finenroll_query(question, chat_history_id)
        return jsonify({
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": data.get("model", "finenroll-rag"),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1416, debug=True)