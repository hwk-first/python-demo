from flask import Flask, request, jsonify
from flask_cors import CORS

#####

from device_api import device_bp
import db

#123
# 初始化 Flask 应用
app = Flask(__name__)
# 解决跨域问题，允许前端访问
CORS(app)

# 注册设备管理接口
app.register_blueprint(device_bp)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 校验规则
    if username == 'admin' and password == '123456':
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'token': 'admin-token-123456',
                'username': username,
            }
        })
    else:
        return jsonify({
            'code': 400,
            'msg': '用户名或密码错误'
        })

# 启动后端服务
if __name__ == '__main__':
    # 首次启动时自动创建数据库和 device 表
    try:
        db.init_database()
        print('MySQL 初始化成功，数据库和 device 表已就绪')
    except Exception as e:
        print('警告：MySQL 初始化失败，请检查 config.py 中的数据库配置：%s' % e)

    # host=0.0.0.0 允许本机访问，port=5000 是后端端口
    app.run(debug=True, port=5000)
