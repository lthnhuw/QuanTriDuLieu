import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import subprocess
import mysql.connector

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Đặt tiêu đề cửa sổ và kích thước cố định
        self.setWindowTitle("Đăng nhập thư viện")
        self.setFixedSize(500, 400)

        # Thiết màu hình nền
        self.setStyleSheet("background-color: rgb(255,255,255);") 

        
        self.lib_frame = QWidget(self)
        self.lib_frame.setGeometry(100, 75, 300, 250)

        # Tiêu đề của form đăng nhập
        self.title_label = QLabel("ĐĂNG NHẬP", self.lib_frame)
        self.title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: rgb(33,113,53); background-color: rgba(255,255,255, 0); ")
        
        # Dòng chào mừng
        self.instruction_label = QLabel("Chào mừng bạn đến với Thư viện", self.lib_frame)
        self.instruction_label.setFont(QFont("Arial", 10))
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("color: rgb(33,113,53); background-color: rgba(255,255,255, 0);")
        
        # Trường nhập tên đăng nhập
        self.username_input = QLineEdit(self.lib_frame)
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFixedHeight(30)
        self.username_input.setStyleSheet("""
            padding-left: 10px;
            background-color: rgba(255, 255, 255, 0.5);
            color: rgb(33,113,53);
            border: 0.5px solid rgb(33,113,53);
            border-radius: 5px;
        """)
        
        # Icon cho tên đăng nhập
        self.username_icon = QLabel(self.lib_frame)
        self.username_icon.setPixmap(QPixmap("images/user.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.username_icon.setStyleSheet("margin-left: 5px; background-color: rgba(255,255,255, 0.7);")

        # Trường nhập mật khẩu
        self.password_input = QLineEdit(self.lib_frame)
        self.password_input.setPlaceholderText("Mật Khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(30)
        self.password_input.setStyleSheet("""
            padding-left: 10px;
            background-color: rgba(255, 255, 255, 0.5);
            color: rgb(33,113,53);
            border: 0.5px solid rgb(33,113,53);
            border-radius: 5px;
        """)

        # Icon cho mật khẩu
        self.password_icon = QLabel(self.lib_frame)
        self.password_icon.setPixmap(QPixmap("images/pass.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.password_icon.setStyleSheet("margin-left: 5px; background-color: rgba(255,255,255, 0.7);")

        # Nút đăng nhập
        self.login_button = QPushButton("Đăng nhập", self.lib_frame)
        self.login_button.setFixedHeight(25)
        self.login_button.setFixedWidth(70)
        self.login_button.setStyleSheet("""
            background-color: rgba(242, 115, 124, 1);
            color: white;
            border-radius: 5px;
            font-weight: bold;
        """)

        # Nhãn "Quên mật khẩu"
        self.forgot_password_label = QLabel("Quên mật khẩu?", self.lib_frame)
        self.forgot_password_label.setStyleSheet("color: rgb(33,113,53); background-color: rgba(255,255,255, 0);")

        # Kết nối nút với hàm login
        self.login_button.clicked.connect(self.login)

        # Nhãn đăng ký
        self.register_label = QLabel("Đăng ký", self.lib_frame)
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_label.setStyleSheet("color: rgb(33,113,53); background-color: rgba(255,255,255, 0); text-decoration: underline;")

        # Kết nối nhãn với hàm mở form đăng ký
        self.register_label.mousePressEvent = self.open_register_form

        # Tạo bố cục cho các trường nhập liệu
        lib_layout = QVBoxLayout()
        lib_layout.addWidget(self.title_label)
        lib_layout.addWidget(self.instruction_label)
        
        # Bố cục cho tên đăng nhập với icon
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_icon)
        username_layout.addWidget(self.username_input)
        lib_layout.addLayout(username_layout)

        # Bố cục cho mật khẩu với icon
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_icon)
        password_layout.addWidget(self.password_input)
        lib_layout.addLayout(password_layout)

        # Nút đăng nhập
        lib_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bố cục cho "Quên mật khẩu"
        options_layout = QHBoxLayout()
        options_layout.addStretch()
        lib_layout.addWidget(self.forgot_password_label, alignment=Qt.AlignmentFlag.AlignCenter)
        lib_layout.addLayout(options_layout)

        # Nhãn đăng ký
        lib_layout.addWidget(self.register_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lib_frame.setLayout(lib_layout)

    def login(self):
        # Lấy tên đăng nhập và mật khẩu từ các trường nhập
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Kiểm tra đăng nhập từ cơ sở dữ liệu MySQL
        user = self.check_credentials(username, password)
        
    def login(self):
        # Lấy tên đăng nhập và mật khẩu từ các trường nhập
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Kiểm tra đăng nhập từ cơ sở dữ liệu MySQL
        user = self.check_credentials(username, password)
        
        if user:
            QMessageBox.information(self, "Success", "Đăng nhập thành công!") 
            try:
                subprocess.Popen(["python", "admin_interface.py"])  
                self.close()  
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Không thể mở giao diện admin: {e}")
        else:
            QMessageBox.critical(self, "Error", "Tên đăng nhập hoặc mật khẩu không đúng")

    def check_credentials(self, username, password):
        db = connect_to_db()
        if db:
            cursor = db.cursor()
            query = "SELECT * FROM tai_khoan WHERE tenTaiKhoan = %s AND matKhau = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()  # Lấy 1 dòng dữ liệu
            db.close()
            return user
        return None

    def open_register_form(self, event):
        # Mở form đăng ký từ register.py
        try:
            subprocess.Popen(["python", "register.py"])  
            self.close() 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể mở giao diện đăng ký: {e}")

def connect_to_db():
    try:
        db = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='07042003',  
            database='quanlithuvien'  
        )
        return db
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Lỗi kết nối", f"Không thể kết nối cơ sở dữ liệu: {err}")
        return None

# Chạy ứng dụng
app = QApplication(sys.argv)
form = LoginForm()
form.show()
sys.exit(app.exec())
