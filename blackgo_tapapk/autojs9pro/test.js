
"ui";
// $settings.setEnabled('enableAccessibilityServiceByRoot', true);
$settings.setEnabled('not_show_console', true);
// $settings.setEnabled('stop_all_on_volume_up', false);
$settings.setEnabled('foreground_service', true)
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
QCYSDK.prototype.CardUnbindDevice = function () { // 卡密解绑设备，需开发者后台配置
    let method = "POST";
    let path = "/v1/card/unbind_device";
    let data = { "card": this._card, "device_id": this._device_id };
    return this.Request(method, path, data);
}
QCYSDK.prototype.CardUnbindDeviceBybindDevice = function () { // 卡密绑定设备上解绑
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
QCYSDK.prototype.CardUnbindDeviceByPassword = function (password) { // 用户通过解绑密码解绑设备
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
QCYSDK.prototype.UserUnbindDevice = function () { // 用户解绑设备，需开发者后台配置
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
    let path = "/v1/software/latest_ver";
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
            this._startTrialHeartheat();
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
QCYSDK.prototype._startTrialHeartheat = function () {  // 开启试用心跳任务
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


let tokenPath = "/sdcard/token.txt"//保存token的路径
let cdkPath = "/sdcard/cdk.txt"//保存token的路径
let token = ""
//充值卡密点击事件
ui.recharge.click(() => {
    if (!ui.card.text() || !ui.use_card.text()) return toastLog("请输入卡密，和充值使用的卡密")
    let ret = qcysdk.CardRecharge(ui.card.text(), ui.use_card.text())
    if (ret.code === 0) {
        toastLog("卡密充值成功")
    } else {
        toastLog(ret.message)
    }
})
//解绑卡密点击事件
ui.unbind_card.click(() => {
    if (!ui.card.text()) return toastLog("请输入需要解绑的卡密")
    qcysdk.SetCard(ui.card.text());
    let ret = qcysdk.CardUnbindDevice()
    if (ret.code === 0) {
        toastLog("解绑成功")
    } else {
        toastLog(ret.message)
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
            toastLog(login_ret.message);  // 重登失败
            sleep(200);
            exit();  // 退出脚本
        }
    }
});

// 当脚本正常或者异常退出时会触发exit事件
events.on("exit", function () {
    qcysdk.CardLogout(token); // 调用退出登录
    log("结束运行");
});

// var k = new RootAutomator({root: true})
//启动脚本点击事件
// setInterval(() => {
//     // 获取当前前台应用的包名
//     let currentApp = currentPackage();

//     // 检查当前前台应用是否是目标应用
//     if (currentApp === "com.a.a") {
//         test()
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


var take = true
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

// 通过 setInterval 保持脚本运行
setInterval(() => {}, 1000);

function check() {
    toastLog("依次看好！请授予修改系统设置.悬浮窗，的权限,请手动开启自启动权限 关闭任何电池优化！让他不限制,请找到无障碍中的auto这个应用，打开他的无障碍权限，如果有按钮请打开按钮");
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
    toastLog("请授予修改系统设置的权限");
    app.startActivity(
        new Intent(
            android.provider.Settings.ACTION_MANAGE_WRITE_SETTINGS,
            app.parseUri("package:" + context.getPackageName())
        )
    );
}
if (context.checkSelfPermission(android.Manifest.permission.CALL_PHONE) == -1) {
    // 如果没有权限，引导用户到应用的设置界面
    toastLog("请授予拨打电话的权限");
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
    toastLog("请找到无障碍中的auto这个应用，打开他的无障碍权限，如果有按钮请打开按钮");
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
//     toastLog(arguments); // { '0': 100, '1': [android.permission.CAMERA], '2': [-1] }
//     // java 对应的方法
//     // onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults)
//   });
// runtime.requestPermissions(activity, ["android.permission.CALL_PHONE"], 100);

test()
function test() {

    //如果开启 控制在线数量 每次卡密登录前需要调用退出登录, 没有开启 限制登录次数 这里不用管
    //从tokenPath路径 读取token
    if (files.isFile(tokenPath)) {
        token = files.read(tokenPath)
        if (token != "") {
            qcysdk.CardLogout(token)
        }
    } else {
        files.createWithDirs(tokenPath);
    }

    if (files.isFile(cdkPath)) {
        cdk = files.read(cdkPath)
        if (cdk != "") {
            ui.card.text(cdk)
        }
    } else {
        files.createWithDirs(cdkPath);
    }

    qcysdk.SetCard(ui.card.text());
    let login_ret = qcysdk.CardLogin();
    if (login_ret.code === 0) {

        files.write(tokenPath, login_ret.result.token);

        files.write(cdkPath, ui.card.text());
        // 监听多任务键按下事件

        if (take) {

            toastLog("到期时间：" + login_ret.result.expires + "登录成功！")
            threads.start(function () {
                take = false
                // events.onKeyDown("volume_down", function(event){
                //     isStarted=!isStarted
                // });

                // k.swipe(130, 1425, 621, 1430, 5)
                // k.tap(599, 1767)
                // k.swipe(599, 1767, 499, 1767, 50) 点抢单
                while (true) {
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



                    a = a + 1
                    sleep(100)
                    if (a % 50 == 0) {
                        toastLog("正在运行中....")
                    }
                    if (isStarted) {
                        if (idEndsWith("com.tencent.mm:id/odb").exists()) {
                            var text = idEndsWith("com.tencent.mm:id/odb").findOne().text()
                            // toastLog(text)
                            var Intent = {
                                action: "android.intent.action.CALL",
                                data: "tel:" + text.substring(0, 11)
                            };
                            // var Intent = {
                            //     action: "DIAL",
                            //     data: "tel:"+text.substring(0, 11)
                            // };
                            // Intent = {
                            //     action: "android.intent.action.DIAL",
                            //     data: "tel:"+text.substring(0, 11)
                            //     }

                            isStarted = false

                            app.startActivity(Intent)
                            // app.startActivity(Intent);
                        }
                    } else {
                        if (idEndsWith("com.tencent.mm:id/o4q").exists()) {
                            isStarted = true
                        }

                    }
                }
            })

        } else {
            // if (take == false) {
            toastLog("重新运行服务！如果无效请检查 1.无障碍权限2.电话权限3.忽略省电模式4.自启动5.后台上锁6.悬浮窗权限！并重启应用")
            // } else {
            take = true
            test()
            // }
        }
    } else {
        // 登录失败提示
        toastLog(login_ret.message);
    }
}
ui.start.click(() => {

    threads.start(function () {
        // ui.run(() => {
        //     var ons = false
        // if (ons == true) {
        //   toastLog("你已经登录了呀，去抢单吧")
        // } else {

        test()
    })
    // })
});

ui.checks.click(() => {
    threads.start(function () {
        check()
    })
})
