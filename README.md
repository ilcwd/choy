Choy
====
Choy可以把markdown文件一键生成wiki。

wiki的层级组织和markdown目录的文件夹组织一样。


TODO List
----
* 整合 Git，可以浏览wiki文档的版本历史；
* 文件和目录cache，加快wiki加载；
* 支持自定义网页模板；
* etc.

Support Syntax
----

* Markdown基本语法
* [TOC] - Table of Content
* Meta - 文件前几行可以使用 `Key: Value` 语法
* 目录会自动寻找 `index.md` 并加载作为自己的内容

Run
----

    python -mchoy.run
