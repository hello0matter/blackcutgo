// 枚举导入表
// var improts = Module.enumerateImports("libencryptlib.so");
// for(let i = 0; i < improts.length; i++){
//     //console.log(JSON.stringify(improts[i]));
//     console.log(improts[i].name + " " + improts[i].address);
// }

// 枚举导出表
// var exports = Module.enumerateExports("libencryptlib.so");
// for(let i = 0; i < exports.length; i++){
//     console.log(exports[i].name + " " + exports[i].address);
// }

// 枚举符号表
// var symbols = Module.enumerateSymbols("libencryptlib.so");
// for(let i = 0; i < symbols.length; i++){
//     console.log(symbols[i].name + " " + symbols[i].address);
// }

// 枚举进程中已加载的模块
// var modules = Process.enumerateModules();
// console.log(JSON.stringify(modules[0].enumerateExports()[0]));

// 导出函数的hook
// var funcAddr = Module.findExportByName("libencryptlib.so", "_ZN7MD5_CTX11MakePassMD5EPhjS0_");
// console.log(funcAddr);
// Interceptor.attach(funcAddr, {
//     onEnter: function (args) {
//         console.log("funcAddr onEnter args[1]: ", hexdump(args[1]));
//         console.log("funcAddr onEnter args[2]: ", args[2].toInt32());
//         this.args3 = args[3];
//     }, onLeave: function (retval) {
//         console.log("funcAddr onLeave args[3]: ", hexdump(this.args3));
//     }
// });

// 各种方式得到so基址
// var module1 = Process.findModuleByName("libencryptlib.so");
// //console.log(JSON.stringify(module1));
// console.log("module1", module1.base);
//
// var module2 = Process.getModuleByName("libencryptlib.so");
// console.log("module2", module2.base);
//
// var soAddr = Module.findBaseAddress("libencryptlib.so");
// console.log("soAddr", soAddr);
//
// var modules = Process.enumerateModules();
// for(let i = 0; i < modules.length; i++){
//     if(modules[i].name == "libencryptlib.so"){
//         console.log(modules[i].name + " " + modules[i].base);
//     }
// }
//
// var module = Process.findModuleByAddress(Module.findBaseAddress("libencryptlib.so"));
// console.log("module " + module.name + " " + module.base);

// hook任意函数
// var soAddr = Module.findBaseAddress("libencryptlib.so");
// // var so = 0x77ab999000;
// // console.log(ptr(so).add(0x1FA38)); // new NativePointer()
// var funcAddr = soAddr.add(0x1FA38);
// Interceptor.attach(funcAddr, {
//     onEnter: function (args) {
//         console.log("funcAddr onEnter args[1]: ", hexdump(args[1]));
//         console.log("funcAddr onEnter args[2]: ", args[2].toInt32());
//         this.args3 = args[3];
//     }, onLeave: function (retval) {
//         console.log("funcAddr onLeave args[3]: ", hexdump(this.args3));
//     }
// });

// 有手就行的so hook
function print_arg(addr) {
    var module = Process.findRangeByAddress(addr);
    if (module != null) return hexdump(addr) + "\n";
    return ptr(addr) + "\n";
}

function hook_native_addr(funcPtr, paramsNum) {
    var module = Process.findModuleByAddress(funcPtr);
    Interceptor.attach(funcPtr, {
        onEnter: function (args) {
            this.logs = [];
            this.params = [];
            this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
            for (let i = 0; i < paramsNum; i++) {
                this.params.push(args[i]);
                this.logs.push("this.args" + i + " onEnter: " + print_arg(args[i]));
            }
        }, onLeave: function (retval) {
            for (let i = 0; i < paramsNum; i++) {
                this.logs.push("this.args" + i + " onLeave: " + print_arg(this.params[i]));
            }
            this.logs.push("retval onLeave: " + print_arg(retval) + "\n");
            console.log(this.logs);
        }
    });
}

