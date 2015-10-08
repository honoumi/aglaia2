#SIGNIN.HTML用户登录与注册页面API#

##RENDER CONTEXT##

account.views.show_signin()

无context。

##AJAX OPERATION##

###1.do_signin###

对用户名和密码进行验证，并完成登录功能。

POST方法

传入参数

+ *username* 输入的用户名
+ *password* 输入的密码

返回值为字符串

+ *'ok'* 登录成功
+ *'mismatch'* 用户名密码错误，登陆失败

###2.do_lookup_depts###

根据指定的搜索条件搜索出可用的部门名称，并返回这些部门名称。

POST方法

传入参数

+ *keyword* 搜索字符串

返回值为如下json格式

    {
        depts: ['dept1', 'dept2', 'dept3', ...]
    }


###3.do_verify_username###

验证指定用户名是否可用。

POST方法

传入参数

+ *username* 待验证用户名

返回值为字符串

+ *'ok'* 用户名可用
+ *'used'* 用户名已经被使用
+ *'invalid'* 用户名格式错误

###4.do_signup###

注册新用户。

POST方法

传入参数

+ *username* 用户名
+ *password* 明文密码
+ *realname* 真实姓名
+ *number* 学工号
+ *tel* 联系电话
+ *email* 电子邮件
+ *depts* 所在部门（以ASCII逗号分隔的字符串列表）

返回值为字符串

+ *'ok'* 注册成功
+ *'failed'* 注册失败

