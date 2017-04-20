# 小型搜索引擎(tinySearchEngine)

> 基于scrapy爬虫框架，结巴分词，php和vue.js实现的小型搜索引擎。
>
> a tiny search engine based on vue.js and use scrapy,jieba,php to accomplish it

### Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

### 整体实现

大体流程如下：

１．爬虫爬取网页数据，保存在文件中，

２．python读取文件内容，存到数据库表中，使用结巴分词对网页内容进行分词，并获得TF-IDF值，构建倒排索引保存到数据库中。

３．前端界面接受用户输入，使用POST请求将数据发送到后端。

４．后端接受到数据进行分词，然后在倒排索引数据库查询，结果取并集，然后根据倒排索引数据库结果在结果数据库中查询，返回网页的具体信息。

５．前端收到返回后，将结果呈现出来。

### 具体实现

#### １．爬虫

爬虫采用的是python的爬虫库scrapy，只需要进行简单的配置就可以使用，如果要递归爬取，可以采用`class DmozSpider(CrawlSpider)`。

要获得的数据网页数据主要有：url,title,description,keywords，具体配置如下：

```python
item['title'] = response.selector.xpath('//title/text()').extract()
item['keywords'] = response.selector.xpath('//meta[@name="keywords"]/@content').extract()
item['description'] = response.selector.xpath('//meta[@name="description"]/@content').extract()
```

同时，为了保存数据，需要定义items，在items.py中添加如下：

```python
url = scrapy.Field()
title = scrapy.Field()
keywords = scrapy.Field()
description = scrapy.Field()
```

在终端中运行`scrapy crawl dmoz -o items.json -t json`，可以把数据存到items.json中。

#### ２．分词