//打印内存中的明文字符串
// var soAddr = Module.findBaseAddress("liblogin_encrypt.so");
// console.log(hexdump(soAddr.add(0xD090)));

//修改函数数值参数和返回值
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var add = soAddr.add(0x165C);
// Interceptor.attach(add, {
//     onEnter: function (args) {
//         args[2] = ptr(1000); // new NativePointer
//         console.log(args[2].toInt32());
//         console.log(args[3]);
//         console.log(args[4]);
//     }, onLeave: function (retval) {
//         retval.replace(1000);
//         console.log(retval.toInt32());
//     }
// });


function stringToBytes(str) {
    return hexToBytes(stringToHex(str));
}

// Convert a ASCII string to a hex string
function stringToHex(str) {
    return str.split("").map(function (c) {
        return ("0" + c.charCodeAt(0).toString(16)).slice(-2);
    }).join("");
}

function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;
}

// Convert a hex string to a ASCII string
function hexToString(hexStr) {
    var hex = hexStr.toString();//force conversion
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

// 修改函数字符串参数
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Update = soAddr.add(0x1D68);
// Interceptor.attach(MD5Update, {
//     onEnter: function (args) {
//         if(args[1].readCString() == "xiaojianbang"){
//             var newStr = "xiaojian";
//             args[1].writeByteArray(hexToBytes(stringToHex(newStr) + "00"));
//             console.log(hexdump(args[1]));
//             args[2] = ptr(newStr.length);
//             console.log(args[2].toInt32());
//         }
//     }, onLeave: function (retval) {
//
//     }
// });

// frida操作C语言结构体
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Update = soAddr.add(0x1D68);
// Interceptor.attach(MD5Update, {
//     onEnter: function (args) {
//         this.args0 = args[0];
//         this.args1 = args[1];
//         // if(args[1].readCString() == "xiaojianbang"){
//         //     args[1] = soAddr.add(0x38A1);
//         //     console.log(hexdump(args[1]));
//         //     args[2] = ptr(soAddr.add(0x38A1).readCString().length);
//         //     console.log(args[2].toInt32());
//         // }
//     }, onLeave: function (retval) {
//         if(this.args1.readCString() == "xiaojianbang"){
//             console.log(hexdump(this.args0.add(24).writeByteArray(stringToBytes("dadajianbang"))));
//         }
//     }
// });

// frida构造新的字符串 以及需要注意的细节
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Update = soAddr.add(0x1D68);
// var newStr = "gdfgdhfgjghjgkhjkh;kl;k;";
// var newStrAddr = Memory.allocUtf8String(newStr);
// Interceptor.attach(MD5Update, {
//     onEnter: function (args) {
//         this.args0 = args[0];
//         this.args1 = args[1];
//         if(args[1].readCString() == "xiaojianbang"){
//             args[1] = newStrAddr;
//             console.log(hexdump(args[1]));
//             args[2] = ptr(newStr.length);
//             console.log(args[2].toInt32());
//         }
//     }, onLeave: function (retval) {
//         if(this.args1.readCString() == "xiaojianbang"){
//             console.log(hexdump(this.args0));
//         }
//     }
// });

//获取指针参数返回值
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Final = soAddr.add(0x3540);
// Interceptor.attach(MD5Final, {
//     onEnter: function (args) {
//         this.args1 = args[1];
//     }, onLeave: function (retval) {
//         console.log(hexdump(this.args1));
//     }
// });

// 内存读写
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log(hexdump(soAddr.add(0x38A1)));
// console.log(soAddr.add(0x38A1).readCString());
// console.log(soAddr.add(0x38A1).writeByteArray(stringToBytes("0123456789abcdef")));
// console.log(soAddr.add(0x38A1).readByteArray(33));
//
// var addr = Memory.alloc(13);
// addr.writeByteArray(stringToBytes("xiaojianbang\0"));
// console.log(addr.readByteArray(13));
// var str = Memory.allocUtf8String("xiaojianbang");
// console.log("Memory.allocUtf8String: ", str.readByteArray(13));
//

// frida修改so函数代码
// function xiugaiCode() {
//     var soAddr = Module.findBaseAddress("libxiaojianbang.so");
//
//     // var codeAddr = soAddr.add(0x1684);
//     // Memory.protect(codeAddr, 4, 'rwx');
//     // codeAddr.writeByteArray(hexToBytes("0001094B"));  //sub w0, w8, w9
//     // console.log(Instruction.parse(codeAddr).toString());
//     //
//     // new Arm64Writer(soAddr.add(0x167C)).putNop();
//     // console.log(Instruction.parse(soAddr.add(0x167C)).toString());
//
//     var codeAddr = soAddr.add(0x1684);
//     Memory.patchCode(codeAddr, 4, function (code) {
//         var writer = new Arm64Writer(code, { pc: codeAddr });
//         writer.putBytes(hexToBytes("0001094B"));  //sub w0, w8, w9
//         writer.putBytes(hexToBytes("FF830091"));  //ADD SP, SP, #0x20
//         writer.putRet();
//         writer.flush();
//     });
// }

// so层module主动调用任意函数模板
function libhello() {
    Java.perform(function () {
        var soAddr = Module.findBaseAddress("libhello-jni.so");
        var funAddr = soAddr.add(0x1CFF0);
        var jstr2cstr = new NativeFunction(funAddr, 'int', ['pointer', 'int', 'pointer']);
        // var env = Java.vm.tryGetEnv();
        // var jstring = env.newStringUtf("xiaojianbang");
        let str = "0123456789abcdef";
        var jstring = Memory.allocUtf8String(str);
        let length = str.length;
        var retjstring = Memory.alloc(length)
        var retval = jstr2cstr(jstring, length, retjstring);
    });
}

//hooklibc读写文件
function writeTxt() {
    var fopenAddr = Module.findExportByName("libc.so", "fopen");
    var fputsAddr = Module.findExportByName("libc.so", "fputs");
    var fcloseAddr = Module.findExportByName("libc.so", "fclose");
    console.log(fopenAddr, fputsAddr, fcloseAddr);

    var fopen = new NativeFunction(fopenAddr, 'pointer', ['pointer', 'pointer']);
    var fputs = new NativeFunction(fputsAddr, 'int', ['pointer', 'pointer']);
    var fclose = new NativeFunction(fcloseAddr, 'int', ['pointer']);

    var fileName = Memory.allocUtf8String("/data/data/com.xiaojianbang.app/xiaojianbang.txt");
    var openMode = Memory.allocUtf8String("w");
    var data = Memory.allocUtf8String("QQ24358757\n");

    var file = fopen(fileName, openMode);
    console.log(file);
    fputs(data, file);
    fclose(file);
}

//hook libart 来hook jni相关函数
function hook_jni() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    var newStringUtf = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if (symbol.name.indexOf("CheckJNI") == -1 && symbol.name.indexOf("NewStringUTF") != -1 && symbols[i].name.indexOf('ArtMethod') > -1 && symbols[i].name.indexOf('RuntimeCallbacks') < 0) {
            console.log(symbol.name, symbol.address);
            newStringUtf = symbol.address;
        }
    }
    Interceptor.attach(newStringUtf, {
        onEnter: function (args) {
            console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
            console.log("newStringUtf args: ", args[1].readCString());
        }, onLeave: function (retval) {
            console.log("newStringUtf retval: ", retval);
        }
    });
}

