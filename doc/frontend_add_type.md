# ADD_TYPE.HTML

添加实物资源类别的页面。只有管理员可以访问。

## 显示 FUNCTION

goods.views.show_add_type

## RENDER CONTEXT

+ base.html要求的render context

## 表单ACTION

### 1.goods.views.add_type

添加一个新的物品类别。如果物品类别已经存在，目前应该添加失败。

POST方法

+ **type_name** 实物资源所属类别的名字
+ **pro1_name** 属性1的名字，如果为空字符串，则表示不使用这个属性。
+ ...
+ **pro32_name** 属性32的名字

## AJAX OPERATIONS

无