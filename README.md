# anjuke
存储scrapy爬虫

## feixiaohao

使用scrapy + selenium + Phantomjs 抓取feixiaohao中的数据,
并对数据进行处理，存入到mongo中


## anjuke


使用scrapy爬虫框架,通过重新构建强求头,关闭设置cookie和重构首次请求来进行反反爬,
再通过观察分页规律构建URL地址再次发起请求.通过自定义的房源图片下载pipeline进行图片的下载和存储.
通过xpath匹配出有效的房源的标题,价格,地址.户型等有效字段进行数据存储.