function hook_jni2() {
    var envAddr = Java.vm.tryGetEnv().handle.readPointer();
    var funAddr = envAddr.add(48).readPointer();
    //console.log(Instruction.parse(funAddr).toString());
    Interceptor.attach(funAddr, {
        onEnter: function (args) {
            console.log("FindClass args: ", args[1].readCString());
        }, onLeave: function (retval) {
            console.log("FindClass retval: ", retval);
        }
    });
}

function call_jni() {
    var retval = Java.vm.tryGetEnv().newStringUtf("xiaojianbang");
    console.log(retval);
    console.log(Java.vm.tryGetEnv().getStringUtfChars(retval).readCString());
}

function call_jni2() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    var newStringUtf = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if (symbol.name.indexOf("CheckJNI") == -1 && symbol.name.indexOf("NewStringUTF") != -1) {
            console.log(symbol.name, symbol.address);
            newStringUtf = symbol.address;
        }
    }
    var newStringUtf_func = new NativeFunction(newStringUtf, 'pointer', ['pointer', 'pointer']);
    var jstring = newStringUtf_func(Java.vm.tryGetEnv().handle, Memory.allocUtf8String("xiaojianbang"));
    console.log(jstring);

    var envAddr = Java.vm.tryGetEnv().handle.readPointer();
    var GetStringUTFChars = envAddr.add(0x548).readPointer();
    var GetStringUTFChars_func = new NativeFunction(GetStringUTFChars, 'pointer', ['pointer', 'pointer', 'pointer']);
    var cstr = GetStringUTFChars_func(Java.vm.tryGetEnv().handle, jstring, ptr(0));
    console.log(cstr.readCString());

}

