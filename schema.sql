-- 设备管理数据库初始化脚本
-- 说明：db.py 启动时会自动创建数据库和 device 表，本文件仅作手动初始化参考。

CREATE DATABASE IF NOT EXISTS device_manage
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE device_manage;

CREATE TABLE IF NOT EXISTS device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    platform VARCHAR(20) NOT NULL COMMENT '机型',
    model VARCHAR(100) NOT NULL COMMENT '手机型号',
    enabled TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态 1启用 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备表';

-- 可选：插入一些初始测试数据
INSERT INTO device (name, platform, model, enabled) VALUES
('张三', '安卓', 'Xiaomi 14 Pro', 1),
('李四', '苹果', 'iPhone 15 Pro Max', 1),
('王五', '鸿蒙', 'Huawei Mate 60 Pro', 0);
