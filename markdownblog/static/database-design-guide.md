[TOC]

数据库开发指南
====

本指南主要针对 MySQL，其他类型RDB可能有小许差异；

!!! note
    hello
    
    hello2
    
        python 1

存储引擎首选 InnoDB
----

InnoDB所有情况下的性能相当或者远超越和MyISAM，因此作为首选引擎。

其他引擎例如Memory也不推荐使用。


字符编码首选 UTF8
----

创建数据库的时候建议：

	CREATE DATABASE `MYDB` DEFAULT CHARACTER SET UTF8;

外部链接：

 - [MySQL - Unicode Character Sets](http://dev.mysql.com/doc/refman/5.5/en/charset-unicode-sets.html)
 - [MySQL - Connection Character Sets and Collations](http://dev.mysql.com/doc/refman/5.5/en/charset-connection.html)

主键选择
----

主键建议为整数，自增型，InnoDB；

如果表记录很少被删除，可以使用 `INT`，否则为 `BIGINT`；

不建议使用UUID等比较长的字符串作为主键，原因如下：

* 主键为随机的时候，InnoDB为随机写，速度较慢；
* InnoDB的索引会包含主键，主键比较大的时候索引也会相应增大，浪费空间；

如果有使用长字符串，例如SHA或者UUID作为主键需求，可以使用唯一索引，然后主键使用自增的INT；


索引选择
----

实测BTree（默认）性能和Hash差不多，并且有范围查找功能，建议选用；

若有排序的查询需求，可考虑索引；


日期类型选择
----

内部生成的，不能被外部修改的时间，例如创建时间，修改时间这种，建议用 `TIMESTAMP`；

外部可修改的时间，用 `DATETIME` ，建议其值为UTC时间；


CHAR/VARCHAR/TEXT 的对比是大小写不敏感的
----

在要求大小写敏感的场合不建议用这几种类型，用 BINARY/VARBINARY/BLOB代替；



查询
----

### 使用索引
除非表很小，否则任何情况下查询都要匹配索引。

要注意索引命中数和结果数的比例不能太高，否则考虑再增加索引，例如下面情况：

查询用户ID为 123 的人的文件中，大小超过 1024bytes 的文件名：

	SELECT `name` FROM `userfile` WHERE `userid`=123 and `size`>1024;

如果表 `userfile` 中普遍用户的文件都不多，可以考虑只用 userid 的索引，
但是如果有些用户可能有10万以上文件，那么这样一条查询，就会对数据库产生10万次随机读，
这时候可以考虑增加 size 的索引；另外，如果大小超过这个值的文件也很多，那么就会一次过返回很多数据，这对数据库性能有很大影响，建议进行分页处理。

	#TODO

使用MySQL的 `EXPLAIN` 命令可以查看你的SQL是否使用索引。



* 使用游标分页
* 使用LIMIT
* 使用escape


命名规则
----

### 数据库名

字母和数字的组合，可以包含下划线，建议使用驼峰式，首字母大写，如 `BookStore` 。

### 表名
字母和数字的组合，可以包含下划线，建议全小写，如 `book` 。

### SQL

> SQL一般情况下建议用 ORM 生成，如果要手写，建议遵从下面规则

SQL关键字用全大小，表名，列表建议加上反引号 <code>\`</code>；

如果确认查询结果只有一条，例如主键，唯一索引查询，可以加上 `LIMIT 1`，
查询时不建议使用 `SELECT *` 

建议：

	SELECT `bid`,`name` FROM `book` WHERE `bid`=1 LIMIT 1;

不推荐：

	SELECT * FROM `book` WHERE `bid`=1;
	select * from `book`;