// 二级指针的构造
function call_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    var xiugaiStr = soAddr.add(0x17D0);
    var xiugaiStr_func = new NativeFunction(xiugaiStr, 'int64', ['pointer']);
    var strAddr = Memory.allocUtf8String("dajianbang");
    console.log(hexdump(strAddr));
    var finalAddr = Memory.alloc(8).writePointer(strAddr);
    xiugaiStr_func(finalAddr);
    console.log(hexdump(strAddr));
}

function hook_dlsym() {
    var dlsymAddr = Module.findExportByName("libdl.so", "dlsym");
    console.log(dlsymAddr);
    Interceptor.attach(dlsymAddr, {
        onEnter: function (args) {
            this.args1 = args[1];
        }, onLeave: function (retval) {
            var module = Process.findModuleByAddress(retval);
            if (module == null) return;
            console.log(this.args1.readCString(), module.name, retval, retval.sub(module.base));
        }
    });
}

//hook_dlsym();
//java层的普通hook类
function hook_java() {
    Java.perform(function () {
        var HelloJni = Java.use("com.example.hellojni.HelloJni")
        HelloJni.sign2.implementation = function (args) {
            let sign2 = this.sign2("0123456789abcde");
            console.log("sign2 args:", args,sign2);
            return sign2;
        }
    });
}

function hook_libc() {

// 针对性的Hook libc.so 的 指定 函数 追算法
    Interceptor.attach(Module.findExportByName("libc.so", "lrand48"), {
        onEnter: function (args) {
            console.log("[lrand48]: " + args[0].readCString());
        },
        onLeave: function (retval) {
            retval.replace(0x12345678);
            console.log("[lrand48]:", retval);
        }
    });
}

//so层的普通hook包装函数
function hex_dump(p) {
    try {
        return hexdump(p, {length: 64}) + "\r\n";
    } catch (error) {
        return ptr(p) + "\r\n";
    }
}


