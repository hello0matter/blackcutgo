"ui";
"nodejs";
// $settings.setEnabled('enableAccessibilityServiceByRoot', true);
// $settings.setEnabled('not_show_console', true);
// $settings.setEnabled('stop_all_on_volume_up', false);
// $settings.setEnabled('foreground_service', true)
// $settings.setEnabled('stable_mode', true);
// var sh = new Shell(true);

// // 检查设备是否已root
// function isRootAvailable() {
//   let result = sh.exec("echo root");
//   return result.code === 0;
// }

// // 申请root权限
// function requestRoot() {
//   let result = sh.exec("su");
//   if (result.code === 0) {
//     toast("Root权限已获取");
//     return true;
//   } else {
//     toast("无法获取Root权限");
//     return false;
//   }
// }

// // 示例：执行需要root权限的命令
// function executeRootCommand(command) {
//   if (!isRootAvailable()) {
//     toast("设备没有root或无法获取root权限");
//     return;
//   }
//   let result = sh.exec(command);
//   if (result.code === 0) {
//     toast("命令执行成功: " + command);
//   } else {
//     toast("命令执行失败: " + result.error);
//   }
// // }
// // 获取root权限root
// function grantOverlayPermission(packageName) {
//   // 授予悬浮窗权限的shell命令
//   let command = "pm grant " + packageName + " android.permission.SYSTEM_ALERT_WINDOW";

//   // 执行shell命令
//   sh.exec(command);

// }


// // 检查并申请root权限
// if (requestRoot()) {
// 授予悬浮窗权限

// } else {
//   requestRoot()
// }

