import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.3
import Qt.labs.settings 1.1

Window {
    id: window
    width: 400
    height: 300
    visible: true
    property alias busyIndicatorClip: busyIndicator.clip
    title: qsTr("Hello World")
    Material.theme: Material.Light
    Material.accent: Material.Purple

    property bool isUpdating: false
    property string loginData
    property string inputcars

    signal main__login(string usercode,string password,string city)

     signal open1()
     signal open2()
     signal inputcar(string code)
    onLoginDataChanged: {

        if(loginData){
            stackView.push(playComponent)
        }else{
            toast.show("登录失效")
            stackView.push(loginComponent)
        }
    }

    Component.onCompleted: {
        console.log("token",settings.value("loginData"))
        if(settings.value("loginData")){
            window.loginData = settings.value("loginData")
        }
        if(settings.value("loginData")){
            stackView.push(playComponent)
        }else{

            stackView.push(loginComponent)
        }


    }

    Settings{
        id: settings
        fileName: "config.ini"
    }
    StackView {
        id: stackView
        anchors.fill: parent

        Component{
            id:loginComponent
            Rectangle{
                id:loginRectangle
                anchors.fill: parent
                property bool check: textInput1.text && textInput2.text ? true:false
                GridLayout {
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
                            ListElement { key: "杭州"; value: "0571" }
                            ListElement { key: "宁波"; value: "0574" }
                            ListElement { key: "温州"; value: "0577" }
                            ListElement { key: "嘉兴"; value: "0573" }
                            ListElement { key: "湖州"; value: "0572" }
                            ListElement { key: "绍兴"; value: "0575" }
                            ListElement { key: "金华"; value: "0579" }
                            ListElement { key: "嵊州"; value: "0570" }
                            ListElement { key: "舟山"; value: "0580" }
                            ListElement { key: "台州"; value: "0576" }
                            ListElement { key: "丽水"; value: "0578" }
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
                        enabled: loginRectangle.check
                        onClicked: {
                            window.isUpdating = true
                            main__login(textInput1.text,textInput2.text,comboBox.model.get(comboBox.currentIndex).value)
                        }
                    }

                    Item {
                        id: spacer1
                        Layout.preferredHeight: 14
                        Layout.preferredWidth: 14
                    }


                }
            }
        }

        Component{
            id:playComponent

            Rectangle{
                id:playRectangle
                Button {
                    id: button44
                    x: 60
                    y: 122
                    width: 146
                    height: 61
                    text: qsTr("确认车码")
                    onClicked: {
                        inputcar(inputt.text)
                    }
                }
                Rectangle {

                    x: 20
                    y: 222
                    width: 200
                    height: 31
                    color: "#e5e2f3"
                    border.color: "grey"
                    TextInput {
                        id: inputt
                        text: window.inputcars
                        anchors.fill: parent
                        font.pointSize: 12
                    }
                }
                Button {
                    id: button33
                    x: 60
                    y: 22
                    enabled:false
                    width: 146
                    height: 61
                    text: qsTr("选择车码txt")
                    onClicked: {
//                        open1()
                    }
                }
                Button {
                    id: button11
                    x: 241
                    y: 22
                    width: 146
                    height: 61
                    text: qsTr("选择输入文件夹")
                    onClicked: {
                        open1()
                    }
                }

                Button {
                    id: button22
                    x: 241
                    y: 122
                    width: 146
                    height: 61
                    text: qsTr("选择输出文件夹")
                    onClicked: {
                          open2()
                    }
                }

                Button {
                    id: button23
                    x: 241
                    y: 222
                    width: 146
                    height: 61
                    text: qsTr("登出账号")
                    onClicked: {
                        settings.setValue("loginData","")
                        window.loginData=""
                    }
                }

            }
        }

    }
    BusyIndicator {
        id: busyIndicator
        running: window.isUpdating
        anchors{
            horizontalCenter: parent.horizontalCenter
            verticalCenter:  parent.verticalCenter
        }
    }
    Toast{ id: toast }

}




