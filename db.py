# -*- coding: utf-8 -*-
"""MySQL 连接与基础操作封装"""
import pymysql
from pymysql.cursors import DictCursor

from config import DB_CONFIG


def get_connection():
    """获取一个使用字典游标的数据库连接"""
    return pymysql.connect(cursorclass=DictCursor, **DB_CONFIG)


def query(sql, args=None):
    """执行查询，返回结果列表"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()


def execute(sql, args=None):
    """执行增删改，返回 (lastrowid, rowcount)"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            lastrowid = cur.lastrowid
            rowcount = cur.rowcount
        conn.commit()
        return lastrowid, rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """自动创建数据库和 device 表（首次启动时调用）"""
    server_config = {k: v for k, v in DB_CONFIG.items() if k != 'database'}

    # 1. 连接 MySQL 服务器（不指定库），确保数据库存在
    conn = pymysql.connect(cursorclass=DictCursor, **server_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARACTER SET utf8mb4"
                % DB_CONFIG['database']
            )
        conn.commit()
    finally:
        conn.close()

    # 2. 创建设备表
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS device (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL COMMENT '姓名',
                    platform VARCHAR(20) NOT NULL COMMENT '机型',
                    model VARCHAR(100) NOT NULL COMMENT '手机型号',
                    enabled TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备表'
                """
            )
        conn.commit()
    finally:
        conn.close()
