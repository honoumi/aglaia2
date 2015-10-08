#BASE.HTML页面基本模板API#

base.html是其他页面的基本模板。除了signin.html（以及以后可能有的404.html/permerror.html）等少数页面，其他页面均扩展自base.html。因此，这些页面对应的views也必须支持base.html所要求的操作。

##RENDER CONTEXT##

+ **user** 当前用户对象
    - **username** 用户名
    - **realname** 真实姓名
    - **number** 学工号
    - **type** 用户类型。可能取值为'normal','manager','supervisor'
    - **email** 电子邮件地址
    - **email_verified** 电子邮件是否已经被认证。可能取值为'true'和'false'
    - **tel** 联系电话
    - **depts** 所在部门。字符串列表，每个元素是一个部门的名称。
    - **permissions** 拥有权限列表。每个元素是一个权限的描述。
    - **status** 该用户对象所在状态，可能的取值为'unauth'(未认证),'auth'(已认证), 'deleted'(已销毁)
+ **num_pending_goods** 当前待审核物资请求数量（对管理员可见）
+ **num_pending_comp** 当前待审核计算资源数量（对管理员可见）
+ **num_pending_unauth** 当前未认证用户数量（对管理员可见）

##AJAX OPERATIONS##

###1.do_modify_account###

修改不敏感的账户信息。目前这类信息包括所在部门和联系电话。

POST方法

传入参数

+ **tel** 新电话号码
+ **depts** 新所在部门（以ASCII逗号分隔的字符串）
+ **realname** 新真实姓名（未认证用户可以更改）
+ **number** 新真实姓名（未认证用户可以更改）

返回值为字符串

+ **'ok'** 修改成功
+ **'invalid'** 新信息的不符合格式
+ **'denied'** 没有权限（例如未登录用户访问这个URL，已认证用户不能更改姓名）

###2.do_modify_email###

修改电子邮件。新电子邮件需要经过验证。

POST方法

传入参数

+ **email** 新电子邮件地址

返回值为字符串

+ **'ok'** 修改成功
+ **'invalid'** 电子邮件格式错误
+ **'denied'** 没有权限（例如未登录用户访问这个URL）

###3.do_modify_password###

修改密码。

POST方法

传入参数

+ **old_password** 旧密码
+ **new_password** 新密码

返回值为字符串

+ **'ok'** 修改成功
+ **'mismatch'** 旧密码输入错误
+ **'invalid'** 新密码不符合密码格式要求
+ **'denied'** 没有权限（例如未登录用户访问这个URL）
