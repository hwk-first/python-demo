# -*- coding: utf-8 -*-
"""MySQL 数据库配置

请根据本机实际环境修改下面的连接信息（尤其是 password）。
也支持通过环境变量覆盖：MYSQL_HOST / MYSQL_PORT / MYSQL_USER / MYSQL_PASSWORD / MYSQL_DATABASE
"""
import os

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    # TODO: 改成你自己的 MySQL 密码
    'password': os.getenv('MYSQL_PASSWORD', '123456'),
    'database': os.getenv('MYSQL_DATABASE', 'device_manage'),
    'charset': 'utf8mb4',
}
