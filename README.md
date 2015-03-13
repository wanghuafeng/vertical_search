<pre>
## movie
垂直领域搜索：app，movie，music，book

垂直搜索爬虫（所有抓取数据英文统一转化为小写入库，已完成自动化工作，分布在mdev由crontab控制）：
	由mdev crontab执行(spider_name)_fab.py,scp 文件到s3指定目录下，
	执行抓取操作（s3_remote_path = '/home/ferrero/wanghuafeng/(spider_name)_spider'）
	1）app （360全站游戏、软件）
		爬虫路径：mdev:/home/mdev/wanghuafeng/app_spider
		1、爬虫抓取360网站数据（app_name，download_count）
		2、基于指定规则对抓取数据进行清洗
		（忽略括号中的内容，含英文、数字组合将空格保留，
		只含有汉字的数据按空格进行切割，切割后数据保留相同的下载量词频）
		3、一次清洗后的数据，交由filter_sentence做二次清洗后生成*.prebuild, 
		*.packet（将download_count作为freq参数，跳过horde词频抓取直接入库）
		4、*.prebuild文件重命名为*.build上传到UDB1的指定路径下
			（'/data/cloud/daily_data'#云词库路径、
			  udb1_vertical_path = '/data/vertical/builds/current'#垂直搜索库路径）
	2）music （百度全站音乐）
		爬虫路径：mdev:/home/mdev/wanghuafeng/music_spider
		1、抓取百度音乐全站音乐数据
		2、基于规则对抓取的音乐数据进行清洗（只保留含有汉字+数字+字母+空格的数据）
		3、由filter_sentence做二次清洗后生成*.prebuild, *.packet，将*.packet交由horde进行词频抓取
	3）video （搜狐、豆瓣、360、爱奇艺）
		爬虫路径：mdev:/home/mdev/wanghuafeng/music_spider
		1、抓取搜狐、豆瓣、360、爱奇艺电影电视剧数据
		2、对视频数据进行清洗（非汉字部分进行切割）
		3、由filter_sentence做二次清洗后生成*.prebuild, *.packet，将*.packet交由horde进行词频抓取
	4）book（京东）
		爬虫路径：mdev:/home/mdev/wanghuafeng/book_spider
		1、抓取京东全站图书数据
		2、对抓取数据进行清洗（只保留汉字部分，滤去以指定元素结尾的数据）
		3、由filter_sentence做二次清洗后生成*.prebuild, *.packet，将*.packet交由horde进行词频抓取
</pre>