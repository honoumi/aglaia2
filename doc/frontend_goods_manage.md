# GOODS_MANAGE.HTML

实物资源借还请求的管理界面。

## 显示FUNCTION

1.goods.views.show_manage

## RENDER CONTEXT

+ base.html要求的render context
+ **borrow_requests** 借用请求列表
    - **id** 请求id
    - **goods_name** 借用物品的名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
+ **return_requests** 归还请求列表
    - **id** 请求id
    - **goods_name** 借用物品名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
+ **borrow_pending_requests** 已同意借用的请求列表
    - **id** 请求id
    - **goods_name** 借用物品的名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
    - **note** 管理员消息
+ **return_pending_requests** 已同意归还的请求列表
    - **id** 请求id
    - **goods_name** 借用物品名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
    - **note** 管理员消息
+ **repair_requests** 待审核维修申请的物品列表
    - **id** 请求id
    - **goods_name** 借用物品名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
    - **note** 消息
+ **repairing_requests** 正在维修物品列表
    - **id** 请求id
    - **goods_name** 借用物品名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
    - **note** 消息
+ **repaired_requests** 已维修完成物品列表
    - **id** 请求id
    - **goods_name** 借用物品名称
    - **sn** 借用物品SN
    - **borrower_name** 借用者用户名
    - **note** 消息

## FORM ACTIONS

### 1.goods.views.do_accept_borrow

接受某个借用申请。完成后返回原页面。

POST方法

+ **id** 请求id
+ **note** 管理员信息(比如去何处取物资)

### 2.goods.views.do_reject_borrow

拒绝某个借用申请。完成后返回原页面。

POST方法

+ **id** 请求id
+ **note** 管理员信息

### 3.goods.views.do_finish_borrow

完成某个借用申请。完成后返回原页面。

POST方法

+ **id** 请求id

### 4.goods.views.do_accept_return

接受某个归还申请。完成后返回原页面。

POST方法

+ **id** 请求id
+ **note** 管理员信息(比如去何处取物资)

### 6.goods.views.do_finish_return

完成某个归还申请。完成后返回原页面。

POST方法

+ **id** 请求id

### 7.goods.views.do_accept_repair

接受维修申请.

POST方法

+ **id** 请求id
+ **note** 管理员消息

### 7.5. goods.views.do_reject_repair

### 8.goods.views.do_start_repair

开始维修。

POST方法

+ **id** 请求id
+ **note** 管理员消息

### 9.goods.views.do_finish_repair

维修完成。

POST方法

+ **id** 请求id
+ **note** 管理员消息

### 10.goods.views.do_return_repair

维修后物品归还借用者。

POST方法

+ **id** 请求id
+ **note** 管理员消息
