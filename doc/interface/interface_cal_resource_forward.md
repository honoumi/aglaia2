#计算资源前端接口

---

##左边栏

>|功能名|接口名|
|:----------:|:---------:|
|服务器状态||
|待审核申请|apply_num|
|待审核释放|release_num|
|使用中资源||

---

##主体内容1——服务器状态

>|功能名|接口名|备注|
|:------:|:------:|:-------:|
|服务器状态数组|server_list|每个服务器server，例如通过server.id获取服务器id|
|服务器address|address|返回string，可编辑|
|服务器id|id|value为string|
|服务器名称|name|value为string|
|服务器状态|status|value为string，“1”代表空闲，“2”代表繁忙，“3”代表不可用（淹、宕，etc）|
|服务器配置|configuration_list|value是配置的数组，每一种配置可通过configuration.name和configuration.config获得配置名称和配置描述|
|使用人数|account_num|获得该服务器账户的人数，value为string|

###按钮：修改 
####方法POST 数据类型text
>|功能名|接口名|备注|
|:------:|:------:|:-------:|
|服务器address|address|返回string，可编辑|
|服务器id|id|返回string，可编辑|
|服务器名称|name|返回string，可编辑|
|服务器状态|status|返回string，选项框，返回“1”代表空闲，“2”代表繁忙，“3”代表不可用（淹、宕，etc）|
|服务器配置|configuration_list|返回配置的数组，每一种配置内有name和config分别是配置名和配置信息，返回的都是string|

---

##主体内容2——待审批申请

>|功能名|接口名|备注|
|:------:|:------:|:-------:|
|待审批申请数组|borrowing_list|每个待审核申请apply，例如通过apply.id获取申请id|
|申请id|id|value为string|
|申请类型|type|value为string，申请实体资源“0”or申请虚拟资源“1”or申请配置调整“2”|
|用户姓名|username|value为string，注意是用户名|
|用户真实姓名|realname|value为string，注意是真实姓名|
|申请理由|note|value为string|
|CPU要求|cpu|value为string|
|内存要求|memory|value为string|
|硬盘类型|disktype|value为string|
|硬盘大小|disk|value为string|
|服务器网络地址|ip|value为string|
|操作系统|os|value为string|
|时间期限|period|value为string，对于申请配置调整不需要显示，此时建议value为“”|
|登陆用户名|login|value为string，这是用户希望能拥有的账号名，如果申请配置调整，不需要显示，此时建议value为“”|
|初始登陆密码|initial_password|value为string，明文，这是用希望的初始登录密码，如果申请配置调整，不不需要显示，此时建议value为“”|

###同意实体机、虚拟机悬浮窗
####方法POST 数据类型text
>|功能名|接口名|备注|
|:----:|:-----:|:------:|
|服务器address|server_address|返回string|
|服务器id|server_id|返回string|
|服务器名称|server_name|返回string|
|登陆用户名|login|返回string，这是管理员创建的账号，可能与申请人希望的账号名有细微差异|
|初始登陆密码|initial_password|返回string，明文，这是管理员创建的初始密码，可能与申请人希望的初始密码有差异|
|说明|message|返回string|

###同意配置调整悬浮窗
####方法POST 数据类型text
>|功能名|接口名|备注|
|:---:|:---:|:----:|
|服务器address|server_address|返回string|
|服务器id|server_id|返回string|
|服务器名称|server_name|返回string|
|说明|message|返回string|

###拒绝悬浮窗
####方法POST 数据类型text
>|功能名|接口名|备注|
|:----:|:-----:|:------:|
|说明|message|返回string|

---

##主体内容3——待审核释放
>|功能名|接口名|备注|
|:---:|:----:|:----:|
|待审核释放信息数组|returning_list||
|申请id|id|value为string|
|申请类型|type|value为string，申请实体资源“0”or申请虚拟资源“1”or申请配置调整“2”|
|用户姓名|username|value为string，注意是用户名|
|用户真实姓名|realname|value为string，注意是真实姓名|
|登陆用户名|login|value为string，这是申请人在服务器上的账号用户名|
|服务器address|server_address|value为string|
|服务器id|server_id|value为string|
|服务器name|server_name|value为string|
|时间期限|period|value为string|
|释放说明|note|value为string|

###同意悬浮窗
####方法POST 数据类型text
>|功能名|接口名|备注|
|:---:|:---:|:----:|
|说明|message|返回string|

###拒绝悬浮窗
####方法POST 数据类型text
>|功能名|接口名|备注|
|:----:|:-----:|:------:|
|说明|message|返回string|

---


##主体内容4——使用中资源
>|功能名|接口名|备注|
|:---:|:----:|:----:|
|使用中信息数组|inuse_list|对于每个使用中的计算资源using（审核通过的，但配置调整通过审核后没有必要显示在这里），例如通过using.username获取使用中资源的申请人用户名|
|申请id|id|value为string|
|申请类型|type|value为string，申请实体资源“0”or申请虚拟资源“1”or申请配置调整“2”|
|用户姓名|username|value为string，注意是用户名|
|用户真实姓名|realname|value为string，注意是真实姓名|
|登陆用户名|login|value为string，这是申请人在服务器上的账号用户名|
|服务器address|server_address|value为string|
|服务器id|server_id|value为string|
|服务器name|server_name|value为string|
|申请理由与答复|note|value为string|
|CPU要求|cpu|value为string|
|内存要求|memory|value为string|
|硬盘类型|disktype|value为string|
|硬盘大小|disk|value为string|
|服务器网络地址|ip|value为string|
|操作系统|os|value为string|
|时间期限|period|value为string|

---














































