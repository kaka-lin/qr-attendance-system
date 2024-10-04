import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "pages"

Page {
    id: root
    width: parent.width
    height: parent.height

    signal tabActivated(bool isActivated)
    onTabActivated: {
        //console.log('tab activated: ' + isActivated);

        if (isActivated) {
            if (view.currentIndex == 0) {
                bmsDataPage.pageActivated(true);
            } else {
                bmsDataPage.pageActivated(false);
            }
        } else {
            bmsDataPage.pageActivated(false);
        }
    }

    header: TabBar {
        id: bar
        width: parent.width
        currentIndex: view.currentIndex
    }

    SwipeView {
        id: view
        anchors.fill: parent
        currentIndex: bar.currentIndex
    }
}
