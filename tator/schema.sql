drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'code' text not null,
  'text' text not null,
    'IDnum' text not null
);
drop table if exists codes;
create table codes (
  id integer primary key autoincrement,
  'code' text not null,
  'words' text not null,
  'bolds' text not null
);
drop table if exists corpus;
create table corpus (
  id integer primary key autoincrement,
  'word' text not null,
  'count' text not null
);
