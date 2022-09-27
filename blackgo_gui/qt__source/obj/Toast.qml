import QtQuick 2.9

Rectangle {
    id: root
    opacity: 0
    color: "black"
    anchors{
        horizontalCenter: parent.horizontalCenter
        bottom: parent.bottom
        bottomMargin: 20
    }
    height: 50
    radius: 25
    antialiasing: true

    Text {
        id: lab
        color: "white"
        wrapMode: Text.Wrap
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 16
        anchors.centerIn: parent
    }

    SequentialAnimation on opacity {
        id: animation
        running: false
        property int msleep: 2500
        property int showTime: 800
        property int hideTime: 500

        NumberAnimation {
            to: 1
            duration: animation.showTime
        }

        PauseAnimation {
            duration: (animation.msleep - animation.showTime - animation.hideTime)
        }

        NumberAnimation {
            to: 0
            duration: animation.hideTime
        }
    }

    function show(text, msleep = 2500) {
        if(!animation.running){
            lab.text = text;
            root.width = lab.contentWidth + 50
            animation.msleep = msleep;
            animation.start();
        }
    }
}
