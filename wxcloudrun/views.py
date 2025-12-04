from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

# 新增导入
import logging
import requests
import numpy as np
# import onnxruntime as ort #暂时注释，在上传模型后再开启
# from PIL import Image #暂时注释
# import io #暂时注释

logger = logging.getLogger('log')

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')

@app.route('/detect', methods=['POST'])
def detect_animal():
    try:
        params = request.get_json()
        if not params or 'fileID' not in params:
            return make_err_response('fileID is required')

        file_id = params['fileID']
        logger.info(f"Received detection request for fileID: {file_id}")

        # 模拟识别过程
        mock_result = {
            "label": "模拟结果: 金毛寻回犬",
            "score": 0.98,
            "fileID": file_id
        }
        
        return make_succ_response(mock_result)

    except Exception as e:
        logger.error(f"Detection error: {e}")
        return make_err_response(str(e))

@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
