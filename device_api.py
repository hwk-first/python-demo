# -*- coding: utf-8 -*-
"""设备管理接口（MySQL 持久化）

接口列表：
    GET    /api/devices          查询设备列表（可选 name/platform 过滤）
    GET    /api/devices/<id>     查询单个设备
    POST   /api/devices          新增设备
    PUT    /api/devices/<id>     更新设备
    DELETE /api/devices/<id>     删除设备
"""
from flask import Blueprint, request, jsonify

import db

device_bp = Blueprint('device', __name__, url_prefix='/api')


def row_to_device(row):
    """把数据库行转换为前端需要的结构"""
    return {
        'id': row['id'],
        'name': row['name'],
        'platform': row['platform'],
        'model': row['model'],
        'enabled': bool(row['enabled']),
    }


@device_bp.route('/devices', methods=['GET'])
def list_devices():
    name = (request.args.get('name') or '').strip()
    platform = (request.args.get('platform') or '').strip()

    conditions = []
    args = []
    if name:
        conditions.append('name LIKE %s')
        args.append('%' + name + '%')
    if platform:
        conditions.append('platform = %s')
        args.append(platform)

    where = (' WHERE ' + ' AND '.join(conditions)) if conditions else ''

    try:
        rows = db.query('SELECT * FROM device' + where + ' ORDER BY id DESC', args)
        devices = [row_to_device(r) for r in rows]
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {'list': devices, 'total': len(devices)},
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '查询失败: %s' % e}), 500


@device_bp.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    try:
        rows = db.query('SELECT * FROM device WHERE id = %s', (device_id,))
        if not rows:
            return jsonify({'code': 404, 'msg': '设备不存在'}), 404
        return jsonify({'code': 200, 'msg': 'success', 'data': row_to_device(rows[0])})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '查询失败: %s' % e}), 500


@device_bp.route('/devices', methods=['POST'])
def create_device():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    platform = (data.get('platform') or '').strip()
    model = (data.get('model') or '').strip()
    enabled = data.get('enabled', True)

    if not name or not platform or not model:
        return jsonify({'code': 400, 'msg': '姓名、机型、手机型号不能为空'}), 400

    try:
        lastrowid, _ = db.execute(
            'INSERT INTO device (name, platform, model, enabled) VALUES (%s, %s, %s, %s)',
            (name, platform, model, 1 if enabled else 0),
        )
        return jsonify({'code': 200, 'msg': '创建成功', 'data': {'id': lastrowid}})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '创建失败: %s' % e}), 500


@device_bp.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json(silent=True) or {}

    fields = []
    args = []
    if 'name' in data:
        name = (data.get('name') or '').strip()
        if not name:
            return jsonify({'code': 400, 'msg': '姓名不能为空'}), 400
        fields.append('name = %s')
        args.append(name)
    if 'platform' in data:
        platform = (data.get('platform') or '').strip()
        if not platform:
            return jsonify({'code': 400, 'msg': '机型不能为空'}), 400
        fields.append('platform = %s')
        args.append(platform)
    if 'model' in data:
        model = (data.get('model') or '').strip()
        if not model:
            return jsonify({'code': 400, 'msg': '手机型号不能为空'}), 400
        fields.append('model = %s')
        args.append(model)
    if 'enabled' in data:
        fields.append('enabled = %s')
        args.append(1 if data.get('enabled') else 0)

    if not fields:
        return jsonify({'code': 400, 'msg': '没有需要更新的字段'}), 400

    args.append(device_id)
    try:
        _, rowcount = db.execute(
            'UPDATE device SET ' + ', '.join(fields) + ' WHERE id = %s', args
        )
        if rowcount == 0:
            return jsonify({'code': 404, 'msg': '设备不存在'}), 404
        return jsonify({'code': 200, 'msg': '更新成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '更新失败: %s' % e}), 500


@device_bp.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    try:
        _, rowcount = db.execute('DELETE FROM device WHERE id = %s', (device_id,))
        if rowcount == 0:
            return jsonify({'code': 404, 'msg': '设备不存在'}), 404
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '删除失败: %s' % e}), 500
