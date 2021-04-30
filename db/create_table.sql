create table `Person`(
    `primary_id` BIGINT NOT NULL ,             -- 注册者唯一标识
    `phone_number` VARCHAR(13) NOT NULL ,           -- 手机号
    `name` VARCHAR(10) ,                            -- 姓名
    `nickname` VARCHAR(20) NOT NULL ,               -- 昵称
    `password` BINARY(32) NOT NULL ,                -- 密码，二进制类型
    `id` VARCHAR(18),                               -- 身份证号
    `create_time` DATETIME NOT NULL ,               -- 创建账号时间
    `mail` varchar(50) ,                   -- 邮箱
    `is_deleted` BIT(1) default 0 NOT NULL ,        -- 逻辑删除
    PRIMARY KEY (`primary_id`),
    INDEX `nickname_index` (`nickname`)             -- 为昵称创建索引
);

create table `Title`(
    `title_id` BIGINT NOT NULL ,                    -- 一级留言的唯一id
    `title` VARCHAR(255) NOT NULL ,                 -- 主题名称
    `subtitle` VARCHAR(255) ,              -- 副标题文本
    `primary_id` BIGINT NOT NULL ,                  -- 主题发起人id
    `nickname` VARCHAR(20) NOT NULL ,               -- 昵称id，避免每次查询
    `activity` INT NOT NULL ,                       -- 活跃度
    `create_time` DATETIME NOT NULL ,
    `last_modify_time` DATETIME NOT NULL ,          -- 最后一次回答的时间
    PRIMARY KEY (`title_id`),
    INDEX `primary_id_index` (`primary_id`)         -- 为primary_id创建索引，nickname可能不唯一
);

create table `Label`(
    `label_id` INT NOT NULL AUTO_INCREMENT,         -- 标签id，需要int，并自增
    `label` VARCHAR(10) NOT NULL ,                            -- 标签
    `create_time` DATETIME NOT NULL ,
    PRIMARY KEY (`label_id`),
    INDEX `label_index` (`label`)                   -- 为标签创建索引
);

-- 多对多关系
create table `TitleLabel`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `label_id` INT NOT NULL,                        -- 标签id
    `title_id` BIGINT NOT NULL ,               -- 主题id
    `create_time` DATETIME NOT NULL ,
    PRIMARY KEY (`id`)
);

create table `Comment`(
    `comment_id` BIGINT NOT NULL ,             -- 一级留言的唯一id
    `title_id` BIGINT NOT NULL ,               -- 主题id
    `primary_id` BIGINT NOT NULL ,             -- 注册者id
    `nickname` VARCHAR(20) NOT NULL ,               -- 昵称id，避免每次查询
    `text` VARCHAR(255) NOT NULL ,                  -- 留言文本
    `preference` INT NOT NULL ,                     -- 点赞数
    `create_time` DATETIME NOT NULL ,
    PRIMARY KEY (`comment_id`)
);

create table `SecondComment`(
    `second_comment_id` BIGINT NOT NULL ,      -- 二级留言唯一id
    `comment_id` BIGINT NOT NULL ,             -- 留言id
    `primary_id` BIGINT NOT NULL ,             -- 注册者id
    `nickname` VARCHAR(20) NOT NULL ,               -- 昵称id，避免每次查询
    `text` VARCHAR(255) NOT NULL ,                  -- 留言文本
    `preference` INT NOT NULL ,                     -- 点赞数
    `create_time` DATETIME NOT NULL ,
    PRIMARY KEY (`second_comment_id`)
);

create table `Books`(
    `book_id` INT NOT NULL AUTO_INCREMENT,          -- book_id
    `book` VARCHAR(127) NOT NULL ,                  -- 书名
    `alia` VARCHAR(127) NULL,                       -- 别名
    `group` VARCHAR(31)  NULL COMMENT '书组 暂时只为一列',
    `create_time` DATETIME NOT NULL ,               -- 创建时间
    `last_modify_time` DATETIME NOT NULL ,          -- 最后修改的时间
    PRIMARY KEY (`book_id`)
)