function hook_native_addr(address, baseaddress) {
    try {
        Interceptor.attach(address, {
            onEnter: function (args) {
                console.log("Enter------------------------------------------------------------------------")
                console.log("[" + ptr(address) + "]: " + ptr(baseaddress) + "\r\n");

                this.arg = [];
                // var maxArgs = 10;  // 假设最多有 10 个参数
                //
                // for (var i = 0; i < maxArgs; i++) {
                //     try {
                //         if (args[i] !== undefined) {
                //             console.log("Arg " + i + ": " + args[i].toString()+":"+(args[i] instanceof NativePointer));
                //         }
                //     } catch (e) {
                //         console.error("Error accessing args[" + i + "]: " + e.message);
                //         break;  // 停止访问，如果遇到错误
                //     }
                // }
                // // 遍历所有参数
                // for (var i = 0; i <maxArgs; i++) {
                //     // 假设参数是指针，可以是字符串或整数等，根据实际情况处理
                //     // try {
                //     //     var value = args[i].readUtf8String();  // 如果参数是字符串指针
                //     // } catch (e) {
                //     var value = args[i];  // 如果参数是整数或其他类型
                //     // }
                //     this.arg.push(value);  // 将参数存入数组
                // }
                // console.log("测试1",args[1]);
                //renew
                // console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');

                this.arg[0] = args[0]
                this.arg[1] = args[1]
                this.arg[2] = args[2]
                this.arg[3] = args[3]
                this.arg[4] = args[4]
                this.arg[5] = args[5]
                this.arg[6] = args[6]
                this.arg[7] = args[7]

                this.lr = this.context.lr
            }, onLeave: function (retval) {
                console.log("Leave------------------------------------------------------------------------")
                console.log("[" + ptr(address) + "]: " + ptr(baseaddress) + "\r\n");

                // console.log("[" + ptr(baseaddress) + "]: \r\n",this.arg)
                for (var i = 0; i < this.arg.length; i++) {
                    // if (canhex(this.arg[i])) {
                    console.log("args[" + i + "]:\r\n" + hex_dump(this.arg[i]) + "\r\n")
                    // }
                }
                console.log("LR:" + ptr(this.lr) + "\r\nBLR:" + ptr(this.lr).sub(address.sub(baseaddress)) + "\r\n")
                console.log("RETVALHEX:\r\n" + hex_dump(retval))
            }
        });
    } catch (e) {
        console.log('Error during hook: ' + e);
    }
}

//so层的普通hook
function hook_native() {
    // Java.vm.getEnv()
    // Process.enumerateModules({
    //     onMatch: function(module) {
    Java.perform(function () {
        // if (module.name === "libhello-jni.so") {
        //     console.log("Module发现: " + module.name + " at " + module.base);
        // 模块加载后你可以在这里调用你的逻辑
        var base_hello_jni = Module.findBaseAddress("libhello-jni.so");

        // Interceptor.attach(base_hello_jni.add(0x809C), {
        //     onEnter: function (args) {
        //         //renew
        //         // console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
        //         console.log("[0x809Chook_native args]: ", args[1].readCString());
        //
        //         this.arg0 = args[0]
        //         this.arg1 = args[1]
        //         this.arg2 = args[2]
        //     }, onLeave: function (retval) {
        //         console.log("[0x809C]:", "\r\nargs[2]:", hexdump(this.arg1, {length: parseInt(this.arg2)}), "retval: ", ptr(retval).readCString());
        //     }
        // });
        // hook_native_addr(base_hello_jni.add(0x12D70), 0x12D70)
        hook_native_addr(base_hello_jni.add(0x1CFF0), 0x1CFF0)
        // }
        // }
        // },
        // onComplete: function() {
        //     // if (!moduleLoaded) {
        //     //     console.log("Waiting for module: libhello-jni" );
        //     //     Process.enumerateModules();
        //     // }
        // }
        // });
    })
}

function print_hex(address) {
    var base_hello_jni = Module.findBaseAddress("libhello-jni.so");
    console.log("打印的值：", hexdump(base_hello_jni.add(address)))
}

