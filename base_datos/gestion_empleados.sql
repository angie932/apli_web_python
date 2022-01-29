create schema sistema;

create table empleados 
(
id int auto_increment primary key, 
nombre char (60),
correo varchar (255),
foto varchar (255)
);

insert into empleados(nombre, correo, foto) values ('angie', 'angietapiero@gmail.com', 'foto2.jpg');
select * from empleados;