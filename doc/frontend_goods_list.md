# GOODS_LIST.HTML实物资源列表页面

实物资源的显示页面。对于普通用户，显示所有可以借用的实物资源。对于管理员，则除了借用操作，也可以添加（转到实物添加页面）、修改、销毁或者维护实物资源。

考虑到采购和申购在用户需求中没有提到，我认为我们也没有实现的必要。

## 显示FUNCTION

显示这个页面的view function为:

goods.views.show_list

方法为GET，接受如下参数(对物品列表的筛选参数)

+ **status** 需要显示处于哪些状态的物品，可以取值为：不存在（显示除了已销毁的全部）、all（显示除了已销毁的全部）、available(在库物品)、unavailable(不可用物品)、destroyed(已销毁物品)、borrowed(已借出物品)。
+ **name** 实物资源的名字（应该可以支持搜索、模糊匹配之类的）
+ **type** 筛选的实物资源类型（譬如笔记本电脑、桌子），取值可以为空，空表示没有限制。
+ **pro1_value** 在筛选类型type确定的情况下有意义：属性一的值。属性一的名字是由类别确定的。
+ ...
+ **pro32_value** 属性32的值。

## RENDER CONTEXT

+ base.html需要的所有context
+ **goods_list** 当前筛选状态下的实物资源列表。每个元素有如下属性：
    - **id** 实物资源id
    - **name** 实物资源的名字
    - **type_id** 实物资源所属类型id
    - **type_name** 实物资源所属类型名字
    - **prop** 属性表，共三十二个元素：
        + **pro_name** 属性i的名字
        + **pro_value** 属性i的值
    - **sn** 实物资源sn号
    - **status** 实物资源所处状态，值为：'available'(在库) 'unavailable'(不在库) 'borrowed'(已借出) 'destroyed'(已销毁)
    - **user_id** 使用者id
    - **user_name** 使用者用户名
    - **note** 处在不可用状态时的描述(仅对不可用物品有意义)
+ **type_list** 所有物品类型

## FORM ACTIONS

以下为表单操作，表单提交的action，不是ajax。完成表单操作后应该回到提交该表单的页面。

### 1.goods.views.do_borrow

拥有借用权限的用户提交某个物品的借用申请。

POST方法

+ **id** 实物资源id
+ **note** 申请理由

### 2.goods.views.do_set_unavailable

拥有权限的用户将某个可用物品设为不可用，并给出不可用理由。

POST方法

+ **id** 实物资源id
+ **note** 不可用描述

### 3.goods.views.do_set_available

拥有权限的用户将某个不可用的物品设为可用。

POST方法

+ **id** 实物资源id

### 4.goods.views.do_destroy

拥有权限的用户将某个可用物品销毁。

POST方法

+ **id** 实物资源id

## AJAX OPERATIONS

### 1.goods.views.do_type_props

列出某一个type下的每个属性的属性名称

POST方法

传入参数

+ **type_name** 类别名字

返回参数: json

+ **pro_names** 从属性1到属性32的名字列表。如果没有该属性，则对应项为''