function hook_RegisterNatives_libart() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    // var RegisterNatives_addr = Module.findExportByName('_ZN3art3JNI14RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodib');

    var RegisterNatives_addr = null;
    var RegisterNatives = false
    var NewStringUTF = null
    var GetStringUTFChars = null
    var FindClass = null
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        //_ZN3art3JNI15RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodi
        if (symbol.name.indexOf("CheckJNI") == -1 && symbol.name.indexOf("JNI") != -1) {
            if (symbol.name.indexOf("RegisterNatives") > 0) {
                RegisterNatives = true
                RegisterNatives_addr = symbol.address;
                console.log(`libart发现 ${symbol.name} address: ${symbol.address}`)
            } else if (symbol.name.indexOf("GetStringUTFChars") > 0) {
                GetStringUTFChars = symbol.address;
                console.log(`libart发现 ${symbol.name} address: ${symbol.address}`)
            } else if (symbol.name.indexOf("NewStringUTF") > 0) {
                NewStringUTF = symbol.address;
                console.log(`libart发现 ${symbol.name} address: ${symbol.address}`)
            } else if (symbol.name.indexOf("FindClass") > 0) {
                FindClass = symbol.address;
                console.log(`libart发现 ${symbol.name} address: ${symbol.address}`)
            }
        }
    }
    if (RegisterNatives_addr) {
        Interceptor.attach(RegisterNatives_addr, {
            onEnter: function (args) {

                var env = Java.vm.tryGetEnv();
                var className = env.getClassName(args[1]);
                var methodCount = args[3].toInt32();
                console.log(`[RegisterNatives_addr]: ${RegisterNatives_addr}\r\n${className} register method count: ${methodCount}`)
                for (let i = 0; i < methodCount; i++) {
                    var methodName = args[2].add(Process.pointerSize * 3 * i).readPointer().readCString();
                    var signature = args[2].add(Process.pointerSize * 3 * i).add(Process.pointerSize).readPointer().readCString();
                    var fnPtr = args[2].add(Process.pointerSize * 3 * i).add(Process.pointerSize * 2).readPointer();
                    var module = Process.findModuleByAddress(fnPtr);
                    console.log(className, methodName, signature, fnPtr, module.name, fnPtr.sub(module.base));
                    console.log(`${methodName}${signature}\t${module.name}!${fnPtr.sub(module.base)}!${module.base}`)
                }

            }, onLeave: function (retval) {
            }
        });
    }
    // if (GetStringUTFChars) {
    //     Interceptor.attach(GetStringUTFChars, {
    //         onLeave: function (retval) {
    //             console.log("[GetStringUTFChars]:", retval, ptr(retval).readCString());
    //         }
    //     })
    // }
    // if (NewStringUTF) {
    //     Interceptor.attach(NewStringUTF, {
    //         onEnter: function (args) {
    //             console.log("[NewStringUTF]:", args[1], ptr(args[1]).readCString());
    //
    //         }
    //     })
    // }
    // if (FindClass) {
    //     Interceptor.attach(FindClass, {
    //         onEnter: function (args) {
    //             console.log("[FindClass]:", args[1], ptr(args[1]).readCString());
    //
    //         }
    //     })
    // }
}


function inlineHook() {
    // var nativePointer = Module.findBaseAddress("libxiaojianbang.so");
    // var hookAddr = nativePointer.add(0x17BC);
    // Interceptor.attach(hookAddr, {
    //     onEnter: function (args) {
    //         console.log("onEnter: ", this.context.x8);
    //     }, onLeave: function (retval) {
    //         console.log("onLeave: ", this.context.x8.toInt32());
    //         console.log(this.context.x8 & 7);
    //     }
    // });

    var nativePointer = Module.findBaseAddress("libxiaojianbang.so");
    var hookAddr = nativePointer.add(0x1B70);
    Interceptor.attach(hookAddr, {
        onEnter: function (args) {
            console.log("onEnter: ", this.context.x1);
            console.log("onEnter: ", hexdump(this.context.x1));
        }, onLeave: function (retval) {

        }
    });
}

//hook_addr_arg_one
function hook_addr_arg_one(addr, soName, callback) {
    Interceptor.attach(addr, {
        onEnter: function (args) {
            var soPath = args[0].readCString();
            if (soPath.indexOf(soName) != -1) this.hook = true;
        }, onLeave: function (retval) {
            if (this.hook) callback();
        }
    });
}

function hook_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    console.log("soAddr", soAddr);
    var MD5Final = soAddr.add(0x3540);
    Interceptor.attach(MD5Final, {
        onEnter: function (args) {
            this.args1 = args[1];
        }, onLeave: function (retval) {
            console.log(hexdump(this.args1));
        }
    });
}

