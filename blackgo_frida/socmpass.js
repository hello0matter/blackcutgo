//so层和ass汇编代码进行算法比较测试

function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function call_1CFF0(input_str) {
    var base_hello_jni = Module.findBaseAddress("libhello-jni.so");
    var sub_1CFF0 = new NativeFunction(base_hello_jni.add(0x1CFF0), "int", ["pointer", "int", "pointer"]);
    // var input_str = "0123456789abcdef";

    var arg0 = Memory.allocUtf8String(input_str);
    var arg1 = input_str.length;
    var arg2 = Memory.alloc(arg1);
    sub_1CFF0(arg0, arg1, arg2);
    // console.log(hexdump(arg2, {length : arg1}));

    return arg2;
}

function test_enc() {
    const cm = new CModule(`
    
void enc_function(const char *input_str, int input_len, char *result) {
    const char *table_key1 = "9d9107e02f0f07984956767ab1ac87e5";
    const unsigned char table_key2[] = {0x37, 0x92, 0x44, 0x68, 0xA5, 0x3D, 0xCC, 0x7F, 0xBB, 0xF, 0xD9, 0x88, 0xEE,
                                        0x9A, 0xE9, 0x5A};

    for (int i = 0; i < input_len; ++i) {
//        unsigned char w3 =
        unsigned int w7 = 0xFFFFFFFF;
        unsigned int w2 = i & 0xF;
        unsigned int key2 = table_key2[(i & 0xF) & 0xFFFFFFFF];
//        printf("%02x", w2);

        unsigned int w8 = 0x1579B514;
        w2 = i;
//        w8 = *input_str;
        unsigned int w30 = 0x25;
        w2 = input_str[w2];
        unsigned int w3 = key2;
        w8 = 0xDA;
        w7 = w8 & (~w2);
        w2 = w2 & w30;
        w2 = w7 | w2;
        w7 = w8 & (~w3);
        w3 = w3 & w30;
        w3 = w7 | w3;
        w2 = w2 ^ w3;
        w3 = w2;
//        printf("%x", w2);

//        printf("%02x", w2);
        unsigned int key1 = table_key1[(i ^ 0xFFFFFFF8) & i];
        w2 = key1;
        w7 = key2;
        w30 = key2;
        unsigned int w1 = w2 & (~w3);
        w3 = w3 & (~w2);
//        unsigned char w9 = result;
        unsigned int w5 = w30 & (~w2);
        w2 = w2 & (~w30);
        w1 = w1 | w3;
        w2 = w5 | w2;
        w1 = w1 + w7;
        w8 = i;
        w3 = w1 & (~w2);
        w1 = w2 & (~w1);
//        w5 = w9;
        w1 = w3 | w1;
        result[w8] = w1;
    }
}

      int test_eq(const char* buf1, const char* buf2, int buf_len) {
        for (int i = 0; i < buf_len; ++i) {
            if (buf1[i] != buf2[i]) {
                return 0;
            }
        }
        return 1;
    }
    `)
    var test_eq = new NativeFunction(cm.test_eq, "int", ["pointer", "pointer", "int"]);
    var enc_function = new NativeFunction(cm.enc_function, "void", ["pointer", "int", "pointer"]);

    for (var index = 1; index < 0x100; index++) {
        var input_str = makeid(index);
        var arg0 = Memory.allocUtf8String(input_str);
        var arg1 = input_str.length;
        var arg2 = Memory.alloc(arg1);
        enc_function(arg0, arg1, arg2);
        // console.log(hexdump(arg2, {length : arg1}));
        var test_ret = test_eq(call_1CFF0(input_str), arg2, arg1);
        if (test_ret == 0) {
            console.log(input_str);
        }
    }
    console.log("test_enc end");
}

setImmediate(test_enc)
