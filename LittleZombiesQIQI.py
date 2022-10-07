import sys, os, json
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem, \
    QAbstractItemView, QMenu
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTableWidget, QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from myfuntions import *
import time
import pyttsx3

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()

        #为了获取输入框的内容,采用个中间人
        self.url_text = None
        self.pass_text = None
        #窗体标题和尺寸
        self.setWindowTitle("小僵尸七七")

        #窗体的尺寸
        self.resize(1507, 819)

        #窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        #设置背景
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
        QtGui.QBrush(QtGui.QPixmap("./image/小姐姐.jpg")))
        self.setPalette(window_pale)

        #布局
        #创建一个垂直方向的布局
        layout = QVBoxLayout()
        # 将菜单布局添加到整个界面的布局中
        layout.addLayout(self.init_menu())
        # 将标题布局添加到整个界面的布局中
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_table())
        # 将菜单布局添加到整个界面的布局中
        layout.addLayout(self.init_footer())

        # 给窗体设置元素的排列方式
        self.setLayout(layout)

#创建顶部菜单布局
    def init_menu(self):
        menu_layout = QHBoxLayout()
        #创建两个按钮,加入到横向区域
        bt_start = QPushButton("七七")
        menu_layout.addWidget(bt_start)
        bt_stop = QPushButton("可莉")
        menu_layout.addWidget(bt_stop)
        bt_stop = QPushButton("迪奥娜")
        menu_layout.addWidget(bt_stop)
        bt_stop = QPushButton("早柚")
        menu_layout.addWidget(bt_stop)
        bt_stop = QPushButton("纳西妲")
        menu_layout.addWidget(bt_stop)
        bt_stop = QPushButton("多莉")
        menu_layout.addWidget(bt_stop)
        bt_stop = QPushButton("瑶瑶")
        menu_layout.addWidget(bt_stop)
        #在右侧添加个弹簧,把两个按钮弹到左边
        menu_layout.addStretch()
        return menu_layout

#创建上面标题布局
    def init_header(self):
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        #添加url输入框
        url_text = QLineEdit()
        # 先获取输入框的内容
        url_text.text()
        #输入框添加默认文字
        url_text.setPlaceholderText("七七超级棒")
        #将url_text的值赋值给self.url_text,方便其他函数内使用
        self.url_text = url_text

        header_layout.addWidget(url_text)

        # 添加参数输入框
        pass_text = QLineEdit()
        # 设置输入框的长度
        pass_text.setFixedWidth(150)
        # 获取输入框的内容
        pass_text.text()
        # 输入框添加默认文字
        pass_text.setPlaceholderText("神秘代码")

        #将pass_text的值赋值给self.pass_text,方便其他函数内使用
        self.pass_text = pass_text
        header_layout.addWidget(pass_text)

        #添加按钮
        bt_add = QPushButton("测试连接")
        #绑定事件
        bt_add.clicked.connect(self.event_add_click)
        header_layout.addWidget(bt_add)

        return header_layout

