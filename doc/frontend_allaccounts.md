#ALLACCOUNTS.HTML用户管理界面API#

##RENDER CONTEXT##

+ **curpage** 当前所在页面的名字。对allaccounts.html取值为'allaccounts'
+ **num_accounts** 该页显示的所有用户的数量
+ **num_pages** 为了显示所有账户所需要的总页数（最小为1）
+ **cur_index** 当前所在页码（从1算起）
+ **accounts** 当前页所需要显示的账户列表
     - **username** 用户名
    - **realname** 真实姓名
    - **number** 学工号
    - **type** 用户类型。可能取值为'normal','manager','supervisor'
    - **email** 电子邮件地址
    - **email_verified** 电子邮件是否已经被认证。可能取值为'true'和'false'
    - **tel** 联系电话
    - **depts** 所在部门。字符串列表，每个元素是一个部门的名称。
    - **status** 该用户对象所在状态，可能的取值为'unauth'(未认证),'auth'(已认证), 'deleted'(已销毁)
+ **all_perms** 所有可能存在的权限的字符串列表。这个列表中权限的下标和每个账号的权限拥有情况的下标应该一致。
+ **filter_type** 用户类型筛选条件。可选值为'all'(所有用户),'unauth'(未认证用户),'auth'(已认证用户)
+ **filter_dept** 部门筛选条件。可选值为部门名称或者None

##AJAX OPERATIONS##

###1.do_approve_account###

审核通过实名认证。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在

###2.do_disapprove_account###

审核驳回实名认证。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在

###3.do_set_manager###

将某个用户设为管理员。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在

###4.do_clear_manager###

取消某个用户的管理员权限。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在

###5.do_delete_account###

删除某个账户。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在

###6.do_get_permissions###

获取某个用户的权限情况。

POST方法

传入参数

+ **username** 待审核用户名

传出参数为json

+ **status** 查询结果状态。可能取值为：
    - **'ok'** 操作完成
    - **'denied'** 没有这个操作权限或者用户名不存在
+ **permissions** 权限列表。每一个元素取值为0或者1。每个元素与同下标的权限名称相对。

###7.do_set_permissions###

修改某个账户的权限。

POST方法

传入参数

+ **username** 待审核用户名
+ **permissions** 一个数字串，每一位数字按顺序和权限名称相对。数字取值为0（无该权限）或者1（有该权限）.

传出参数为字符串

+ **'ok'** 操作完成
+ **'denied'** 没有这个操作权限或者用户名不存在
