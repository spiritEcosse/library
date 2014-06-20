drop table if exists book;

create table book (
  id integer primary key autoincrement,
  title text not null
);

drop table if exists author;

create table author (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists book_and_author;

create table book_and_author (
	id integer primary key autoincrement,
	book_id integer not null,
	author_id integer not null,
	FOREIGN KEY (book_id) REFERENCES book (id),
	FOREIGN KEY (book_id) REFERENCES author (id)
);


insert into book (title) values('Мастер и Маргарита');
insert into book (title) values('Война и мир');
insert into book (title) values('Преступление и наказание');
insert into book (title) values('Анна Каренина');
insert into book (title) values('Мёртвые души');
insert into book (title) values('Евгений Онегин');
insert into book (title) values('Собачье сердце');

insert into author (name) values('Михаил Булгаков');
insert into author (name) values('Лев Толстой');
insert into author (name) values('Федор Достоевский');
insert into author (name) values('Александр Дюма');
insert into author (name) values('Николай Гоголь');
insert into author (name) values('Александр Пушкин');
insert into author (name) values('Александр Грибоедов');

insert into book_and_author (book_id, author_id) values(1, 2);
insert into book_and_author (book_id, author_id) values(1, 3);
insert into book_and_author (book_id, author_id) values(1, 6);

insert into book_and_author (book_id, author_id) values(2, 7);
insert into book_and_author (book_id, author_id) values(2, 2);
insert into book_and_author (book_id, author_id) values(2, 3);

insert into book_and_author (book_id, author_id) values(3, 4);
insert into book_and_author (book_id, author_id) values(3, 3);

insert into book_and_author (book_id, author_id) values(4, 5);
insert into book_and_author (book_id, author_id) values(4, 4);
insert into book_and_author (book_id, author_id) values(4, 2);

insert into book_and_author (book_id, author_id) values(5, 4);

insert into book_and_author (book_id, author_id) values(6, 6);

insert into book_and_author (book_id, author_id) values(7, 7);
insert into book_and_author (book_id, author_id) values(7, 1);



