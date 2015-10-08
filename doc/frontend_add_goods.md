# ADD_GOODS.HTML

添加实物资源的页面。只有管理员可以访问。从这个页面可以通过goods.views.show_add_type添加新的类型。

## 显示 FUNCTION

goods.views.show_add_goods

## RENDER CONTEXT

+ base.html要求的render context
+ **type_list** 可选类型列表

## 表单ACTION

### 1.goods.views.add_goods

添加一个新的物品。完成操作后应该回到goods_list.html页面。

POST方法

+ **name** 实物资源名称
+ **type_name** 实物资源所属类别的名字
+ **pro1_value** 属性1的值
+ ...
+ **pro32_value** 属性32的值
+ **sn** 实物资源sn号
+ **quantity** 实物数量

## AJAX OPERATIONS

### 1.goods.views.do_type_props

列出某一个type下的每个属性的属性名称

POST方法

传入参数

+ **type_name** 类别名字

返回参数: json

+ **pro_names** 从属性1到属性32的名字列表。如果没有该属性，则对应项为''
