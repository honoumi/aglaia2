Permission 说明
===================

使用django自带的Permission Model，content type 均设置为account。总计包含以下权限：
----
	name: 普通借用(已认证用户均可获得)
	code name: normal

	name: 实物借用审核
	code name: goods_auth

	name: 计算资源借用审核
	code name: comput_auth

	name: 用户身份审核
	code name: user_auth

	name: 查看所有用户列表及信息
	code name: view_all

	name: 修改他人的普通信息
	code name: modf_normal

	name: 修改所有人的敏感信息
	code name: modf_key

	name: 修改所有人的权限设定
	code name: modf_perm

	name: 修改所有人所在的用户组
	code name: modf_group

	name: 删除用户
	code name: del_user
