<?php
$method = $_REQUEST["method"];
$data = $_REQUEST["data"];

$user = new UserDAO ();

if ($method == "a") {
    $arr = $user->queryList();
    echo "<center><h3>list</h3><table border=1><tr><th>id</th><th>txt</th><th>time</th></tr>";
    foreach ($arr as $value) {
        echo "<tr><td>" . $value ['id'] . "</td><td>" . $value ['txt'] . "</td><td>" . $value ['time'] . "</td></tr>";
    }
} elseif ($method == "b") {
    //设置时区的方法
    date_default_timezone_set('PRC');
    //这样便能获取准确的时间了
    $times = date('y-m-d h:i:s', time());
    $userAdd = array(1, $data, $times);
    $user->addList($userAdd);
} elseif ($method == "d") {
    $arr = $user->queryUserById();
    echo $arr[0]['can1'];
} elseif ($method == "e") {
    $arr = $user->queryUserById();
    echo $arr[0]['can2'];
} elseif ($method == "f") {
    $arr = $user->queryUserById();
    echo $arr[0]['can3'];
} elseif ($method == "c") {
    $arr = $user->queryUserById();
    echo $arr[0]['can'];
}

class UserDAO
{

    var $pdo;

    function __construct()
    {
        $this->pdo = new PDO("mysql:host=localhost;dbname=blackgo", "blackgo", "LpGSsPzs3HxBZAzP");
    }


    function GetPDO()
    {
        if ($this->pdo == null)
            $this->pdo = new PDO ("mysql:host=localhost;dbname=blackgo", "blackgo", "LpGSsPzs3HxBZAzP");
        return $this->pdo;
    }

    function addList($arr)
    {
        try {
            $this->pdo->exec("insert into list(id,txt,time) values(" . $arr[0] . ",'" . $arr[1] . "','" . $arr[2] . "')");
        } catch (Exception $e) {
            echo "error:" . $e->getMessage();
        }
    }

    //修改用户
    function modifUser($arr)
    {

        $this->pdo->exec("update userinfo set username='" . $arr[0] . "',pwd='" . $arr[1] . "',age=" . $arr[2] . " where id=" . $arr[3]);
    }

    //删除用户
    function deleteUser($id)
    {
        $this->pdo->exec("delete from  userinfo where id=" . $id);
    }

    public function queryList()
    {
        $rs = $this->pdo->query("select * from list");
        $rs->setFetchMode(PDO::FETCH_ASSOC);
        $result_arr = $rs->fetchAll();
        return $result_arr;
    }

    //根据用户ID 查询该ID用户
    function queryUserById()
    {
        $rs = $this->pdo->query("select * from user where id = 1");
        $rs->setFetchMode(PDO::FETCH_ASSOC);
        $result_arr = $rs->fetchAll();
        return $result_arr;
    }
}



/**
 * 用户删除
 *
 * $user->deleteUser(3);
 * echo "删除成功！";
 * */
