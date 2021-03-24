
-- 创建用户 blog，密码是 111111
CREATE USER 'blog'@'localhost' identified by '111111';

-- 创建数据库，存在则不创建
CREATE DATABASE IF NOT EXISTS blog CHARACTER SET utf8mb4;

-- 将数据库 blog 的所有权限都授权给用户 blog
GRANT ALL ON blog.* to 'blog'@'localhost';
GRANT ALL ON blog.* to 'blog'@'%';

-- 允许 blog 用户远程登录
GRANT ALL PRIVILEGES ON blog.* to 'blog'@'%' IDENTIFIED BY '111111' WITH GRANT OPTION;
FLUSH PRIVILEGES;