function hook_JNIOnload() {
    var xiaojianbangAddr = Module.findBaseAddress("libxiaojianbang.so");
    var funcAddr = xiaojianbangAddr.add(0x1CCC);
    Interceptor.replace(funcAddr, new NativeCallback(function () {
        console.log("this func is replaced !");
    }, 'void', []));
}


//升级版本兼容32 64
function hook_call_constructor_ex() {
    if (Process.pointerSize == 4) {
        var linker = Process.findModuleByName("linker");
    } else {
        var linker = Process.findModuleByName("linker64");
    }

    var addr_call_function = null;
    var addr_g_ld_debug_verbosity = null;
    var addr_async_safe_format_log = null;
    if (linker) {
        //console.log("found linker");
        var symbols = linker.enumerateSymbols();
        for (var i = 0; i < symbols.length; i++) {
            var name = symbols[i].name;
            if (name.indexOf("call_function") >= 0) {
                addr_call_function = symbols[i].address;
                // console.log("call_function",JSON.stringify(symbols[i]));
            } else if (name.indexOf("g_ld_debug_verbosity") >= 0) {
                addr_g_ld_debug_verbosity = symbols[i].address;

                ptr(addr_g_ld_debug_verbosity).writeInt(2);

            } else if (name.indexOf("async_safe_format_log") >= 0 && name.indexOf('va_list') < 0) {
                // console.log("async_safe_format_log",JSON.stringify(symbols[i]));
                addr_async_safe_format_log = symbols[i].address;

            }

        }
    }
    if (addr_async_safe_format_log) {
        Interceptor.attach(addr_async_safe_format_log, {
            onEnter: function (args) {
                this.log_level = args[0];
                this.tag = ptr(args[1]).readCString()
                this.fmt = ptr(args[2]).readCString()
                if (this.fmt.indexOf("c-tor") >= 0 && this.fmt.indexOf('Done') < 0) {
                    this.function_type = ptr(args[3]).readCString(), // func_type
                        this.so_path = ptr(args[5]).readCString();
                    var strs = new Array(); //定义一数组
                    strs = this.so_path.split("/"); //字符分割
                    this.so_name = strs.pop();
                    this.func_offset = ptr(args[4]).sub(Module.findBaseAddress(this.so_name))
                    console.log("func_type:", this.function_type,
                        '\nso_name:', this.so_name,
                        '\nso_path:', this.so_path,
                        '\nfunc_offset:', this.func_offset
                    );
                    // hook代码在这加
                }
            },
            onLeave: function (retval) {
            }
        })
    }


}

function hook_call_constructors() {
    var symbols = Process.getModuleByName("linker64").enumerateSymbols();
    var call_constructors_addr = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if (symbol.name.indexOf("__dl__ZN6soinfo17call_constructorsEv") != -1) {
            call_constructors_addr = symbol.address;
        }
    }
    console.log("call_constructors_addr: ", call_constructors_addr);
    Interceptor.attach(call_constructors_addr, {
        onEnter: function (args) {
            if (!isHooked) {
                hook_initarray();
                isHooked = true;
            }
        }, onLeave: function (retval) {
        }
    });
}

function hook_initarray() {
    var xiaojianbangAddr = Module.findBaseAddress("libxiaojianbang.so");
    var func1_addr = xiaojianbangAddr.add(0x1C54);
    var func2_addr = xiaojianbangAddr.add(0x1C7C);
    var func3_addr = xiaojianbangAddr.add(0x1C2C);
    Interceptor.replace(func1_addr, new NativeCallback(function () {
        console.log("func1 is replaced!!!");
    }, 'void', []));

    Interceptor.replace(func2_addr, new NativeCallback(function () {
        console.log("func2 is replaced!!!");
    }, 'void', []));

    Interceptor.replace(func3_addr, new NativeCallback(function () {
        console.log("func3 is replaced!!!");
    }, 'void', []));
}

