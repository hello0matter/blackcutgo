import QtQuick 2.9

Rectangle{
    id: toast

    property real time: defaultTime
    readonly property real defaultTime: 3000
    readonly property real fadeTime: 300

    property real margin: 10
    property bool selfDestroying: false

    width: 98
    height: 98
    radius: 4
    opacity: 0
    color: "#000000"

    anchors.horizontalCenter: parent.horizontalCenter

    function show(text, duration){
        theText.text = text;
        if(typeof duration !== "undefined"){
            if(duration >= 2*fadeTime)
                time = duration;
            else
                time = 2*fadeTime;
        }
        else
            time = defaultTime;
        anim.start();
    }

    Image {
        id: imgHeader
        anchors.top: parent.top
        anchors.topMargin: 13
        anchors.horizontalCenter: parent.horizontalCenter
        sourceSize.width: 50
        sourceSize.height: 50
        source: ":/obj/toast.svg"
    }


    Text{
        id: theText
        text: ""
        horizontalAlignment: Text.AlignHCenter
        x: 28
        y: 68
        font.pixelSize: 14
        color: "#ffffff"
    }

    SequentialAnimation on opacity {
        id: anim

        running: false

        NumberAnimation{
            to: 0.9
            duration: fadeTime
        }
        PauseAnimation{
            duration: time - 2*fadeTime
        }
        NumberAnimation{
            to: 0
            duration: fadeTime
        }

        onRunningChanged:{
            if(!running && selfDestroying)
                toast.destroy();
        }
    }
}
