物品相关数据模型
－－－
－－－
GType //记录物品类型和属性名
	//数据：
	id
	name:string //记录物品类型名称，要求唯一
	pro_names:string  //记录物品属性名称，具体实现方式请自定
	//接口函数-全局
	create_gtype(name,["name1","name2",...])
	find_gtypes(name) //按照name查找Gtype
	delete_gtype(name)
	//接口函数-类
	set_proname(int, name)//设置属性名称, 下标从0开始, 无返回值
	add_proname(name)//增加属性, 无返回值
	remove_proname(int)//删除属性, 无返回值
	get_proname(int)//获得属性名称, 下标从0开始
	get_pro_index(name)//获得具体属性名称的序号, 下标从0开始, 没找到返回-1
	get_all_pros()//获得所有属性名称list
	get_pronum()//获得属性数目


Goods //记录物品具体属性信息
	//数据
	id
	name:string //物品名称
	gtype:GType //物品配置类型
	pro_values:string  //记录具体属性值，具体实现方式自定
	//接口函数-全局
	create_goods(name, gtype, ["pro1","pro2",...])
    find_goods({gtype_name, name})
	delete_goods(name/id/...)//参数自定，我能用就行
	//接口函数-类
	get_pro(int)//获得属性值,属性下标从0开始
	set_pro(int, value)//设置属性值,属性下标从0开始
	remove_pro(int)//删除属性值,属性下标从0开始

	
Single //记录单个物品
	//数据
	id
	sn:string //sn号，要求唯一
	goods: Goods
	status:enum //表示物品状态，共available(av),unavailable(un),borrowed(bo),destroyed(de),repairing(re)５个状态, 缩写为首两个字母
	account://目前物品被谁借出，可为空
	note //备注信息
	//接口函数-全局
	create_singles(goods, ['sn1','sn2',...], status, user_name)//同时创建多个，account为None,note为‘’，除sn号以外其他属性均相同
	delete_single(id/sn/...)//参数自定，我能用就行。。。。
	update_single({'status':....,  'user_name':...., 'note':....})
	//接口函数-类
	


Borrow //记录所有借用
	//数据
	id
	account //用户
	single　//具体物品
	status  //状态，包括borrow_authing(ba),rejected(rej),accepted(ac),borrowed(bo),return_authing(ra),return_pending(rp),returned(ret),lost(lo),damaged(da)
	user_note:string    //备注信息, 最多1000个bits
	manager_note:string //备注信息, create时置为"", 最多1000个bits
	//接口-全局
	create_borrow(account, sn, status, user_note) //manager_note默认为""
	find_borrow({'single': ..., 'status':...., 'account':.....}, {})
	delete_borrow(id)
	update_borrow(id, {'status':...., 'user_note':...., 'manager_note':......})


Package() //借用词源的套餐(写在computing.models)
	//数据
	name
	cpu
	pc_type
	memory
	disk
	disk_type
	//接口-全局
	create_package({})
	get_package_list() //返回所有对象组成的List
	update_package(id, {}) //更新package对象的信息
	delete_package(id)	//删除对象