分词我选用的是python环境下的[结巴分词](https://github.com/fxsjy/jieba),　在考虑了好几种分词后，最后选择了结巴分词，主要是安装简单(可以直接通过pip安装)，使用方便，并且在社区的贡献下，衍生出了不同语言版本(在后端中，我采用的是结巴分词的php版本)。

结巴分词直接提供了基于TF-IDF算法的关键词提取功能：

> jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
>
> sentence 为待提取的文本
>
> topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
>
> withWeight 为是否一并返回关键词权重值，默认值为 Falseallow
>
> POS 仅包括指定词性的词，默认值为空，即不筛选

所以在分词过程中，可以直接通过结巴分词获得关键词，以及关键词对应的TF-IDF值。

#### ３．数据库

数据库选择的是MySQL,新建数据库名`python`，数据库下有两个表，`search_result`,`inverted index`。

```
├── python                         //数据库　　　　　　　　　
│   ├── search_result　　　　　　　　//搜索结果
│   └── inverted indexsuoyin      //倒排索引
```

经过爬虫爬取的数据保存在items.json中，在jsonToMySQL.py中，将文件中保存的数据存到数据库表search_result中，有index作为网页的唯一标志，字段有`index_`,`url`,`title`,`date`,`description`。

在urlToKeywords.py中，从表search_result中读取每一条，利用结巴分词提取关键字，并获得每个关键词的TF-IDF值，保存到表`inverted index`中，在查询的过程中，输入一条语句，将这条语句分词后得到关键词，将每个关键词进inverted index中查询，得到index和TF-IDF,结果取并集，根据index到search_result查询url,title等信息，利用TF-IDF之和进行页面的排序。

#### ４．前端

前端采用前端框架`vue.js`，`使用vue-router`实现路由管理，使用`axios`发送http请求。组件有两个，模仿的是百度的首页，在有输入的时候输入框位置变化(百度打开时输入框居中，有输入的时候变换到输入框在顶部)，百度应该是用切换css类的方式来实现的，我采用的是切换组件，首页输入框有输入改变触发`<input type='text>'`的`input`事件，触发后，实现页面跳转到结果页面，为了保持输入的数据不变，把输入框的值进行了组件间的通信，首页组件将输入值传给父组件，父组件将值传给结果子组件，并且创建钩子，在页面挂载mounted后，让输入框获得焦点

```javascript
//子组件向父组件通信，传递输入框的值
methods: {
  	change: function(){
  		this.$emit('childChange',this.query)
  	},
}
```

```javascript
//父组件监听到子组件的事件后，实现页面跳转。
showResult: function(data){
      //alert('hello')
      this.query=data
      console.log(this.query)
      this.$router.replace({path:'/result'})
  }  
```

```javascript
//子组件接受来自于父组件的值
props: ['parentQuery'],
```

mounted后，结果页面输入框获得焦点

```javascript
 mounted: function(){
  	var input_query=document.getElementById('input')
  	input_query.focus()
  },
```

前端接受的来自于后端的json数据，利用vue的列表渲染，页面选择按钮数量根据返回结果的数目确定`parseInt(num/10)+1`就是按钮的个数，同时采用条件渲染控制出现结果选择的时间。

```html
<button v-if="show_button" v-for="n in parseInt(length/10)+1" v-on:click="page_select=n">{{n}}</button>
```

结果显示

```html
	<div v-for="item in part_response">
	    <a id="title" v-bind:href="item.url" target="_blank" class="item_title">{{ item.title}}</a>
	    <p class="item_description">{{ item.description }}</p>
	    <li id="small_url_content"><a v-bind:href="item.url" id="small_url" target="_blank">{{ item.url }}</a></li>
	    <li id="date">&nbsp{{ item.date }}</li>
    </div>
```

利用计算属性，只显示十个结果，并根据当前页的不同显示不同的结果。

```javascript
part_response: function(){
  		var part=[]
  		for(let start = (this.page_select-1)*10;start<this.page_select*10;start++){
  			if(start<this.length){
  				part.push(this.response[start])
  			}
  		}
  		//shixian guanjianzi gaoliang;
  		var split_query = this.query.split("")
  		console.log(split_query)
  		var char
  		var part_to_str =  JSON.stringify(part)
  		return part
  	}
```



#### ５．后端

在后端同样需要分词，后端接受到前端发送的数据，对搜索进行分词，我采用的是结巴分词的PHP版，需要在使用的时候引入需要的PHP文件即可，但是在使用的时候要初始化，即调用`Jieba::init()`，但是该过程非常耗时间，搜索的绝大多数时间都消耗在此，为了测试消耗时间，我注释掉所有代码，只保留该初始化函数，发现耗时基本跟执行完整查询一致，目前还没有很好的解决方法，自己实现分词功能不是很现实。

分词后得到几个关键词，从倒排索引数据库搜索对应结果，按照TF-IDF排序，将index从搜索结果数据库查询，返回title,url等字段，保存在二维数组中，最后使用json返回结果。

```php
echo json_encode($return_array);
```

### 运行截图

![](https://github.com/xujingguo58/tinySearchEngine/blob/master/image/img1.png)

![](https://github.com/xujingguo58/tinySearchEngine/blob/master/image/img2.png)

![](https://github.com/xujingguo58/tinySearchEngine/blob/master/image/img3.png)

![](https://github.com/xujingguo58/tinySearchEngine/blob/master/image/img4.png)



### 文件结构

```
.
├── back_end.php     //后端文件，负责把接受前端的ＰＯＳＴ请求，查询后返回以json返回结果
├── build
├── config
├── dist　　　　　　　　　
│   ├── index.html　　　　//首页
│   └── static
│       ├── css
│       └── js
├── DomzSpider.py      //爬虫文件，负责爬取网页的title,url,description保存在一个josn文件中
├── index.html
├── node_modulels      //node模块
├── package.json
├── README.md
├── src
│   ├── App.vue
│   ├── assets
│   │   └── logo.png
│   ├── components
│   │   ├── searchEngine.vue       //搜索的首页
│   │   └── searchResult.vue       //搜索结果显示
│   ├── main.js
│   └── router                    //路由
│       └── index.js
├── static
├── test
├── jsonToMySQL.py                //从json读取数据保存到MySQL数据库search_result表中
└── urlToKeywords.py              //从数据库search_result表读取数据，利用结巴分词将获得TF-IDF,保存到									  //inverted index表中

```

### 参考

[dySE：一个 Java 搜索引擎的实现，第 1 部分: 网络爬虫](https://www.ibm.com/developerworks/cn/java/j-lo-dyse1/index.html)

[Python抓取框架Scrapy快速入门教程](http://www.tuicool.com/articles/AzeABf)

[自制简单搜索引擎](https://sanwen8.cn/p/160kKfo.html)

[结巴中文分词](https://github.com/fxsjy/jieba)

["結巴"中文分詞：做最好的 PHP 中文分詞、中文斷詞組件。](https://github.com/fukuball/jieba-php)





For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).