function hook_pthread_create() {
    var pthread_create_addr = Module.findExportByName("libc.so", "pthread_create");
    console.log("pthread_create_addr: ", pthread_create_addr);
    Interceptor.attach(pthread_create_addr, {
        onEnter: function (args) {
            console.log(args[0], args[1], args[2], args[3]);
            var Module = Process.findModuleByAddress(args[2]);
            if (Module != null) console.log(Module.name, args[2].sub(Module.base));
        }, onLeave: function (retval) {
        }
    })
}

// hook_pthread_create();


//test 函数表遍历并hook ai作品
function hook_RegisterNative_ai() {
    // Hook RegisterNatives to get JNI function pointers
    Interceptor.attach(Module.findExportByName("libart.so", "_ZN3art3JNI14RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodib"), {
        onEnter: function (args) {
            // Get the class name
            var env = args[0];
            var jclass = args[1];
            var methods = args[2];
            var method_count = args[3].toInt32();

            var class_name = Java.vm.getEnv().getClassName(jclass);
            console.log("RegisterNatives called for class: " + class_name);

            // Loop through the methods
            for (var i = 0; i < method_count; i++) {
                var method = methods.add(i * Process.pointerSize * 3);
                var name_ptr = method.readPointer();
                var sig_ptr = method.add(Process.pointerSize).readPointer();
                var fn_ptr = method.add(Process.pointerSize * 2).readPointer();

                var name = name_ptr.readCString();
                var sig = sig_ptr.readCString();

                console.log("Registering native method: " + name + " with signature: " + sig + " at address: " + fn_ptr);

                // Hook the native method
                Interceptor.attach(fn_ptr, {
                    onEnter: function (args) {
                        console.log("Entering native method: " + name + " with signature: " + sig);

                        // Print arguments (if needed)
                        // for (var j = 0; j < args.length; j++) {
                        //     console.log("arg[" + j + "]: " + args[j]);
                        // }
                    },
                    onLeave: function (retval) {
                        console.log("Leaving native method: " + name + " with signature: " + sig);

                        // Modify return value (if needed)
                        // retval.replace(123);
                    }
                });
            }
        },
        onLeave: function (retval) {
            // You can add post-hooking logic here if needed
        }
    });

}

// Hook libc.so 的 printf 函数 没有办法追jni的时候动态追踪最底层
Interceptor.attach(Module.findExportByName("libc.so", "printf"), {
    onEnter: function (args) {
        console.log("printf called with args: " + args[0].readCString());
    },
    onLeave: function (retval) {
        console.log("printf returned");
    }
});

function misc() {

    var dlopen = Module.findExportByName("libdl.so", "dlopen");
    var android_dlopen_ext = Module.findExportByName("libdl.so", "android_dlopen_ext");

    Process.enumerateModules({
        onMatch: function (module) {
            console.log("Module发现: " + module.name + " at " + module.base);
            // 模块加载后你可以在这里调用你的逻辑
        },
        onComplete: function () {
            // if (!moduleLoaded) {
            //     console.log("Waiting for module: libhello-jni" );
            //     Process.enumerateModules();
            // }
        }
    });

    // hook_addr_arg_one(dlopen, "libxiaojianbang.so", inlineHook);
    // hook_addr_arg_one(android_dlopen_ext, "libxiaojianbang.so", inlineHook);
}

function main() {
    //有手就行
    // var soAddr = Module.findBaseAddress("libwtf.so");
    // var MD5Digest = soAddr.add(0xC90 + 1);
    // hook_native_addr(MD5Digest, 3);
    //
    // var get32MD5String = soAddr.add(0x8BC + 1);
    // hook_native_addr(get32MD5String, 2);

    hook_RegisterNatives_libart();
    hook_java()
    hook_native()
    hook_libc()
    // libhello()
    misc()
    // hook_call_constructor_ex()
    // hook_initarray();
    // hook_RegisterNative_ai()

    var isHooked = false;
}

setImmediate(main)

