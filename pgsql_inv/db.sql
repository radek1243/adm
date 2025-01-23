create table host (
    id integer primary key generated always as identity,
    name varchar(20) not null unique,
    ip varchar(15) not null unique
);

create table hostvars (
    id integer generated always as identity primary key,
    name varchar(30) not null,
    value varchar(50) not null,
    hostid int references host(id) on delete cascade
);

create table "group" (
    id integer generated always as identity primary key,
    name varchar(30) not null,
    parent_group_id int references "group"(id) on delete cascade
);

create table groupvars (
    id integer generated always as identity primary key,
    name varchar(30) not null,
    value varchar(50) not null,
    groupid int references "group"(id) on delete cascade
);

create table host_group (
    id integer generated always as identity primary key,
    hostid int references host(id) on delete cascade,
    groupid int references "group"(id) on delete cascade
);
