from . import api
from flask import current_app, jsonify


def not_found(message="404 未找到相关资源"):
    response = jsonify({
        'error':True,
        'message':message
    })
    # response.status_code = 404  # 根据前端设计
    return response

@api.errorhandler(500)
def internal_server_error(e):
    response = jsonify({
        'error': True,
        'message': "服务器内部错误，稍后重试。感谢联系 %s 反馈！" % current_app.config['MAIL_ADMIN']
    })
    # response.status_code = 500  # 根据前端
    return response


@api.errorhandler(404)
def source_not_found(e):
    return not_found(e.args[0])
