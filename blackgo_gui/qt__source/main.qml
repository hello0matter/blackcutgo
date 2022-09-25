import QtQuick
import QtQuick.Window
import QtQuick.Controls 6.3
import QtQuick.Layouts 1.0
import QtQuick.Controls.Material 6.3

Window {
    id: window
    width: 400
    height: 300
    visible: true
    title: qsTr("Hello World")
    Material.theme: Material.Light
    Material.accent: Material.Purple

    property var check: textInput1.text && textInput2.text ? true:false
    signal main__login(string usercode,string password,string city)

    GridLayout {
        anchors.verticalCenterOffset: 1
        anchors.horizontalCenterOffset: 0
        anchors.centerIn: parent
        focus: true
        rows: 4
        columns: 3
        columnSpacing :20
        rowSpacing : 20
        Label {
            id: label1
            text: qsTr("地区：")
            Layout.preferredHeight: 25
            Layout.preferredWidth: 53
        }

        ComboBox {
            id: comboBox
            Layout.columnSpan: 2
            Layout.preferredHeight: 35
            Layout.preferredWidth: 205
            textRole: "key"
            model: ListModel {
                ListElement { key: "杭州"; value: 0571 }
                ListElement { key: "宁波"; value: 0574 }
                ListElement { key: "温州"; value: 0577 }
                ListElement { key: "嘉兴"; value: 0573 }
                ListElement { key: "湖州"; value: 0572 }
                ListElement { key: "绍兴"; value: 0575 }
                ListElement { key: "金华"; value: 0579 }
                ListElement { key: "嵊州"; value: 0570 }
                ListElement { key: "舟山"; value: 0580 }
                ListElement { key: "台州"; value: 0576 }
                ListElement { key: "丽水"; value: 0578 }
            }
        }

        Label {
            id: label
            text: qsTr("账号：")
            Layout.preferredHeight: 25
            Layout.preferredWidth: 53
        }

        Rectangle {
            Layout.columnSpan: 2
            Layout.preferredHeight: 24
            Layout.preferredWidth: 199
            color: "#e5e2f3"
            border.color: "grey"

            TextInput {
                id: textInput1
                text: ""
                font.pixelSize: 12
                anchors.leftMargin: 3
                anchors.fill: parent
                font.pointSize: 15
                focus: true

            }
        }
        Label {
            id: label2
            text: qsTr("密码：")
            Layout.preferredHeight: 25
            Layout.preferredWidth: 53
        }


        Rectangle {
            Layout.columnSpan: 2
            Layout.preferredHeight: 24
            Layout.preferredWidth: 199
            color: "#e5e2f3"
            border.color: "grey"
            TextInput {
                id: textInput2
                text: ""
                font.pixelSize: 12
                anchors.leftMargin: 3
                anchors.fill: parent
                font.pointSize: 15
            }
        }
        Item {
            id: spacer
            Layout.preferredHeight: 14
            Layout.preferredWidth: 14
        }

        Button {
            id: login
            text: qsTr("登录")
            Layout.preferredHeight: 38
            Layout.preferredWidth: 89
            enabled: window.check
            onClicked: {
                console.log(main__login(textInput1.text,textInput2.text,comboBox.currentText))
                console.log("login")
            }
        }

        Item {
            id: spacer1
            Layout.preferredHeight: 14
            Layout.preferredWidth: 14
        }
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:1.25}
}
##^##*/
