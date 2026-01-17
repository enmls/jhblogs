from flask import Flask, render_template, request, jsonify, session, redirect
import io
import contextlib

app = Flask(__name__)
# 如果你使用了 session，必须设置 secret_key
app.secret_key = 'your_secret_key_here' 

# 1. 你的页面路由 (保持不变)
@app.route("/onlinepy")
def onlinepy():
    if "username" not in session:
        return redirect("/login")
    # Flask 会自动去 templates 文件夹里找 Onlinepy.html
    return render_template("Onlinepy.html")

# 2. 运行代码的 API 接口 (新增)
@app.route("/api/run", methods=["POST"])
def run_code():
    # 获取前端传来的 JSON 数据
    data = request.json
    code = data.get('code', '')

    # 捕获 print 输出
    buffer = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(buffer):
            # 执行代码
            exec(code, {})
        
        output = buffer.getvalue()
        return jsonify({
            'output': output,
            'error': None
        })
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        return jsonify({
            'output': buffer.getvalue(),
            'error': error_msg
        }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
