# CALC_RESOURCE.HTML 计算资源审核页面

## 显示函数

computing.views.show_calc_resource

## RENDER CONTEXT
+ **borrowing_list** 借用申请审核列表
    - **id** 该请求id
    - **name** 该请求的名字
    - **flag** 重要资源
    - **package_name** 套餐名字
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
+ **returning_list** 归还申请审核列表
    - **id** 该请求id
    - **sn** 该计算资源SN号
    - **name** 该请求的名字
    - **flag** 重要资源
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
+ **modifying_list** 修改申请审核列表
    - **id** 该请求id
    - **name** 该请求的名字
    - **sn** 该计算资源SN号
    - **flag** 重要资源
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
+ **inuse_list** 使用中计算资源
    - **id** 该请求id
    - **name** 该请求的名字
    - **sn** 该计算资源SN号
    - **flag** 重要资源
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
+ **package_list** 套餐列表
    - **name** 套餐名字
    - **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
    - **cpu** CPU描述
    - **memory** 内存大小
    - **disktype** 硬盘类型
    - **disk** 硬盘大小
    - **os** 操作系统

## 表单操作

### 1.computing.views.do_approve_borrow

同意一个计算资源的借用申请。完成后重定向到本页面。

POST方法

传入参数

+ **id** 同意的计算资源申请id
+ **sn** 该计算资源的SN号
+ **note** 管理员消息
+ **initial_password** 初始登陆密码
+ **login** 登陆用户名
+ **ip** IP地址

### 2.computing.views.do_disapprove_borrow

拒绝一个计算资源的借用申请。完成后重定向到本页面。

POST方法

传入参数

+ **id**  拒绝的计算资源申请id
+ **note** 管理员消息

### 3.computing.views.do_approve_return

同意一个计算资源的归还申请。完成后重定向到本页面。

POST方法

传入参数 

+ **id** 同意的计算资源申请id
+ **note** 管理员消息

### 4.computing.views.do_approve_modify

同意一个计算资源的修改申请。完成后重定向到本页面。

POST方法

传入参数

- **id** 同意的计算资源申请id
- **flag** 重要资源
- **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
- **cpu** CPU描述
- **memory** 内存大小
- **disktype** 硬盘类型
- **disk** 硬盘大小
- **ip** 服务器网络地址
- **os** 操作系统
- **period** 资源时间限制
- **note** 管理员消息

### 5.computing.views.do_disapprove_modify

拒绝一个计算资源的修改申请。完成后重定向到本页面。

POST方法

传入参数

+ **id** 拒绝的计算资源申请id
+ **note** 管理员消息

### 6.computing.views.do_create_package

创建一个新套餐。重定向到本页面。

POST方法

传入参数

- **name** 套餐名字
- **type** 计算资源类型，字符串：'real'（实体机）,'virtual'（虚拟机）
- **cpu** CPU描述
- **memory** 内存大小
- **disktype** 硬盘类型
- **disk** 硬盘大小
- **os** 操作系统

### 7.computing.views.do_delete_package

删除一个新套餐。重定向到本页面

POST方法

传入参数

+ **name** 套餐名字



