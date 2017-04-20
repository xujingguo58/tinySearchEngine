<?php
ini_set("display_errors", "Off");
//error_reporting(E_ALL | E_STRICT);
error_reporting(1);
ini_set('memory_limit', '1024M');
set_time_limit(0);
//ignore_user_abort(); // 后台运行  

require_once dirname(__FILE__)."/vendor/multi-array/MultiArray.php";
require_once dirname(__FILE__)."/vendor/multi-array/Factory/MultiArrayFactory.php";
require_once dirname(__FILE__)."/class/Jieba.php";
require_once dirname(__FILE__)."/class/Finalseg.php";
use Fukuball\Jieba\Jieba;
use Fukuball\Jieba\Finalseg;
use Fukuball\Jieba\JiebaAnalyse;
//echo "hello";


function find($str){
	//$link = mysqli_connect("localhost", "root", "666666", "python");
	global $link;
	mysqli_set_charset($link, "utf8");
	/* check connection */
	if (mysqli_connect_errno()) {
		//printf("Connect failed: %s\n", mysqli_connect_error());
		echo json_encode("");
		exit();
	}
	$sql = "select * from `inverted index` where keywords='".$str."'";
	//echo $sql." \n";

	$result=$link->query($sql);

	if(!$result){
		echo json_encode("");
		//echo "sql语句错误<br/>";
		//echo "error:".$mysqli->error."|".$mysqli->error;
	}
	$num_results = $result -> num_rows; //结果行数
	//echo "<p>Number of row found: ". $num_results ."</p>";//输出行数
	global $result_array;
	for($i = 0;$i < $num_results;$i++)//循环输出每组元素
	{
		$row = $result -> fetch_assoc();//提取元素，一次一行，fetch_assoc()提取出的元素，有属性以及值
		$index_ = stripcslashes(($row['index_']));
		$tf_idf = stripcslashes($row['tf_idf']);
		//echo $index_." ".$tf_idf."   ";
		if(array_key_exists($index_,$result_array)){
			$result_array[$index_]+=$tf_idf;
		}
		else{
			$result_array[$index_] = 0+$tf_idf;
		}
	}

	//mysqli_close($link);
}
function search($index){
	global $return_array;
	//$link = mysqli_connect("localhost", "root", "666666", "python");
	global $link;
	mysqli_set_charset($link, "utf8");
	/* check connection */
	if (mysqli_connect_errno()) {
		echo json_encode("");
		exit();
	}

	$sql = "select * from `search_result` where index_='".$index."'";

	$result=$link->query($sql);

	$num_results = $result -> num_rows; //结果行数
	$row = $result -> fetch_assoc();//提取元素，一次一行，fetch_assoc()提取出的元素，有属性以及值
	$url = stripcslashes(($row['url']));
	$title = stripcslashes($row['title']);
	$description = stripcslashes($row['description']);
	$date = stripcslashes($row['date']);
	$return_array[]=array("url"=>$url,"title"=>$title,"description"=>$description,"date"=>$date);
	//mysqli_close($link);
}
session_start();

//	$_POST['question']='大约';
if($_POST['question']!=""){
	//$_SESSION["Jie"]=serialize(Jieba::return_self());
	//unserialize($_SESSION["Jie"])::init();
	Jieba::init();
	Finalseg::init();
	//open database 
	$link = mysqli_connect("localhost", "root", "666666", "python");


	$result_array=[];
	$return_array=[];
	$seg_list=Jieba::cutForSearch($_POST['question']);
	//$seg_list = unserialize($_SESSION["Jie"])::cutForSearch($_POST['question']);
	//var_dump($seg_list);
	if(count($seg_list)==0){
		echo json_encode("");
		exit();
	}
	foreach ($seg_list as $value){
		//print($value." ");
		find($value);
	}
	if(count($result_array)==0){
		echo json_encode("");
		exit();
	}
	arsort($result_array);
	foreach ($result_array as $key=>$value){
		search($key);
	}
	if(count($return_array)==0){
		echo json_encode("");
		exit();
	}
	echo json_encode($return_array);

	//close database
	mysqli_close($link);

}
?>
