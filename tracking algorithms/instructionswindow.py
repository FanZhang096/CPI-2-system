# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instructionswindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1231, 754)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(60, 30, 1121, 711))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:11.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:12pt; font-weight:600;\">Co-axial Tele-guidance System Instructions</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt; font-weight:600;\">Calibration</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">Calibration module is designed for engineers to calibrate projected annotations </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">1.</span><span style=\" font-family:\'Times New Roman\'; font-size:7pt;\">      </span><span style=\" font-size:11pt;\">Type number in the “Thickness” box to adjust the thickness of annotations. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">2.</span><span style=\" font-family:\'Times New Roman\'; font-size:7pt;\">      </span><span style=\" font-size:11pt;\">Type number in the “Width”, “Height”, “Y axis”, “X axis” to adjust the width, height, </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">location on the X and Y axis respectively. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">3.</span><span style=\" font-family:\'Times New Roman\'; font-size:7pt;\">      </span><span style=\" font-size:11pt;\">Click on the “save” button to save parameters after adjustment. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt; font-weight:600;\">Strategy 1: Real-time Guidance</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">This strategy allows trainers to implement real-time on-site and remote annotations. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">1. Click on the “Start” button to begin real-time guidance. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">2. Click on and drag the left mouse button to make screen annotations which will be orthotopicallly projected on the tissue. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">3. Click on the “Clear” button to clear screen annotations. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt; font-weight:600;\">Strategy 2: Vedio Guidance</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">In this category, users can record a video of the operation of a specialist, and then record verbal guidance and annotations according to the video. As a result, a video with verbal guidance and annotations will be synthesized. Finally, trainees can be trained with an audible video on the monitor and annotations on the model. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">1. Click on the “Delete” button to clear previous images. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">2. Click on the “Start” button to stat to record operation of trainer. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">3. Click on the “Stop” button to stop recording. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">4. Before annotation recording, click on another “Delete” button to clear previous annotations. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">5. Click on the “Start” button to start or continue to record screen annotations and verbal guidance. Video will stop at the last image. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">6. Click on the “Clear” button anytime you want to clear the screen annotations </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">7. Close the window and restart again after image indexing. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">8. Restart the window and click on the “Start” button to start video guidance. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%;\"><span style=\" font-size:11pt;\">9    .Click on the “Stop” button anytime you want the annotations to stay. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">  </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Note</span><span style=\" font-size:11pt;\">: Camera parameters can be adjusted with the MindVision Software. </span></p></body></html>"))