#创建中间布局
    def init_table(self):
        try:
            table_layout = QHBoxLayout()

            # 初始化表格数据
            # 读取数据文件
            file_path = os.path.join(BASE_DIR, "db", "data.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            data_list = json.loads(data)

            # 创建表格
            # 默认显示几行几列
            self.table_widget = table_widget = QTableWidget(0, 8)

            #开始添加数据了
            current_row_count = table_widget.rowCount() #获取当前表格有多少行
            for row_list in data_list:
                table_widget.insertRow(current_row_count) #一行一行添加数据
                #写数据
                for i, ele in enumerate(row_list):
                    cell = QTableWidgetItem(str(ele))
                    # 文本居中显示
                    cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    #设置除了备注栏之外其余的都不可修改, 备注索引是5
                    if i != 5:
                        cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                    table_widget.setItem(current_row_count, i, cell)
                current_row_count += 1


            #设置横向标题, 第二个参数得是个QTableWidgeItem对象
            #创建item对象,设置好文字再添加到表格中
            #循环遍历下
            table_header = [
                {"text": "URL", 'width': 322},
                {"text": "IP", 'width': 228},
                {"text": "参数", 'width': 91},
                {"text": "脚本类型", 'width': 91},
                {"text": "OS类型", 'width': 182},
                {"text": "备注", 'width': 182},
                {"text": "添加时间", 'width': 182},
                {"text": "状态", 'width': 182},
            ]
            for idx,info in enumerate(table_header):
                item = QTableWidgetItem()
                item.setText(info['text'])
                #文本居中显示
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table_widget.setHorizontalHeaderItem(idx, item)

                #设置标题索引对应的宽度
                table_widget.setColumnWidth(idx,info['width'])

            #设置表格颜色交替
            table_widget.setAlternatingRowColors(True)
            #设置表格为整行选择
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

            #开启右键设置
            table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            table_widget.customContextMenuRequested.connect(self.right_menu)

            #表格添加到布局中
            table_layout.addWidget(table_widget)
            return table_layout
        except Exception as e:
            pass

#底部菜单
    def init_footer(self):
        footer_layout = QHBoxLayout()
        #添加Label
        self.label_status = label_status = QLabel("七七太棒了", self)
        footer_layout.addWidget(label_status)
        #添加个弹簧
        footer_layout.addStretch()

        #添加按钮
        btn_del = QPushButton("删除")
        btn_del.clicked.connect(self.event_delete_click)
        footer_layout.addWidget(btn_del)
        # 添加个杀软检测功能
        btn_av = QPushButton("AV查看")
        btn_av.clicked.connect(self.event_av_click)
        footer_layout.addWidget(btn_av)

        btn_proxy = QPushButton("代理设置")
        btn_proxy.clicked.connect(self.event_proxy_click)
        footer_layout.addWidget(btn_proxy)

        # btn_save = QPushButton("保存")
        # btn_save.clicked.connect(self.event_save_click)
        # footer_layout.addWidget(btn_save)

        btn_help = QPushButton("帮助")
        btn_help.clicked.connect(self.event_help_click)
        footer_layout.addWidget(btn_help)


        return footer_layout

#添加功能
    def event_add_click(self):
        try:
            #1.获取输入框中的内容
            url = self.url_text.text()
            passwd = self.pass_text.text()
            #判断输入框是否有内容
            if not url or not passwd:
                # pyttsx3.speak("请输入完整的url和神秘代码")
                pass

            #2.发送请求获取数据,注意点:如果是爬虫的话不能在主线程中做这个事,要不然桌面的其他功能都不能用
            #这个时候应该创建一个线程,让线程去做爬虫,暂时不加,等学精了再说
            test_statue = test_conn(url, passwd)
            if test_statue == "NO":
                pyttsx3.speak("密码错误")
            elif test_statue == "FALSE":
                pyttsx3.speak("url路径错误")
            else:
                pyttsx3.speak("连接成功")
                script_size = str(url).rsplit(".")[-1]
                # 把列表的内容添加到表格中
                ip = test_statue[0]
                os_size = test_statue[1]
                new_row_list = [url, ip, passwd, script_size, os_size, "", time.strftime("%Y-%m-%d"), "七七超级可爱"]

                #准备往表格里添加数据,先获取当前行数
                current_row_count = self.table_widget.rowCount() #获取当前表格有多少行
                #插入一行
                self.table_widget.insertRow(current_row_count)
                for i, ele in enumerate(new_row_list):
                    cell = QTableWidgetItem(str(ele))
                    # 文本居中显示
                    cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    # 设置除了备注栏之外其余的都不可修改, 备注索引是5
                    if i != 5:
                        cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table_widget.setItem(current_row_count, i, cell)
                self.event_save_click()
        except Exception as e:
            print(e)

#删除功能
    def event_delete_click(self):
        #获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            pass
        else:
            # 反转一下,防止删除时索引一直变
            row_list.reverse()
            for row_object in row_list:
                index = row_object.row()
                self.table_widget.removeRow(index)
        self.event_save_click()

#右键功能
    def right_menu(self, pos):
        # 获取当前选中行,只有选中行才支持右键
        select_row_list = self.table_widget.selectionModel().selectedRows()
        if len(select_row_list) == 1:
            menu = QMenu()
            item_copy = menu.addAction("复制url")
            item_file = menu.addAction("文件管理")
            item_cmd = menu.addAction("虚拟终端")
            item_wifi = menu.addAction("WIFI密码收集")


            #action表示选中了哪个
            action = menu.exec_(self.table_widget.mapToGlobal(pos))
            if action == item_copy:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.table_widget.selectedItems()[0].text())
            elif action == item_file:
                self.event_file_click()
            elif action == item_cmd:
                self.event_cmd_click()
            elif action == item_wifi:
                self.event_wifi_click()
            else:
                pass
            #获取到选中行的url和参数,然后传递给下一个程序

#文件管理
    def event_file_click(self):
        try:
            from utils.dialog import FileMag
            dialog_cmd = FileMag()
            dialog_cmd.setWindowModality(Qt.ApplicationModal)

            # 先看下有没有选中行,如果有的话直接检测选中的url,如果没有再执行下一个
            # 获取已经选中的行
            row_list = self.table_widget.selectionModel().selectedRows()
            # 如果只选中一行的话执行自动检测
            if len(row_list) == 1:
                # 接下来就应该获取行内url和password了
                url = self.table_widget.selectedItems()[0].text()
                pwd = self.table_widget.selectedItems()[2].text()
                try:
                    # 将实例化的对象传过去,然后后面的__init__中先把需要的变量定义好
                    FileMag.url_pwd(dialog_cmd, url, pwd)

                except Exception as  e:
                    print(e)

            dialog_cmd.exec_()
        except Exception as e:
            print(e)

