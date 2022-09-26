import QtQuick 2.9



Column{

    id: toastManager

    z: Infinity
    spacing: 5
    anchors.centerIn: parent

    property var toastComponent

    Component.onCompleted: toastComponent = Qt.createComponent(":/obj/Toast.qml")

    function show(text, duration) {
        var toast = toastComponent.createObject(toastComponent);
        toast.selfDestroying = true;
        toast.show(text, duration);
    }


}