// sh.exit();
function QCYSDK(appKey, appSecret) {
    http.__okhttp__.setMaxRetries(0);
    http.__okhttp__.setTimeout(10 * 1000);
    this.event = events.emitter();

    this.debug = true;
    this._lib_version = "v1.1.8";
    this._protocol = "http";
    this._hosts = ["api1.7ccccccc.com", "api2.7ccccccc.com", "api3.7ccccccc.com"]
    this._host = this._hosts[0]
    this._device_id = this.getDeviceID();
    this._switch_count = 0;

    this._retry_count = 9;
    this._appKey = appKey;
    this._appSecret = appSecret;
    this._card = null;

    this._username = null;
    this._password = null;
    this._token = null;

    this.is_trial = false;
    this.login_result = {
        "card_type": "",
        "expires": "",
        "expires_ts": 0,
        "config": "",
    };

    this._auto_heartbeat = true;  // 是否自动开启心跳任务
    this._heartbeat_gap = 300 * 1000; // 默认300秒
    this._heartbeat_task = null;
    this._heartbeat_ret = { "code": -9, "message": "还未开始验证" };
    this._prev_nonce = null;
}
QCYSDK.prototype.switchHost = function () { // 切换备用服务器
    this._switch_count++;
    this._host = this._hosts[this._switch_count % this._hosts.length];
}
QCYSDK.prototype.SetCard = function (card) {
    this._card = card.trim();
}
QCYSDK.prototype.SetUser = function (username, password) {
    this._username = username.trim();
    this._password = password;
}
QCYSDK.prototype.MD5 = function (str) {
    try {
        let digest = java.security.MessageDigest.getInstance("md5");
        let result = digest.digest(new java.lang.String(str).getBytes("UTF-8"));
        let buffer = new java.lang.StringBuffer();
        for (let index = 0; index < result.length; index++) {
            let b = result[index];
            let number = b & 0xff;
            let str = java.lang.Integer.toHexString(number);
            if (str.length == 1) {
                buffer.append("0");
            }
            buffer.append(str);
        }
        return buffer.toString();
    } catch (error) {
        alert(error);
        return "";
    }
}
/* 通用 */
QCYSDK.prototype.GetHeartbeatResult = function () {
    return this._heartbeat_ret;
}
QCYSDK.prototype.GetTimeRemaining = function () {
    let g = this.login_result.expires_ts - this.getTimestamp();
    if (g < 0) {
        return 0;
    }
    return g;
}
QCYSDK.prototype.getDeviceID = function () {
    let id = device.serial;
    if (id == null || id == "" || id == "unknown") {
        id = device.getAndroidId();
    }
    if (id == null || id == "" || id == "unknown") {
        id = device.getIMEI();
    }
    return id;
}
/* 卡密相关 *//*卡密登录功能*/
QCYSDK.prototype.CardLogin = function () {  // 卡密登录
    if (!this._card) {
        return { "code": -4, "message": "请先设置卡密" };
    }
    let method = "POST";
    let path = "/v1/card/login";
    let data = { "card": this._card, "device_id": this._device_id };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this._token = ret.result.token;
        this.login_result = ret.result;
        if (this._auto_heartbeat) {
            //调用心跳
            this._startCardHeartheat();
        }
    }
    return ret;
}
/*卡密心跳*/
QCYSDK.prototype.CardHeartbeat = function () {  // 卡密心跳，默认会自动调用
    if (!this._token) {
        return { "code": -2, "message": "请在卡密登录成功后调用" };
    }
    let method = "POST";
    let path = "/v1/card/heartbeat";
    let data = { "card": this._card, "token": this._token };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this.login_result.expires = ret.result.expires;
        this.login_result.expires_ts = ret.result.expires_ts;
    }
    return ret;
}
QCYSDK.prototype._startCardHeartheat = function () {  // 开启卡密心跳任务
    if (this._heartbeat_task) {
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    this._heartbeat_task = threads.start(function () {
        setInterval(function () { }, 10000);
    });
    this._heartbeat_ret = this.CardHeartbeat();
    this._heartbeat_task.setInterval((self) => {
        self._heartbeat_ret = self.CardHeartbeat();
        if (self._heartbeat_ret.code != 0) {
            self.event.emit("heartbeat_failed", self._heartbeat_ret);
        }
    }, this._heartbeat_gap, this);
    this._heartbeat_task.setInterval((self) => {
        if (self.GetTimeRemaining() == 0) {
            self.event.emit("heartbeat_failed", { "code": 10210, "message": "卡密已过期！" });
        }
    }, 1000, this);
}
QCYSDK.prototype.CardRecharge = function (card, useCard) { // 以卡充卡
    let method = "POST";
    let path = "/v1/card/recharge";
    let data = { "card": card, "useCard": useCard };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CardLogout = function (token) {  // 卡密退出登录
    threads.shutDownAll()
    this._heartbeat_ret = { "code": -9, "message": "还未开始验证" };
    if (this._heartbeat_task) { // 结束心跳任务
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    if (!token) {
        return { "code": 0, "message": "OK" };
    }
    let method = "POST";
    let path = "/v1/card/logout";
    let data = { "card": this._card, "token": token };
    let ret = this.Request(method, path, data);
    // 清理
    this._token = null;
    this.login_result = {
        "card_type": "",
        "expires": "",
        "expires_ts": 0,
        "config": "",
    };
    return ret;
}
QCYSDK.prototype.CardUnbinstarthreadsevice = function () { // 卡密解绑设备，需开发者后台配置
    let method = "POST";
    let path = "/v1/card/unbind_device";
    let data = { "card": this._card, "device_id": this._device_id };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CardUnbinstarthreadseviceBybinstarthreadsevice = function () { // 卡密绑定设备上解绑
    let method = "POST";
    let path = "/v1/card/unbind_device/bind_device";
    let data = { "card": this._card, "device_id": this._device_id };
    return this.Request(method, path, data);
}
QCYSDK.prototype.SetCardUnbindPassword = function (password) { // 自定义设置解绑密码
    if (!this._token) {
        return { "code": -2, "message": "请在卡密登录成功后调用" };
    }
    let method = "POST";
    let path = "/v1/card/unbind_password";
    let data = { "card": this._card, "password": password, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CardUnbinstarthreadseviceByPassword = function (password) { // 用户通过解绑密码解绑设备
    let method = "POST";
    let path = "/v1/card/unbind_device/by_password";
    let data = { "card": this._card, "password": password };
    return this.Request(method, path, data);
}
/* 用户相关 */
QCYSDK.prototype.UserRegister = function (username, password, card) {  // 用户注册（通过卡密）
    let method = "POST";
    let path = "/v1/user/register";
    let data = { "username": username, "password": password, "card": card, "device_id": this._device_id };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UserLogin = function () {  // 用户账号登录
    if (!this._username || !this._password) {
        return { "code": -4, "message": "请先设置用户账号密码" };
    }
    let method = "POST";
    let path = "/v1/user/login";
    let data = { "username": this._username, "password": this._password, "device_id": this._device_id };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this._token = ret.result.token;
        this.login_result = ret.result;
        if (this._auto_heartbeat) {
            this._startUserHeartheat();
        }
    }
    return ret;
}
QCYSDK.prototype.UserHeartbeat = function () {  // 用户心跳，默认会自动开启
    if (!this._token) {
        return { "code": -2, "message": "请在用户登录成功后调用" };
    }
    let method = "POST";
    let path = "/v1/user/heartbeat";
    let data = { "username": this._username, "token": this._token };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this.login_result.expires = ret.result.expires;
        this.login_result.expires_ts = ret.result.expires_ts;
    }
    return ret;
}
QCYSDK.prototype._startUserHeartheat = function () {  // 开启用户心跳任务
    if (this._heartbeat_task) {
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    this._heartbeat_task = threads.start(function () {
        setInterval(function () { }, 10000);
    });
    this._heartbeat_ret = this.UserHeartbeat();

    this._heartbeat_task.setInterval((self) => {
        self._heartbeat_ret = self.UserHeartbeat();
        if (self._heartbeat_ret.code != 0) {
            self.event.emit("heartbeat_failed", self._heartbeat_ret);
        }
    }, this._heartbeat_gap, this);

    this._heartbeat_task.setInterval((self) => {
        if (self.GetTimeRemaining() == 0) {
            self.event.emit("heartbeat_failed", { "code": 10250, "message": "用户已到期！" });
        }
    }, 1000, this);
}
QCYSDK.prototype.UserLogout = function (token) {  // 用户退出登录
    threads.shutDownAll()
    this._heartbeat_ret = { "code": -9, "message": "还未开始验证" };
    if (this._heartbeat_task) { // 结束心跳任务
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    if (!token) {
        return { "code": 0, "message": "OK" };
    }
    let method = "POST";
    let path = "/v1/user/logout";
    let data = { "username": this._username, "token": token };
    let ret = this.Request(method, path, data);
    // 清理
    this._token = null;
    this.login_result = {
        "card_type": "",
        "expires": "",
        "expires_ts": 0,
        "config": "",
    };
    return ret;
}
QCYSDK.prototype.UserChangePassword = function (username, password, newPassword) {  // 用户修改密码
    let method = "POST";
    let path = "/v1/user/password";
    let data = { "username": username, "password": password, "newPassword": newPassword };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UserRecharge = function (username, card) { // 用户通过卡密充值
    let method = "POST";
    let path = "/v1/user/recharge";
    let data = { "username": username, "card": card };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UserUnbinstarthreadsevice = function () { // 用户解绑设备，需开发者后台配置
    let method = "POST";
    let path = "/v1/user/unbind_device";
    let data = { "username": this._username };
    return this.Request(method, path, data);
}
/* 配置相关 */
QCYSDK.prototype.GetCardConfig = function () { // 获取卡密配置
    let method = "POST";
    let path = "/v1/card/config";
    let data = { "card": this._card };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UpdateCardConfig = function (config) { // 更新卡密配置
    let method = "POST";
    let path = "/v1/card/config";
    let data = { "card": this._card, "config": config };
    return this.Request(method, path, data);
}
QCYSDK.prototype.GetUserConfig = function () { // 获取用户配置
    let method = "POST";
    let path = "/v1/user/config";
    let data = { "username": this._username };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UpdateUserConfig = function (config) { // 更新用户配置
    let method = "POST";
    let path = "/v1/user/config";
    let data = { "username": this._username, "config": config };
    return this.Request(method, path, data);
}
/* 软件相关 */
QCYSDK.prototype.GetSoftwareConfig = function () { // 获取软件配置
    let method = "POST";
    let path = "/v1/software/config";
    return this.Request(method, path, {});
}
QCYSDK.prototype.GetSoftwareNotice = function () { // 获取软件通知
    let method = "POST";
    let path = "/v1/software/notice";
    return this.Request(method, path, {});
}
QCYSDK.prototype.GetSoftwareVersion = function () { // 获取软件版本
    let method = "POST";
    let path = "/v1/software/lastarthreads_ver";
    return this.Request(method, path, {});
}
/* 试用功能 */
QCYSDK.prototype.TrialLogin = function () {  // 试用登录
    let method = "POST";
    let path = "/v1/trial/login";
    let data = { "device_id": this._device_id };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this.is_trial = true;
        this.login_result = ret.result;
        this._token = ret.result.token;
        if (this._auto_heartbeat) {
            this._starthreadsrialHeartheat();
        }
    }
    return ret;
}
QCYSDK.prototype.TrialHeartbeat = function () {  // 试用心跳，默认会自动调用
    let method = "POST";
    let path = "/v1/trial/heartbeat";
    let data = { "device_id": this._device_id, "token": this._token };
    let ret = this.Request(method, path, data);
    if (ret.code == 0) {
        this.login_result.expires = ret.result.expires;
        this.login_result.expires_ts = ret.result.expires_ts;
    }
    return ret;
}
QCYSDK.prototype._starthreadsrialHeartheat = function () {  // 开启试用心跳任务
    if (this._heartbeat_task) {
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    this._heartbeat_task = threads.start(function () {
        setInterval(function () { }, 10000);
    });
    this._heartbeat_ret = this.TrialHeartbeat();
    this._heartbeat_task.setInterval((self) => {
        self._heartbeat_ret = self.TrialHeartbeat();
        if (self._heartbeat_ret.code != 0) {
            self.event.emit("heartbeat_failed", self._heartbeat_ret);
        }
    }, this._heartbeat_gap, this);
    this._heartbeat_task.setInterval((self) => {
        if (self.GetTimeRemaining() == 0) {
            self.event.emit("heartbeat_failed", { "code": 10407, "message": "试用已到期！" });
        }
    }, 1000, this);
}
QCYSDK.prototype.TrialLogout = function () {  // 试用退出登录，没有http请求，只是清理本地记录
    threads.shutDownAll()
    this.is_trial = false;
    this._heartbeat_ret = { "code": -9, "message": "还未开始验证" };
    if (this._heartbeat_task) { // 结束心跳任务
        this._heartbeat_task.interrupt();
        this._heartbeat_task = null;
    }
    // 清理
    this._token = null;
    this.login_result = {
        "card_type": "",
        "expires": "",
        "expires_ts": 0,
        "config": "",
    };
    return { "code": 0, "message": "OK" };
}
/* 高级功能 */
QCYSDK.prototype.GetRemoteVar = function (key) { // 获取远程变量
    let method = "POST";
    let path = "/v1/af/remote_var";
    let data = { "varName": key, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.GetRemoteData = function (key) { // 获取远程数据
    let method = "POST";
    let path = "/v1/af/remote_data";
    let data = { "key": key, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CreateRemoteData = function (key, value) { // 创建远程数据
    let method = "POST";
    let path = "/v1/af/remote_data";
    let data = { "action": "create", "key": key, "value": value, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.UpdateRemoteData = function (key, value) { // 修改远程数据
    let method = "POST";
    let path = "/v1/af/remote_data";
    let data = { "action": "update", "key": key, "value": value, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.DeleteRemoteData = function (key) { // 删除远程数据
    let method = "POST";
    let path = "/v1/af/remote_data";
    let data = { "action": "delete", "key": key, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CallRemoteFn = function (fnName, params) { // 云函数
    let method = "POST";
    let path = "/v1/af/call_remote_func";
    let data = { "fnName": fnName, "params": params, "token": this._token };
    return this.Request(method, path, data);
}
QCYSDK.prototype.Request = function (method, path, params) {
    // 构建公共参数
    params["appKey"] = this._appKey;
    method = method.toUpperCase();
    let max_retries = this._retry_count;
    let retries_count = 0;

    let data = { "code": -1, "message": "连接服务器失败" };
    do {
        retries_count++;
        let url = this._protocol + "://" + this._host + path
        let sec = this.retry_fib(retries_count);
        delete params["sign"]
        params["nonce"] = this.genNonce();
        params["timestamp"] = this.getTimestamp();
        let ps = this.joinParams(params);
        let s = method + this._host + path + ps + this._appSecret;
        let sign = this.MD5(s);
        params["sign"] = sign;
        let resp, body;
        try {
            if (method === "GET") {
                resp = http.get(url + "?" + ps + "&sign=" + sign);
            } else {  // POST
                resp = http.post(url, params);
            }
            console.log("resp:", resp);
            body = resp.body.string();
            console.log("body:", body);
            data = JSON.parse(body);
            this._debug(method + '-' + path + ':', params, data);
            let crs = this.CheckRespSign(data);
            if (crs.code !== 0) {
                return crs;
            } else {
                return data;
            }
        } catch (error) {
            log("[*] request error: ", error, sec + "s后重试");
            this._debug(method + '-' + path + ':', params, body)
            this.switchHost();
            sleep(sec * 1000);
        }

    } while (retries_count < max_retries);
    return data;
}
/*工具类*/
QCYSDK.prototype.retry_fib = function (num) {
    if (num > 9) {
        return 34
    }
    let a = 0;
    let b = 1;
    for (i = 0; i < num; i++) {
        let tmp = a + b;
        a = b
        b = tmp
    }
    return a
}
QCYSDK.prototype.genNonce = function () {
    const ascii_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let tmp = '';
    for (let i = 0; i < 20; i++) {
        tmp += ascii_str.charAt(Math.round(Math.random() * ascii_str.length));
    }
    return this.MD5(this._device_id + this._prev_nonce + new Date().getTime() + tmp);
}
QCYSDK.prototype.getTimestamp = function () {
    try {
        let res = http.get("http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp");
        let data = res.data.json()
        return Math.floor(data["data"]["t"] / 1000);
    } catch (error) {
        return Math.floor(new Date().getTime() / 1000);
    }
}
QCYSDK.prototype.joinParams = function (params) {
    let ps = [];
    for (let k in params) {
        ps.push(k + "=" + params[k])
    }
    ps.sort()
    return ps.join("&")
}
QCYSDK.prototype.CheckRespSign = function (resp) {
    if (resp.code != 0 && resp.nonce === "" && resp.sign === "") {
        return resp
    }
    let ps = "";
    if (resp["result"]) {
        ps = this.joinParams(resp["result"]);
    }
    let s = resp["code"] + resp["message"] + ps + resp["nonce"] + this._appSecret;
    let sign = this.MD5(s);
    if (sign === resp["sign"]) {
        return { "code": 0, "message": "OK" };
    }
    return { "code": -99, "message": "CRS:签名校验失败" };
}
QCYSDK.prototype._debug = function (path, params, result) {
    if (this.debug) {
        console.log("\n" + path, "\nparams:", params, "\nresult:", result)
    }
}
// 有问题请加群 675107742
//=======================================界面============================================
ui.layout(
    <ScrollView>
        <vertical>
            <toolbar bg="#009688" gravity="center" marginBottom="3">
                <text w="*" text="car" gravity="center" textColor="#ffffff" textSize="25sp" />
            </toolbar>

            <horizontal marginTop="10sp">
                <text text="卡密:" textColor="black" textSize="15sp" marginLeft="10sp" />
                <input id="card" hint="" textSize="15sp" marginLeft="5sp" w="*" />
            </horizontal>

            <horizontal marginTop="10sp">
                <text text="充值使用的卡密:" textColor="black" textSize="15sp" marginLeft="10sp" />
                <input id="use_card" hint="" textSize="15sp" marginLeft="5sp" w="*" />
            </horizontal>

            <button id="unbind_card" text="解绑" marginLeft="10" marginRight="10" marginBottom="20" />

            <button id="recharge" text="充值卡密" marginLeft="10" marginRight="10" marginBottom="20" />
            <button id="phonetext" text="电话文本地址" marginLeft="10" marginRight="10" marginBottom="20" />
            <button id="checks" text="如果老是自动关闭请点此检查权限" marginLeft="10" marginRight="10" />
            <button id="start" text="启动脚本" marginLeft="10" marginRight="10" />
        </vertical>
    </ScrollView>
);

let AppKey = "v8JfLlyN1UEufqawl3";//7c云开发后台软件管理里面获取
let AppSecret = "GFn8xiUVtOR90P8T3JUhZyjomhf7TMY9";//7c云开发后台软件管理里面获取
let qcysdk = new QCYSDK(AppKey, AppSecret);
qcysdk._protocol = "http"
qcysdk.debug = false; //关闭debug不会打印输出
// 开启断线重连
let isLoginAgain = true //false 关闭断线重连
qcysdk.SetCard(ui.card.text());

function getDatetime() {
    //获取当前的年月日
    let date_ = new Date();
    return (date_.getFullYear() + "." + date_.getMonth() + "." + date_.getDate() + "." + date_.getHours() + ":" + date_.getMinutes() + ":" + date_.getSeconds())
}
function getDatetimeDay() {
    //获取当前的年月日
    let date_ = new Date();
    return (date_.getMonth() + "月" + date_.getDate() + "日")
}

var runthreads = null;
var logPath = "/sdcard/whatsapp/log/"//保存log的路径
let tokenPath = "/sdcard/whatsapp/token/"//保存token的路径
let cdkPath = "/sdcard/whatsapp/cdk.txt"//保存cdk的路径
let imgPath = "/sdcard/whatsapp/img/"//保存错误图片的路径
let token = ""
//充值卡密点击事件
ui.recharge.click(() => {
    if (!ui.card.text() || !ui.use_card.text()) return mylog("请输入卡密，和充值使用的卡密")
    let ret = qcysdk.CardRecharge(ui.card.text(), ui.use_card.text())
    if (ret.code === 0) {
        mylog("卡密充值成功")
    } else {
        mylog(ret.message)
    }
})
//解绑卡密点击事件
ui.unbind_card.click(() => {
    if (!ui.card.text()) return mylog("请输入需要解绑的卡密")
    qcysdk.SetCard(ui.card.text());
    let ret = qcysdk.CardUnbinstarthreadsevice()
    if (ret.code === 0) {
        mylog("解绑成功")
    } else {
        mylog(ret.message)
    }
})


// 监听心跳失败事件
qcysdk.event.on("heartbeat_failed", function (hret) {
    log("心跳失败，尝试重登...")
    sleep(2000);
    if (isLoginAgain) {
        let login_ret = qcysdk.CardLogin();
        if (login_ret.code == 0) {
            files.write(tokenPath, login_ret.result.token);
            log("重登成功");
        } else {
            threads.shutDownAll()
            mylog(login_ret.message);  // 重登失败
            sleep(200);
            exit();  // 退出脚本
        }
    }
});

// 当脚本正常或者异常退出时会触发exit事件
events.on("exit", function () {
    threads.shutDownAll()
    qcysdk.CardLogout(token); // 调用退出登录
    log("结束运行");
});

//启动脚本点击事件
// setInterval(() => {
//     // 获取当前前台应用的包名
//     let currentApp = currentPackage();

//     // 检查当前前台应用是否是目标应用
//     if (currentApp === "com.a.a") {
//         starthreads()
//         toast("目标应用已打开");
//         // 在这里可以执行你想要的操作
//     }
// }, 1000);  // 1秒的时间间隔
if (files.isFile(cdkPath)) {
    cdk = files.read(cdkPath)
    if (cdk != "") {
        ui.card.text(cdk)
    }
} else {
    files.createWithDirs(cdkPath);
}
var w = floaty.rawWindow(
    <frame gravity="center">
        <text id="text">读取信息中</text>
    </frame>
);

w.setPosition(0, 0);
w.setTouchable(true)


var runthreadsclosed = true
var isStarted = true

var a = 0
//显示上层权限 悬浮窗
// app.startActivity({
//     action: android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
//     data: android.net.Uri.parse("package:" + context.getPackageName())
// });
if (!floaty.checkPermission()) {

    app.startActivity({
        action: android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
        data: android.net.Uri.parse("package:" + context.getPackageName())
    });
}

function checkSelfPermission() {
    mylog("依次看好！请授予修改系统设置.悬浮窗，的权限,请手动开启自启动权限 关闭任何电池优化！让他不限制,请找到无障碍中的auto这个应用，打开他的无障碍权限，如果有按钮请打开按钮");
    app.startActivity({
        action: android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
        data: android.net.Uri.parse("package:" + context.getPackageName())
    });

    app.startActivity({
        action: "android.settings.APPLICATION_DETAILS_SETTINGS",
        data: android.net.Uri.parse("package:" + context.getPackageName())
    });

    if (!android.provider.Settings.System.canWrite(context)) {

        app.startActivity(
            new Intent(
                android.provider.Settings.ACTION_MANAGE_WRITE_SETTINGS,
                app.parseUri("package:" + context.getPackageName())
            )
        );
    }

    app.startActivity(
        new android.content.Intent()
            .setAction(android.provider.Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            .setData(android.net.Uri.parse("package:" + context.packageName))
    );

    if (auto.service == null) {
        app.startActivity({
            action: "android.settings.ACCESSIBILITY_SETTINGS",
        });
    }
}
// }
if (!android.provider.Settings.System.canWrite(context)) {
    mylog("请授予修改系统设置的权限");
    app.startActivity(
        new Intent(
            android.provider.Settings.ACTION_MANAGE_WRITE_SETTINGS,
            app.parseUri("package:" + context.getPackageName())
        )
    );
}
if (context.checkSelfPermission(android.Manifest.permission.CALL_PHONE) == -1) {
    // 如果没有权限，引导用户到应用的设置界面
    mylog("请授予拨打电话的权限");
    app.startActivity(
        new Intent(
            android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
            android.net.Uri.parse("package:" + context.getPackageName())
        )
    );
} else {
    // toast("已经拥有拨打电话的权限");
}
if (auto.service == null) {
    mylog("请找到无障碍中的auto这个应用，打开他的无障碍权限，如果有按钮请打开按钮");
    app.startActivity({
        action: "android.settings.ACCESSIBILITY_SETTINGS",
    });
}
// runtime.requestPermissions([
//     "android.permission.CALL_PHONE"
// ])

// runtime.requestPermissions(["android.permission.CALL_PHONE"], function(granted) {
//     if (granted) {
//         toast("拨打电话权限已授予");
//         // 在此处执行拨打电话的操作
//         // callPhoneFunction();  // 假设你有一个拨打电话的函数
//     } else {
//         toast("拨打电话权限被拒绝");
//     }
// });
// ui.emitter.on("request_permission_result", function () {
//     mylog(arguments); // { '0': 100, '1': [android.permission.CAMERA], '2': [-1] }
//     // java 对应的方法
//     // onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults)
//   });
// runtime.requestPermissions(activity, ["android.permission.CALL_PHONE"], 100);

// 生成一个范围内的随机时间（毫秒）
function getRandomTime(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 随机点击某个位置
function randomClick(x, y, root) {
    var delay = getRandomTime(100, 700); // 随机延迟500ms到2000ms之间
    sleep(delay);
    if (root) {
        Tap(x, y)
    } else {
        click(x, y);
    }
}
// 随机按住某个位置
function randomPress(x, y, isroot) {
    var delay = getRandomTime(100, 400); // 随机延迟500ms到2000ms之间
    sleep(delay);
    var delay2 = getRandomTime(100, 400); // 随机延迟500ms到2000ms之间
    if (isroot) {
        // rootTap.press(x, y, delay2);

        press(x, y, delay2);
    } else {

        press(x, y, delay2);
    }
}
// 随机滑动
function randomSwipe(startX, startY, distance, duration, isroot) {
    var endX = startX + distance * (Math.random() < 0.5 ? 1 : -1); // 随机滑动方向
    var endY = startY + distance * (Math.random() < 0.5 ? 1 : -1);
    if (isroot) {
        Swipe(startX, startY, endX, endY, duration);
    } else {
        swipe(startX, startY, endX, endY, duration);
    }
}

// 随机点击或者滑动或者按住
function randomTap(element, isroot) {
    if (element) {
        var bounds = element.bounds(); // 获取控件的边界
        var width = bounds.width();
        var height = bounds.height();
        // log(width, height, bounds.left, bounds.right)
        // 计算20%区域
        var offsetX = width * 0.1; // 20% 的宽度
        var offsetY = height * 0.1; // 20% 的高度
        let manner = Math.random();
        // 随机选择执行点击或滑动
        var actionType = manner < 0.666 ? manner < 0.333 ? "press" : "click" : "swipe";
        // log(actionType)
        if (actionType === "click") {
            // 在控件内的20%区域随机点击
            var x = getRandomTime(bounds.left + offsetX, bounds.right - offsetX);
            var y = getRandomTime(bounds.top + offsetY, bounds.bottom - offsetY);
            randomClick(x, y, isroot);

        } else if (actionType === "swipe") {
            // 在控件内的20%区域随机滑动
            var startX = getRandomTime(bounds.left + offsetX, bounds.right - offsetX);
            var startY = getRandomTime(bounds.top + offsetY, bounds.bottom - offsetY);
            var distance = getRandomTime(1, 5); // 滑动距离1到20像素
            var duration = getRandomTime(100, 800); // 滑动时间0.1s到1.5s（以毫秒为单位）
            randomSwipe(startX, startY, distance, duration, isroot);
        } else {
            var x = getRandomTime(bounds.left + offsetX, bounds.right - offsetX);
            var y = getRandomTime(bounds.top + offsetY, bounds.bottom - offsetY);
            randomPress(x, y, isroot);
        }
    } else {
        log("未能点击指定的控件，此控件的变量异常: " + selectText);
    }
}

function mylog(content) {
    toastLog(content)
    let timefile = logPath + getDatetimeDay() + ".txt";
    if (files.isFile(timefile)) {
        let logfile = open(timefile, mode = "a", encoding = "utf-8", bufferSize = 8192)
        // logfile = files.read(timefile)
        logfile.writeline(getDatetime() + ": " + content)
        logfile.close()
    } else {
        files.createWithDirs(timefile);
        let logfile = open(timefile, mode = "a", encoding = "utf-8", bufferSize = 8192)
        // logfile = files.read(timefile)
        logfile.writeline(getDatetime() + ": " + content)
        logfile.close()
    }
}
function printtokenlog(content) {
    let tokenfile = tokenPath + getDatetimeDay() + ".txt";
    if (files.isFile(tokenfile)) {
        let logfile = open(tokenfile, mode = "a", encoding = "utf-8", bufferSize = 8192)
        // logfile = files.read(timefile)
        logfile.writeline(getDatetime() + ": " + content)
        logfile.close()
    } else {
        files.createWithDirs(tokenfile);
        let logfile = open(tokenfile, mode = "a", encoding = "utf-8", bufferSize = 8192)
        // logfile = files.read(timefile)
        logfile.writeline(getDatetime() + ": " + content)
        logfile.close()
    }
}
//容错函数，不允许输入自建找控件函数，会陷入回调地狱
function fault() {
    if (textContains("拨打电话和管理通话吗").exists()) {
        textContains("拒绝").findOne().click()
    }
    if (textContains("访问您的手机通话记录").exists()) {
        textContains("拒绝").findOne().click()
    }
    if (textContains("访问您的通讯录").exists()) {
        textContains("拒绝").findOne().click()
    }
    if (textContains("访问您设备上的照片").exists()) {
        textContains("拒绝").findOne().click()
    }
    if (textContains("您需要使用官方 WhatsApp 才能登录").exists()) {
        mylog("whatsapp异常")
        sleep(1000)
        clearapp()
        sendfailnow = true
    }
}

//是否存在
function isExistsNow(selectext, sleeptime) {
    fault()
    returnStatus = false
    let isExists = selectext.exists();
    if (!sleeptime || sleeptime == null || sleeptime == undefined) {
        if (isExists) {
            returnStatus = true
        } else {
            returnStatus = false
        }

        return returnStatus
    } else {
        sleeptime = sleeptime * 10
    }

    for (let index = 0; index < sleeptime; index++) {
        sleep(100)
        fault()
        isExists = selectext.exists();
        if (isExists) {
            returnStatus = true
            break
        }
        if (index == sleeptime - 1) {
            returnStatus = false
            mylog("未找到：" + selectext);
            log("未找到：" + selectext);
            break
        }
    }
    return returnStatus
}
//存在则点击
function isExistsTouch(selectext, sleeptime) {
    fault()
    returnStatus = false
    let isExists = selectext.exists();
    if (!sleeptime || sleeptime == null || sleeptime == undefined) {
        if (isExists) {
            returnStatus = true
            let elem = selectext.findOne();
            randomTap(elem)

            log("模拟点击：" + selectext)
        } else {
            returnStatus = false
        }

        return returnStatus

    } else {
        sleeptime = sleeptime * 10
    }

    for (let index = 0; index < sleeptime; index++) {
        sleep(100)
        fault()
        isExists = selectext.exists();
        if (isExists) {
            returnStatus = true
            let elem = selectext.findOne();
            randomTap(elem)

            log("模拟点击：" + selectext)
            break
        }
        if (index == sleeptime - 1) {
            returnStatus = false
            mylog("未找到：" + selectext);
            log("未找到：" + selectext);
            break
        }
    }
    return returnStatus
}
function shellCA() {
    shell("input keyevent --longpress 113", true)
    shell("input keyevent 29", true)
    shell("input keyevent 113", true)
}
//存在则输入
function isExistsInput(selectext, inputext, sleeptime) {
    fault()
    returnStatus = false

    let isExists = selectext.exists();
    if (!sleeptime || sleeptime == null || sleeptime == undefined) {
        if (isExists) {
            returnStatus = true
            let elem = selectext.findOne();
            rootTap()
            randomTap(elem)
            // shellCA()
            // sleep(1000)
            KeyCode(61)

            KeyCode(61)
            Text(inputext)
            // elem.setText(inputext)

            mylog("输入文字:" + inputext)
        } else {
            returnStatus = false
        }

        return returnStatus
    } else {
        sleeptime = sleeptime * 10
    }

    for (let index = 0; index < sleeptime; index++) {
        sleep(100)
        fault()
        isExists = selectext.exists();
        if (isExists) {
            returnStatus = true
            let elem = selectext.findOne();

            randomTap(elem)
            mylog("输入文字:" + inputext)
            elem.setText(inputext)
            break
        }
        if (index == sleeptime - 1) {
            returnStatus = false
            mylog("未找到：" + selectext);
            log("未找到：" + selectext);
            break
        }
    }
    return returnStatus
}


//等待出现则输入,带提前返回,单位秒,判断是否大于0
function isExistsInputExit(selectext, exitext, inputext, sleeptime) {
    returnStatus = 0
    if (!sleeptime || sleeptime == null || sleeptime == undefined) {
        sleeptime = 300
    } else {
        sleeptime = sleeptime * 10
    }
    for (let index = 0; index < sleeptime; index++) {
        sleep(100)
        fault()
        //提前找到待出现控件 退出
        if (exitext && exitext != null && exitext != undefined && exitext.exists()) {
            returnStatus = 2
            break
        }
        if (selectext.exists()) {

            //成功找到控件 点击退出
            returnStatus = 1
            const elem = selectext.findOne();
            // elem.setText()
            elem.setText(inputext)
            mylog("输入文字:" + inputext)
            randomTap(elem)

            elem.performAction("select_all")

            press(67)
            Text(inputext)
            // } else {
            //     elem.setText(inputext)
            // }
            break
        }
        if (index == sleeptime - 1) {

            returnStatus = -1
            mylog("未找到：" + selectext);
            log("未找到：" + selectext);
            break
        }
    }
    return returnStatus
}
//等待出现则点击,带提前返回,单位秒,判断是否大于0
function isExistsTouchExit(selectext, exitext, sleeptime) {
    returnStatus = 0
    if (!sleeptime || sleeptime == null || sleeptime == undefined) {
        sleeptime = 300
    } else {
        sleeptime = sleeptime * 10
    }
    for (let index = 0; index < sleeptime; index++) {
        sleep(100)
        fault()
        //提前找到待出现控件 退出
        if (exitext && exitext != null && exitext != undefined && exitext.exists()) {
            returnStatus = 2
            break
        }
        if (selectext.exists()) {
            //成功找到控件 点击退出
            returnStatus = 1
            let elem = selectext.findOne();
            randomTap(elem)

            log("模拟点击：" + selectext)
            break
        }
        if (index == sleeptime - 1) {
            returnStatus = -1
            mylog("未找到：" + selectext);
            log("未找到：" + selectext);
            break
        }
    }
    return returnStatus
}
// log(2332)
function test() {
    //模拟 测试
    while (true) {
        getcode()
        sleep(100)
        fault()
        if (isExistsTouchExit(idEndsWith("com.whatsapp.w4b:id/continue_button_group"), textContains("下一步"), 3) > 0) {
            isExistsTouch(textContains("下一步"))
        }
    }
}
function getcode() {
    var rungetcode = true
    var rungetcodetime = 0
    while (rungetcode == true) {
        rungetcodetime = rungetcodetime + 1

        if (rungetcodetime >= 230) {

            // printscreen("验证码超时")
            // clearapp()
            sendfailnow = true
            rungetcode = false
            break;
        }
        sleep(100)

        //输入电话号码提交按钮存在 下一步
        if (isExistsTouch(idEndsWith("com.whatsapp.w4b:id/registration_submit"))) {
            // //重发验证吗按钮
            // if (isExistsNow("com.whatsapp.w4b:id/fallback_methods_entry_button")) {

            // }
            //检查提交注册按钮

            isExistsTouch(idEndsWith("android:id/button1"), 1)
        }
        // fault()
        // let sendenable = false
        let sendenable = false
        let linknow = false
        let sendnow = false
        //接受验证码
        if (isExistsNow(textContains("正在验证..."))) {
            sendenable = true
        }
        if (isExistsNow(textContains("此手机号码已注册"))) {

        }
        if (isExistsNow(textContains("正在发送验证码..."))) {
            sendnow = true
        }
        if (isExistsNow(textContains("无法发送验证短信"))) {
            // sendnow = true
            mylog("无法发送")
            sendfailnow = true
            rungetcode = false
            break
        }
        if (isExistsNow(textContains("正在连接..."))) {
            linknow = true
        }
        if (isExistsNow(textContains("您需要使用官方 WhatsApp 才能登录"))) {
            mylog("whatsapp异常")
            sendfailnow = true
            rungetcode = false
            break
        }
        //其他方式验证
        if (isExistsNow(idEndsWith("com.whatsapp.w4b:id/secondary_button")) && isExistsNow((textContains("其他方式验证")))) {
            idEndsWith("com.whatsapp.w4b:id/secondary_button").findOne().click()

            isExistsTouchExit(className("android.widget.LinearLayout").depth("10").drawingOrder("2"), undefined, 5)

        }
        //不是有效的
        if (isExistsNow(textContains("不是有效的"))) {
            mylog(textContains("不是有效的").findOne().text())
            sendfailnow = true
            rungetcode = false
            break
            //换号码
        }
        //没有收到验证码
        if (isExistsNow(textContains("没有收到验证码"))) {
            // idEndsWith("com.whatsapp.w4b:id/secondary_button").findOne().click()
            if (isExistsTouch((textContains("重发短信")))) {

            }
            // isExistsTouchExit(className("android.widget.LinearLayout").depth("10").drawingOrder("2"), undefined, 5)

        }
        //其他方式验证弹出
        if (isExistsNow(textContains("通过未接来电自动完成验证："))) {
            // linknow = true
            //其他方式验证
            //选择短信
            if (isExistsTouchExit(idEndsWith("com.whatsapp.w4b:id/continue_button_group"), textContains("下一步"), 3) > 0) {
                isExistsTouch(textContains("下一步"))
            }
        }
        if (isExistsNow(textContains("我们无法发送短信至您的号码，请检查您的号码并于"))) {
            mylog(textContains("我们无法发送短信至您的号码，请检查您的号码并于").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
            sendfailnow = true
            rungetcode = false
            break
        }
        if (isExistsNow(textContains("请输入您的电话号码"))) {
            mylog(textContains("请输入您的电话号码").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains("电话号码长度在此国家无效:"))) {
            mylog(textContains("电话号码长度在此国家无效").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains("无法连接，请稍后再试:"))) {
            mylog(textContains("无法连接，请稍后再试").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains("的有效电话号码:"))) {
            mylog(textContains("的有效电话号码").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains("此电话号码是否正确？"))) {
            mylog(textContains("此电话号码是否正确？").findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains('请先点击 "重发短信" 或 "致电给我"'))) {
            mylog(textContains('请先点击 "重发短信" 或 "致电给我"').findOne().text())
            randomTap(idEndsWith("android:id/button1").findOne())
        }
        if (isExistsNow(textContains("小时"))) {
            mylog(textContains("小时").findOne().text())
            sendfailnow = true
            rungetcode = false
            break
        }

    }
}
function random(prefix, randomLength) {
    // 兼容更低版本的默认值写法
    prefix === undefined ? prefix = "" : prefix;
    randomLength === undefined ? randomLength = 8 : randomLength;

    // 设置随机用户名
    // 用户名随机词典数组
    let nameArr = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "g", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    ]
    // 随机名字字符串
    let name = prefix;
    // 循环遍历从用户词典中随机抽出一个
    for (var i = 0; i < randomLength; i++) {
        // 随机生成index
        let index = Math.floor(Math.random() * 2);
        let zm = nameArr[index][Math.floor(Math.random() * nameArr[index].length)];
        // 如果随机出的是英文字母
        if (index === 1) {
            // 则百分之50的概率变为大写
            if (Math.floor(Math.random() * 2) === 1) {
                zm = zm.toUpperCase();
            }
        }
        // 拼接进名字变量中
        name += zm;
    }
    // 将随机生成的名字返回
    return name;
}
var getoken = false
var sendfailnow = false
var delaytime = 0
function inputcode(number) {
    while (true) {
        if (isExistsNow(textContains("创建目录"))) {
            // 设置名字成功之后的下一步的下一步 创建目录
            if (isExistsTouch(textContains("以后再说"))) {


            }
        }
        if (isExistsNow(textContains("显示更多选项"))) {
            // 设置名字下面展开更多设置
        }
        if (isExistsNow(textContains("正在初始化"))) {
            // 设置名字成功之后的下一步
        }
        if (isExistsNow(idEndsWith("com.whatsapp.w4b:id/customPanel"))) {
            //网络问题
            if (isExistsTouch(textContains("重试"), 2)) {

            }
        }
        //下一步
        if (isExistsNow(idEndsWith("com.whatsapp.w4b:id/register_name_accept"))) {
            //商业名字
            if (isExistsInput(idEndsWith("com.whatsapp.w4b:id/registration_name"), random("test", 10)), 2) {
                //选商业模式
                if (isExistsTouchExit(idEndsWith("com.whatsapp.w4b:id/form_field_main_label_container"), textContains("建议"))) {
                    //选商业模式第一个
                    isExistsTouchtExit(className("android.widget.LinearLayout").depth("9"), idEndsWith("com.whatsapp.w4b:id/register_name_accept"), 2)
                    sleep(600)
                    //下一步
                    isExistsTouch(idEndsWith("com.whatsapp.w4b:id/register_name_accept"), 2)
                }
            }
        }
        if (textContains("正在验证...").exists()) {

        }
        //verification_complete_message
        if (textContains("验证完毕").exists()) {

        }
        if (textContains("正在加载...").exists()) {

        }
        if (textContains("要轻松向").exists()) {
            if (isExistsTouch(textContains("继续"), 2)) {

            }
        }
        if (isExistsNow(textContains("WA Business")) && isExistsNow(textContains("WhatsApp Business"))) {
            //登录成功
            mylog("登录成功")
            printscreen("登录成功" + nownumber)
        }
        if (textContains("还原备份数据").exists()) {
            if (isExistsTouch(textContains("取消"), 2)) {

            }
        }
        //有验证码输入验证码
        isExistsInput(idEndsWith("com.whatsapp.w4b:id/code_input_and_progress_bar"), number)
    }
}

var nownumber = ""

// var rootTap = new RootAutomator()
// log(234234)
function register(number) {
    //切换到新号码逻辑，将控制变量置空
    getoken = false
    sendfailnow = false
    delaytime = 0
    nownumber = number

    inputcode(123232)
    clearapp()
    lunchapp("com.whatsapp.w4b")
    while (getoken == false) {
        sleep(100)
        delaytime = delaytime + 1
        fault()
        a = a + 1
        if (a % 100 == 0) {
            mylog("正在运行中....")
        }


        if (isStarted) {
            // clearapp()
            //启动whatsapp存在
            isExistsTouch(idEndsWith("com.whatsapp.w4b:id/next_button"))
            //同意并继续存在
            isExistsTouch(idEndsWith("com.whatsapp.w4b:id/eula_accept"))
            //输入电话号码select存在 进入输验证码环节
            if (isExistsNow(idEndsWith("com.whatsapp.w4b:id/registration_country"))) {
                isExistsTouch(idEndsWith("com.whatsapp.w4b:id/registration_country"), 1)
                //城市代码控件是否存在
                if (isExistsNow(textContains("选择国家"), 2)) {
                    if (idEndsWith("com.whatsapp.w4b:id/menuitem_search").exists()) {
                        idEndsWith("com.whatsapp.w4b:id/menuitem_search").findOne().click()
                        sleep(800)
                        //输入框不能编辑
                        // className("android.widget.LinearLayout").depth("7").findOne().setText("34")
                        Text("86")
                        sleep(200)
                        isExistsTouch(className("android.widget.LinearLayout").depth("7").drawingOrder("1"))
                        sleep(200)

                        //输入电话号码edit存在
                        if (isExistsInputExit(idEndsWith("com.whatsapp.w4b:id/registration_phone"), undefined, number, 1) > 0) {
                            getcode()
                            // inputcode()
                        }
                    }
                }
            }


        }
        // if (idEndsWith("com.tencent.mm:id/odb").exists()) {
        //     var text = idEndsWith("com.tencent.mm:id/odb").findOne().text()
        //     // mylog(text)
        //     var Intent = {
        //         action: "android.intent.action.CALL",
        //         data: "tel:" + text.substring(0, 11)
        //     };
        //     // var Intent = {
        //     //     action: "DIAL",
        //     //     data: "tel:"+text.substring(0, 11)
        //     // };
        //     // Intent = {
        //     //     action: "android.intent.action.DIAL",
        //     //     data: "tel:"+text.substring(0, 11)
        //     //     }

        //     isStarted = false

        //     app.startActivity(Intent)
        //     // app.startActivity(Intent);
        // }
        //找到了对应的token
        //app清除应用数据
        if (getoken) {
            printtokenlog(token)
            mylog("手机号获取token成功:" + number)
            break
        } else if (sendfailnow) {
            printscreen("验证码超时" + nownumber)
            mylog("验证码获取超时:" + number)
            clearapp()

            break
        } else {
            if (delaytime > 1000) {
                printscreen("注册时间过长" + nownumber)
                clearapp()
                // 执行shell命令
                mylog("注册时间过长:" + number)
                break
            }
        }

    }
    // else {
    // if (idEndsWith("com.tencent.mm:id/o4q").exists()) {
    //     isStarted = true
    // }

    // }
}
function clearapp() {

    let command = "pm clear com.whatsapp.w4b android.permission.SYSTEM_ALERT_WINDOW";
    shell(command, true)
    sleep(1000)
}
function starthreads() {

    //如果开启 控制在线数量 每次卡密登录前需要调用退出登录, 没有开启 限制登录次数 这里不用管
    //从tokenPath路径 读取token
    // if (files.isFile(tokenPath)) {
    //     token = files.read(tokenPath)
    //     if (token != "") {
    //         qcysdk.CardLogout(token)
    //     }
    // } else {
    //     files.createWithDirs(tokenPath);
    // }

    // getScreenCapture()
    // if (files.isFile(cdkPath)) {
    //     cdk = files.read(cdkPath)
    //     if (cdk != "") {
    //         ui.card.text(cdk)
    //     }
    // } else {
    //     files.createWithDirs(cdkPath);
    // }

    var phonepath = "/sdcard/whatsapp/"
    var txtFiles = files.listDir(phonepath, function (name) {
        return name.endsWith('phone.txt');
    });
    //最后一个文件
    var phonefile = open(files.join(phonepath, txtFiles.pop()));

    qcysdk.SetCard(ui.card.text());
    //登录卡密
    // let login_ret = qcysdk.CardLogin();
    //if (login_ret.code === 0) {
    if (true) {
        // files.write(tokenPath, login_ret.result.token);

        // files.write(cdkPath, ui.card.text());
        // 监听多任务键按下事件

        if (runthreadsclosed) {
            if (runthreads && runthreads.isAlive()) {
                log("停止run线程....")
                runthreadsclosed = true
                runthreads.interrupt()
            }
            // mylog("到期时间：" + login_ret.result.expires + "登录成功！")
            runthreads = threads.start(function () {
                runthreadsclosed = false
                // events.onKeyDown("volume_down", function(event){
                //     isStarted=!isStarted
                // });

                // k.swipe(130, 1425, 621, 1430, 5)
                // k.tap(599, 1767)
                // k.swipe(599, 1767, 499, 1767, 50) 点抢单
                // if (take == true) {
                //     // k.swipe(130, 1425, 621, 1430, 5)
                //     // k.tap(599, 1767)
                //     // k.swipe(599, 1767, 499, 1767, 50) 点抢单
                //     if (idEndsWith("com.Union.Driver:id/orderdetail_more").exists()) {
                //         take = false
                //     }
                //     if (idEndsWith("com.Union.Driver:id/car_vehicleno").exists()) {
                //         take = false
                //         // getss = true
                //     }
                //     k.swipe(x, y, x + 490, y, 50)
                //     // sml_move(130, 1425, 621,1430, 50)
                //     // }
                //     // swipe(x, y, x + 490, y, 50)

                // } else {
                //     //132 1413 605
                //     //fullId("com.Union.Driver:id/slideToBackground")
                //     //fullId("com.Union.Driver:id/PerpareRob_bottom_cv")
                //     if (idEndsWith("com.Union.Driver:id/OrderHistory_SelectLoc").exists() && !idEndsWith("com.Union.Driver:id/orderdetail_type").exists()) {

                //         if (idEndsWith("com.Union.Driver:id/slideToBackground").exists()) {

                //             var xxxxx = idEndsWith("com.Union.Driver:id/slideToBackground").findOne().bounds()
                //             var zz = className("android.widget.ImageView").boundsInside(xxxxx.left, xxxxx.top, xxxxx.right, xxxxx.bottom)
                //             if (zz.exists()) {
                //                 var a = zz.findOne()
                //                 x = a.bounds().centerX()
                //                 y = a.bounds().centerY()
                //                 take = true
                //                 // getss = true
                //                 //     console.log(className("android.widget.ImageView").depth(10).findOne().scrollRight())
                //                 //    console.log(className("android.widget.ImageView").depth(10).findOne().scrollForward())
                //             }


                //         }
                //     }
                // }
                phonefile.readlines().forEach((line) => {

                    register(line)
                })

            })
        } else {
            // if (take == false) {
            mylog("重新运行服务！如果无效请检查 1.无障碍权限2.电话权限3.忽略省电模式4.自启动5.后台上锁6.悬浮窗权限！并重启应用")
            // } else {
            runthreadsclosed = true
            starthreads()
            // }
        }
    } else {
        // 登录失败提示
        mylog(login_ret.message);
    }
}
ui.start.click(() => {

    threads.start(function () {
        // ui.run(() => {
        //     var ons = false
        // if (ons == true) {
        //   mylog("你已经登录了呀，去抢单吧")
        // } else {

        starthreads()
    })
    // })
});

ui.checks.click(() => {
    threads.start(function () {
        checkSelfPermission()
    })
})

function lunchapp(packageName) {
    // 检查应用状态
    if (currentPackage() == packageName) {
        mylog("WhatsApp Business is already running.");
    } else {
        mylog("WhatsApp Business is not running. Starting it now...");
        launch(packageName);
    }

}
// if (!requestScreenCapture()) {
//     requestScreenCapture(true)
// }
function getScreenCapture() {
    let Thread = threads.start(function () {
        if (auto.service != null) {  //如果已经获得无障碍权限
            //由于系统间同意授权的文本不同，采用正则表达式
            let Allow = textMatches(/(允许|立即开始|统一)/).findOne(10 * 1000);
            if (Allow) {
                Allow.click();
            }
        }
    });
    if (!requestScreenCapture()) {
        log("请求截图权限失败");
        return false;
    } else {
        Thread.interrupt()
        log("已获得截图权限");
        return true;
    }
}
function printscreen(content) {
    //"screencap -p " +
    var screenpath = imgPath + content + getDatetime() + ".png"


    if (files.isFile(screenpath)) {

        let screenfile = open(screenpath, mode = "a", encoding = "utf-8", bufferSize = 8192)
        screenfile.close()
    } else {
        files.createWithDirs(screenpath);

        let screenfile = open(screenpath, mode = "a", encoding = "utf-8", bufferSize = 8192)
        screenfile.close()
    }
    // logfile = files.read(timefile)
    shell("screencap -p " + screenpath, true)
}

setInterval(() => { }, 1000);
// starthreads()
// 通过 setInterval 保持脚本运行

setImmediate(starthreads);