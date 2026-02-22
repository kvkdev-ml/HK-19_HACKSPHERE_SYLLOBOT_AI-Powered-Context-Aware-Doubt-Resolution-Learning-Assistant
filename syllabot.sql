drop database if exists syllobot;
create database if not exists syllobot;

use syllobot;

drop table if EXISTS user_tb;
create table if not exists user_tb(
    fname varchar(50),
    username varchar(50),
    userpass varchar(50),
    email varchar(50)
);

insert into user_tb values(
    'kvkdev',
    'kvkdev14',
    '12345',
    'something@gmail.com'
);

select * from user_tb;


drop table if exists user_dt;
CREATE TABLE IF NOT EXISTS user_dt (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(50) NOT NULL,
    question TEXT NULL,
    answer TEXT NULL,
    file_name VARCHAR(100) NULL,
    file_type VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from user_tb;