#虚拟终端界面
    def event_cmd_click(self):
        # 调用自己弄的弹窗函数
        try:
            from utils.dialog import AlertDialogCmd
            dialog_cmd = AlertDialogCmd()
            dialog_cmd.setWindowModality(Qt.ApplicationModal)

            # 先看下有没有选中行,如果有的话直接检测选中的url,如果没有再执行下一个
            # 获取已经选中的行
            row_list = self.table_widget.selectionModel().selectedRows()
            # 如果只选中一行的话执行自动检测
            if len(row_list) == 1:
                # 接下来就应该获取行内url和password了
                url = self.table_widget.selectedItems()[0].text()
                pwd = self.table_widget.selectedItems()[2].text()
                try:
                    # 将实例化的对象传过去,然后后面的__init__中先把需要的变量定义好
                    AlertDialogCmd.url_pwd(dialog_cmd, url, pwd)

                except Exception as  e:
                    print(e)

            dialog_cmd.exec_()
        except Exception as e:
            print(e)

#杀软查看功能
    def event_av_click(self):
        #创建弹窗,并在弹窗中设置
        #调用自己弄的弹窗函数
        from utils.dialog import AlertDialog
        dialog = AlertDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        #先看下有没有选中行,如果有的话直接检测选中的url,如果没有再执行下一个
        # 获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        #如果只选中一行的话执行自动检测
        if len(row_list) == 1:
            #接下来就应该获取行内url和password了
            url = self.table_widget.selectedItems()[0].text()
            passwd = self.table_widget.selectedItems()[2].text()
            # print(url, passwd)
            #选择完之后开始执行命令,此时直接发送请求,并获取到响应包内容,然后将结果传递给下一个检测的那个,显示到列表上
            task_res = cmd_conn(url, passwd, r'system("tasklist /SVC");')
            task_res = str(task_res)
            # 获取到回显后,如何传递给另一个页面呢?
            try:
                #将实例化的对象传过去,然后后面的__init__中先把需要的变量定义好
                AlertDialog.check_func(dialog, task_res)
            except Exception as  e:
                print(e)
        #如果没选或者选中多行的话就不执行自动检测操作,先就这么写,等之后想到啥骚操作再补
        else:
            pass
        dialog.exec_()

#wifi密码查看
    def event_wifi_click(self):
        #创建弹窗,并在弹窗中设置
        #调用自己弄的弹窗函数
        from utils.dialog import WifiDialog
        dialog = WifiDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        #先看下有没有选中行,如果有的话直接检测选中的url,如果没有再执行下一个
        # 获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        #如果只选中一行的话执行自动检测
        if len(row_list) == 1:
            #接下来就应该获取行内url和password了
            url = self.table_widget.selectedItems()[0].text()
            passwd = self.table_widget.selectedItems()[2].text()
            try:
                #将实例化的对象传过去,然后后面的__init__中先把需要的变量定义好
                WifiDialog.get_url(dialog, url, passwd)
            except Exception as  e:
                print(e)
        #如果没选或者选中多行的话就不执行自动检测操作,先就这么写,等之后想到啥骚操作再补
        else:
            pass
        dialog.exec_()

#定义一个保存数据功能
    def event_save_click(self):
        db_list = []
        str_list = []        #获取当前行数
        current_row_count = self.table_widget.rowCount()  # 获取当前表格有多少行
        current_cols_count = self.table_widget.columnCount()  # 获取当前表格有多少列
        #遍历行内容,遍历行的个数就行
        for row_index in range(current_row_count):
            for cols_index in range(current_cols_count):
                #获取到每个单元格的内容了,先添加到内部列表中
                str_list.append(self.table_widget.item(row_index, cols_index).text())
                #内部列表添加到总列表中
            db_list.append(str_list)
                #然后再讲str_list内容清空
            str_list = []
        # print(db_list)
        # [['http://127.0.0.1/zijide.php', '192.168.1.94', 'qiqi', 'php', 'NT', '测试', '2022-09-25', '未知']]
        #该往数据文件中写了
        try:
            with open("./db/data.json", mode="w", encoding="utf-8") as f:
                json.dump(db_list, f, indent=2, separators=(',', ':'), ensure_ascii=False)
        except Exception as e:
            print(e)


#添加代理设置功能
    def event_proxy_click(self):
        from utils.dialog import ProxyDialog
        proxy_dialog = ProxyDialog()
        proxy_dialog.setWindowModality(Qt.ApplicationModal)
        proxy_dialog.exec_()
        pass

# #弹窗功能
#     def messageDialog(self):
#         msg_box = QMessageBox(QMessageBox.Information, "小僵尸", "保存成功")
#         msg_box.setWindowIcon(QtGui.QIcon("image/1.ico"))
#         msg_box.exec_()

#帮助
    def event_help_click(self):
        pyttsx3.speak("没学过这个,一点一点网上搜着写的,出了问题自己解决,本人爱莫能助")

if __name__ == '__main__':
    #读取代理设置,已经写好了,这个是直接设置
    proxy_size = set_proxy()
    if proxy_size != "不使用代理":
        pyttsx3.speak(f"当前使用了{proxy_size}")

    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())