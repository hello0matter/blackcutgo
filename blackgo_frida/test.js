Java.perform(function () {
    // 获取 File 类
    var File = Java.use("java.io.File");

    // Hook File.delete() 方法
    File.delete.implementation = function () {
        // 获取文件名
        var filePath = this.getAbsolutePath();

        // 检查文件是否以 .mp3 结尾
        if (filePath.endsWith(".mp3")) {
            console.log("Attempting to delete MP3 file: " + filePath);
            // 播放 MP3 文件
            playMp3(filePath);
            // 阻止文件删除
            console.log("Blocked deletion of: " + filePath);
            return false; // 返回 false 阻止删除
        }

        // 对于其他文件，正常删除
        console.log("Deleting file: " + filePath);
        return this.delete(); // 调用原始删除方法
    };

    // 播放 MP3 文件的方法
    function playMp3(filePath) {
        try {
            var MediaPlayer = Java.use("android.media.MediaPlayer");
            var mediaPlayer = MediaPlayer.$new();

            // 设置数据源
            mediaPlayer.setDataSource(filePath);
            mediaPlayer.prepare();
            mediaPlayer.start();

            console.log("Playing MP3 file: " + filePath);
        } catch (e) {
            console.error("Error playing MP3: " + e);
        }
    }
});
