drop table if exists users;
create table users (
    id integer primary key autoincrement,
    name varchar(60),
    email varchar(255),
    password varchar(255));


drop table if exists events;
create table events (
    id integer primary key autoincrement,
    title varchar(255),
    video_url varchar(255),
    happens_on date,
    message text,
    user_id integer not null
    );
