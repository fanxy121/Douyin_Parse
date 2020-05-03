#-*-coding:utf-8-*-
from PyQt5.QtWidgets import QWidget,QPushButton,QMessageBox
from PyQt5.QtGui import QIcon, QMouseEvent,QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.Qt import QUrl, QVideoWidget,Qt
from Douyin_UI import Ui_Form
from PyQt5 import QtCore
from Spider import ParseData
import qtawesome,requests,time

class MainLogic(QWidget,Ui_Form,ParseData):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowIcon(QIcon("source/logo1.png"))
        self.setupUi(self)
        self.widget_style()
        self.setCursor(Qt.ArrowCursor)

    def setVideo(self,url):
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.playSlide) #进度条
        self.play_sld.sliderMoved.connect(self.changeSlide) #进度条
        self.video_widget = QVideoWidget(self.video_box)
        self.video_widget.setGeometry(0,0,100,100)
        self.video_widget.setAspectRatioMode(1)
        self.video_widget.show()
        self.verticalLayout_4.addWidget(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl(url)))

        self.player.setVolume(50) #设置声音大小
        self.player.setVideoOutput(self.video_widget)
        self.player.pause()

    def parse_video(self):
        try:
            self.parse_url(self.parse_le.text())
            self.get_data()
            self.setVideo(self.play_addr)
            self.insertData()
            self.clear_btn.setEnabled(True)
            self.play_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.parse_btn.setEnabled(False)
        except:
            QMessageBox.critical(self, "解析失败", "请检查当前网络链接\n或者检查分享链接是否输入正确")

    def widget_style(self):
        self.min_btn = QPushButton(qtawesome.icon('fa.window-minimize', color='#ddd'), "",self.widget_3)
        self.min_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.min_btn.setStyleSheet("margin: 12px;padding: 2px 0;background:#b99910;border-radius:5px;")
        self.min_btn.setText("")
        self.min_btn.setAutoRepeatDelay(300)
        self.min_btn.setObjectName("min_btn")
        self.horizontalLayout.addWidget(self.min_btn)

        self.close_btn = QPushButton(qtawesome.icon('fa.window-close', color='#ddd'),'',self.widget_3)
        self.close_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.close_btn.setStyleSheet("margin: 12px;padding: 2px 0;background:#bf3b3b;border-radius:5px;")
        self.close_btn.setText("")
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)
        self.parse_btn_2.setIcon(QIcon('source/parse.ico'))

        self.introduce_label.setAlignment(Qt.AlignTop)
        self.desc_label.setAlignment(Qt.AlignTop)

    def clear_data(self):
        self.clear_btn.setEnabled(False)
        self.play_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.parse_btn.setEnabled(True)
        self.player.deleteLater()
        self.video_widget.deleteLater()

        self.avatar_label.clear()
        self.author_name_label.clear()
        self.douyin_id_label.clear()
        self.introduce_label.clear()
        self.desc_label.clear()
        self.create_time_label.clear()
        self.video_size_label.clear()

        self.play_btn.setText('播放')
        self.play_sld.setValue(0)
        self.video_time.setText("00:00/00:00")
    def insertData(self):
        avatar = requests.get(self.author_avatar_addr,headers = self.headers).content
        img = QPixmap()
        img.loadFromData(avatar)
        self.avatar_label.setPixmap(img)
        self.avatar_label.setScaledContents(True)
        self.response = requests.get(self.play_addr, headers=self.headers)
        self.video_size = str(format(int(self.response.headers['Content-Length']) / 1048576, ".2f") + " Mb")
        self.author_name_label.setText(self.author_nickname)
        self.douyin_id_label.setText(self.author_unique_id)
        self.introduce_label.setText(self.author_signature)
        self.desc_label.setText(self.douyin_desc)
        self.video_size_label.setText(self.video_size)
        self.create_time_label.setText(str(self.douyin_create_time))
    def playSlide(self,position):
        self.vidoeLength = self.player.duration() + 0.01
        videoLength = divmod(round(position / 1000), 60)
        self.video_time.setText(f'{str("%02d:%02d" % (videoLength[0],videoLength[1]))}/{self.video_duration}')
        self.play_sld.setValue(round((position/self.vidoeLength)*100))
        if self.vidoeLength > 0.01 and round(position) == round(self.vidoeLength): #判断是否播放结束
            self.play_btn.setText('播放')
            self.play_sld.setValue(0)
    def changeSlide(self):
        self.play_position = round(self.play_sld.value()/100 * self.v_length)
        self.player.setPosition(self.play_position)
    def play(self):
        if self.play_btn.text() == '播放' and self.vidoeLength > 0.01:
            self.play_btn.setText('暂停')
            self.player.play()
        else:
            self.play_btn.setText('播放')
            self.player.pause()

    def download(self):
        fw = open(self.desc_label.text() + '.mp4', "wb")
        chunk_size = 1048576
        r = requests.get(self.play_addr, headers=self.headers, stream=True)
        filesize = self.response.headers['Content-Length']
        if filesize is None:
            fw.write(r.content)
        else:
            dl = 0
            total_length = int(filesize)
            t1 = time.time()
            for data in r.iter_content(chunk_size):
                dl += len(data)
                show = dl / total_length
                fw.write(data)
                t2 = time.time()
                t = t2 - t1
                speed = dl / 1024 / 1024 / t
                self.progressBar.setValue(show * 100)
                self.download_speed_label.setText(f'{str(speed)[0:4]}M/s')

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except:
            pass
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

#  我在抖音选演员系列 ——袁冰妍 饰 王初冬  #雪中悍刀行  #60帧 https://v.douyin.com/w5CAH2/ 复制此链接，打开【抖音短视频】，直接观看视频！
#  一直想做一期王者的语音台词，费了很多精力做了一期，可还行？ https://v.douyin.com/wVoGuG/ 复制此链接，打开【抖音短视频】，直接观看视频！
#  古风#60帧#送你一张动态壁纸！十年情思百年渡，不斩相思不忍顾 @抖音小助手 https://v.douyin.com/wQrjcy/ 复制此链接，打开【抖音短视频】，直接观看视频！
#这...是反派？？？ #焰灵姬  #60帧 https://v.douyin.com/wWAxXV/ 复制此链接，打开【抖音短视频】，直接观看视频！
#天行九歌 #韩非与嬴政对话 十年可见春去秋来，百年可见生老病死，千年可证王朝更替，万年可见斗转星移 https://v.douyin.com/wW581S/ 复制此链接，打开【抖音短视频】，直接观看视频！
# proxies = {'http':'39.137.69.7'},

