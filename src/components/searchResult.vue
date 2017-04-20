<template>
<div id="searchResult">
  <div id="header">
  <input type="text" v-model="query" id="input" v-on:keyup.enter="submit">
  <button v-on:click="submit" id="submit">search</button>
  </div>
  <div id="result"><p id="result_number">{{ tips }}</p>
  	<div v-for="item in part_response">
	    <a id="title" v-bind:href="item.url" target="_blank" class="item_title">{{ item.title}}</a>
	    <p class="item_description">{{ item.description }}</p>
	    <li id="small_url_content"><a v-bind:href="item.url" id="small_url" target="_blank">{{ item.url }}</a></li>
	    <li id="date">&nbsp{{ item.date }}</li>
    </div>
	</div>
  <div id="footer">
  	<button v-if="show_button" v-for="n in parseInt(length/10)+1" v-on:click="page_select=n">{{n}}</button>
  </div>
</div>

</template>

<script>
export default {
  name: 'searchResult',
  props: ['parentQuery'],
  mounted: function(){
  	var input_query=document.getElementById('input')
  	input_query.focus()
  },
  /*updated: function(){
  	if(this.query!=""){
	  	var split_query = this.query.split("")
	  	var item_description = document.getElementsByClassName('item_description')
	  	var item_title = document.getElementsByClassName('item_title')
	  	var re= new RegExp(this.query,"g")
	  	var index
	  	for(index in item_description){
	  		var description_text = item_description[index].innerHTML
	  		var title_text = item_title[index].innerHTML
	  		title_text = title_text.replace(re,"<span style='color:red'>"+this.query+"</span>")
	  		description_text = description_text.replace(re,"<span style='color:red'>"+this.query+"</span>")
	  		item_description[index].innerHTML=description_text
	  		item_title[index].innerHTML = title_text
	  	}
  	}
  	//console.log(text)
  	//alert('updated')
  },*/
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      query: this.parentQuery,
      //query: '美国',
      page_select: 1,
      tips: '请输入要搜索的内容',
      show_button: false,
      response: []
    }
  },
  computed:{
  	length: function(){
  		var len=0
  		for(let item in this.response){
  			len++
  		}
  		return len
  	},
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
  },
  methods: {
  	submit: function(){
  		this.tips='正在查询。。。'
  		var qs = require('qs');
  		//alert(this.query)
  		this.$axios.post('./back_end.php',
  			qs.stringify({
  			'question': this.query
  		})).then(response=>{
  			this.show_button=true
  			this.response=response.data
  			//console.log(response.data)
  			this.tips='为您找到大约'+this.length+'个结果'
  		})
  		.catch(error=>{
  			this.tips='查询失败，请检查网络连接'
  			console.log(error)
  		})
  	}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hightLight{
	color: red;
}
#searchResult{
	width: 100%;
	height: 100%;
	margin: 0;
	padding: 0;
	
}
#header{
    margin-top: 0;
    padding: 0;
    width: 100%;
    height: 80px;
    background-color: #FFF;
    position: fixed;
    top: 0px;
    left: 0px;
    z-index: 1;
}
#input{
	width: 600px;
    height: 35px;
    //border-color:#39F;
    border-style:solid;
    border-width:1px;
    font-size:24px;
    position: relative;
    left: 15%;
    top: 8px;
}
#submit{
	height:40px;
    width:120px;
    background-color:#39F;
    border:none;
    //border-style:solid;
    font-size:24px;
    color:#FFF;
    margin-top: -1px;
    //margin-left:-10px;
    position: relative;
    top: 8px;
    left: 10%;
}
#result{
    height: auto;
    width: 40%;
    margin-top: 80px;
    position: relative;
    left: 15%;
}
#result_number{
	color: gray;
	font-size: 16px;
}
#result a{
    font-size: 18px;
    color: #0000FF;
}
#result p{
    margin:2px;
}
/*#result li{
    display: inline-block;
    font-size: 12px;
    color: #666666;
}*/
#small_url_content{
	display: inline-block;
}
#date{
	display: inline-block;
    font-size: 12px;
    color: #666666;
}
#result li a{
	display:block;/*内联对象需加*/
    width:15em;
    word-break:keep-all;/* 不换行 */
    white-space:nowrap;/* 不换行 */
    overflow:hidden;/* 内容超出宽度时隐藏超出部分的内容 */
    text-overflow:ellipsis;/* 当对象内文本溢出时显示省略标记(...) ；需与overflow:hidden;一起使用。*/
    font-size: 12px;
    text-decoration: none;
    color: #008B00;
}
#footer{
	position: relative;
	left: 15%;
	
}
#footer button{
	margin-right:20px;
	font-size: 15px;
	background-color: #FFF;
	border:solid 1px #FFF;
	padding: 10px 14px 10px 14px;
	//border:none;
	color: #191970;
}
#footer button:hover{
	border:solid 1px #39F;
	cursor: hand;
}
</style>
