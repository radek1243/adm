create schema inv;

create table inv.host (
    id integer primary key generated always as identity,
    name varchar(20) not null unique,
    ip varchar(15) not null unique
);

create table inv.hostvars (
    name varchar(30) not null,
    value text not null,
    hostid int references inv.host(id) on delete cascade,
    primary key (name, hostid)
);

create table inv.group (
    id integer generated always as identity primary key,
    name varchar(30) not null,
    parent_group_id int references inv.group(id) on delete set null
);

create table inv.groupvars (
    name varchar(30) not null,
    value text not null,
    groupid int references inv.group(id) on delete cascade,
    primary key (name, groupid)
);

create table inv.host_group (
    id integer generated always as identity primary key,
    hostid int references inv.host(id) on delete cascade,
    groupid int references inv.group(id) on delete cascade
);

create or replace procedure inv.add_hostvar(hostname varchar(20), varname varchar(15), varvalue text)
    as $$
    declare hid int;
    begin
        select id into hid from inv.host where name=hostname;
        insert into inv.hostvars (name, value, hostid) values (varname,varvalue,hid);
        commit;
    end;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE inv.add_host_to_group(hostname varchar(20), groupname varchar(30))
	AS $$
	declare hid int;
	declare gid int;
	BEGIN
		select id into hid from inv.host where name=hostname;
		select id into gid from inv.group WHERE name=groupname;
		insert into inv.host_group (hostid, groupid) values (hid,gid);
		commit;
	end;
$$ LANGUAGE plpgsql

CREATE OR REPLACE PROCEDURE inv.add_groupvar(groupname varchar(30), varname varchar(30), varvalue text)
LANGUAGE 'plpgsql'
AS $BODY$
    declare gid int;
    begin
        select id into gid from inv.group where name=groupname;
        insert into inv.groupvars (name, value, groupid) values (varname,varvalue,gid);
        commit;
    end;
$BODY$;