#BORROW.HTML借还管理界面

普通用户借还物资并管理借还请求的界面。

目前阶段仅需要实现计算资源的借还操作。

##RENDER CONTEXT

+ **curpage** 当前页面名称。对于borrow.html取值为'borrow'
+ **num_res_used** 正在使用的计算资源数量
+ **num_res_borrow** 正在申请借用的计算资源数量
+ **num_res_release** 正在申请归还的计算资源数量
+ **num_res_modif** 正在申请修改的计算资源数量
+ **num_goods_used** 正在使用的实物资源数量
+ **num_goods_borrow** 正在申请借用的实物资源数量
+ **num_goods_return** 正在申请归还的实物资源数量
+ **package_list** 可以使用的套餐列表
+ **borrowing_list** 正在借用审核的计算资源列表
    - **id** 该请求id
    - **name** 该请求的名字
    - **note** 管理员与用户相互传递的消息
    - **package_name** 套餐名字
    - **sn** 计算资源SN号
    - **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
    - **cpu** CPU描述
    - **memory** 内存大小
    - **disktype** 硬盘类型
    - **disk** 硬盘大小
    - **ip** 服务器网络地址
    - **os** 操作系统
    - **login** 登录用户名
    - **initial_password** 初始密码 
    - **period** 资源时间限制
+ **inuse_list** 正在使用的计算资源列表
    - **id** 该请求id
    - **name** 该请求的名字
    - **package_name** 套餐名字
    - **sn** 计算资源SN号
    - **note** 管理员与用户相互传递的消息
    - **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
    - **cpu** CPU描述
    - **memory** 内存大小
    - **disktype** 硬盘类型
    - **disk** 硬盘大小
    - **ip** 服务器网络地址
    - **os** 操作系统
    - **login** 登录用户名
    - **initial_password** 初始密码 
    - **period** 资源时间限制
+ **modifying_list** 正在修改审核的计算资源列表
    - **id** 该请求idh
    - **name** 该请求的名字
    - **note** 管理员与用户相互传递的消息
    - **package_name** 套餐名字
    - **sn** 计算资源SN号
    - **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
    - **cpu** CPU描述
    - **memory** 内存大小
    - **disktype** 硬盘类型
    - **disk** 硬盘大小
    - **ip** 服务器网络地址
    - **os** 操作系统
    - **login** 登录用户名
    - **initial_password** 初始密码 
    - **period** 资源时间限制
+ **returning_list** 正在释放审核的计算资源列表
    - **id** 该请求id
    - **name** 该请求的名字
    - **note** 管理员与用户相互传递的消息
    - **package_name** 套餐名字
    - **sn** 计算资源SN号
    - **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
    - **cpu** CPU描述
    - **memory** 内存大小
    - **disktype** 硬盘类型
    - **disk** 硬盘大小
    - **ip** 服务器网络地址
    - **os** 操作系统
    - **login** 登录用户名
    - **initial_password** 初始密码
    - **period** 资源时间限制
+ **goods_borrowing_list** 正在审核借用申请的物品列表（审核尚未通过）
    - **id** 该借用请求id
    - **sn** 借用物品sn号
    - **name** 被借出物品名
    - **note** 管理员消息或者用户说明
+ **goods_borrow_pending_list** 已经审核通过的借用申请的物品列表
    - **id** 该借用请求id
    - **sn** 借用物品sn号
    - **name** 被借出物品名
    - **note** 管理员消息或者用户说明
+ **goods_borrow_failed_list** 审核被拒绝的物品列表
    - **id** 该借用请求id
    - **sn** 借用物品sn号
    - **name** 被借出物品名
    - **note** 管理员消息
+ **goods_inuse_list** 已借用物品列表
    - **id** 该借用请求id
    - **sn** 借用物品sn号
    - **name** 被借出物品名
    - **note** 管理员消息或者用户说明
+ **goods_returning_list** 正在审核归还物品列表(审核尚未通过)
    - **id** 该借用申请id
    - **sn** 借用物品sn号
    - **name** 被借用物品名
    - **note** 管理员消息或者用户说明
+ **goods_repair_list** 待审核维修申请的物品列表
    - **id** 该借用申请id
    - **sn** 借用物品sn号
    - **name** 被借用物品名
    - **note** 管理员消息或者用户说明
+ **goods_repairing_list** 正在维修物品列表
    - **id** 该借用申请id
    - **sn** 借用物品sn号
    - **name** 被借用物品名
    - **note** 管理员消息或者用户说明
+ **goods_repaired_list** 已维修完成物品列表
    - **id** 该借用申请id
    - **sn** 借用物品sn号
    - **name** 被借用物品名
    - **note** 管理员消息或者用户说明

##AJAX OPERATION

###1.computing.views.do_borrow_request

提交计算资源借用申请。

POST方法

传入参数

+ **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
+ **name** 该请求的名字
+ **package_name** 套餐名字
+ **cpu** CPU描述
+ **memory** 内存大小
+ **disktype** 硬盘类型
+ **disk** 硬盘大小
+ **os** 操作系统
+ **reason** 用户的申请说明
+ **period** 资源时间限制（应该是expire时间？）
+ **login** 用户名
+ **initial_password** 初始密码

返回值为字符串

+ **'ok'** 操作完成
+ **'denied'** 操作失败

###2.computing.views.do_return_request

提交计算资源归还申请

POST方法

传入参数

+ **id** 计算资源请求id

返回值为字符串

+ **'ok'** 操作完成
+ **'denied'** 操作失败

###3.computing.views.do_modif_request

提交计算资源修改申请

POST方法

传入参数

+ **id** 计算资源请求id
+ **period** 修改后的截止时间
+ **reason** 修改原因

返回值为字符串

+ **'ok'** 操作完成
+ **'denied'** 操作失败

###4.computing.views.do_get_package

获得某个套餐下的属性值

POST方法

传入参数

+ **name** 套餐名称

传出参数：JSON

- **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
- **cpu** CPU描述
- **memory** 内存大小
- **disktype** 硬盘类型
- **disk** 硬盘大小
- **os** 操作系统




## 表单ACTION

###1.goods.views.do_return_goods

归还实物资源（准确说是提交归还申请，需等待管理员同意归还后由管理员确认归还完成）。

POST方法

传入参数

+ **id** 实物资源id
+ **note** 归还说明

###2.goods.views.do_miss_goods

挂失实物资源（令实物资源进入destroyed状态）

POST方法

传入参数

+ **id** 实物资源id
+ **note** 挂失说明

###3.goods.views.do_repair_goods

维修实物资源

POST方法

传入参数

+ **id** 实物资源id
+ **note** 维修说明



### 3.computing.views.do_set_flag

标记一个计算资源是否包含重要数据。完成后重定向到本页面。

POST方法

传入参数 

+ **id** 同意的计算资源申请id
+ **flag** 是否包含重要数据,'true' or 'false'



