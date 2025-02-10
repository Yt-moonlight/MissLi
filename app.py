from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 获取WEB端口号
port = int(os.getenv("PORT"))

@app.route('/chat', methods=['POST'])
def handle_chat():
    # 获取用户输入
    data = request.get_json()
    user_message = data.get('message')

    # 调用 DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "你是一个英文学习助手，用简洁易懂的英文和用户进行沟通，并附带中文解释。如果用户的英文回答中存在语法错误需要进行纠正。"},
            {"role": "user", "content": user_message}
        ],
        "model": "deepseek-chat",
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 检查 HTTP 错误
        ai_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print("DeepSeek API Error:", e)
        return jsonify({"error": "Failed to get response"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)