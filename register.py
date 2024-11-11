import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import subprocess

class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Đặt tiêu đề cửa sổ và kích thước cố định
        self.setWindowTitle("Đăng ký tài khoản thư viện")
        self.setFixedSize(500, 400) 

        

        # Thiết lập màu nền
        self.setStyleSheet("background-color: rgb(255,255,255);") 

        self.reg_frame = QWidget(self)
        self.reg_frame.setGeometry(100,50, 300, 300)  

        # Nút trở lại form đăng nhập
        self.back_button = QPushButton("← Trở lại", self)
        self.back_button.setGeometry(5, 5, 60, 25)
        self.back_button.setStyleSheet("""
            color: darkgreen;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.back_button.clicked.connect(self.open_login_form)

        # Form đăng ký
        self.title_label = QLabel("ĐĂNG KÝ", self.reg_frame)
        self.title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: rgb(33,113,53); background-color: rgba(210,210,210, 0);")

        # Tạo các trường nhập liệu với biểu tượng
        self.name_input = self.create_input_field("Tên", "images/user.png")
        self.email_input = self.create_input_field("Email", "images/email.png")
        self.address_input = self.create_input_field("Địa chỉ", "images/address.png")  
        self.password_input = self.create_input_field("Mật Khẩu", "images/pass1.png", is_password=True)
        self.confirm_password_input = self.create_input_field("Nhập lại mật khẩu", "images/pass.png", is_password=True)

        # Nút đăng ký
        self.register_button = QPushButton("Đăng ký", self.reg_frame)
        self.register_button.setFixedHeight(25)
        self.register_button.setFixedWidth(70)
        self.register_button.setStyleSheet("""
            background-color: rgba(242, 115, 124, 1);
            color: white;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.register_button.clicked.connect(self.register)

        # Tạo bố cục cho các trường nhập liệu
        reg_layout = QVBoxLayout()
        reg_layout.addWidget(self.title_label)
        reg_layout.addLayout(self.name_input)
        reg_layout.addLayout(self.email_input)
        reg_layout.addLayout(self.address_input) 
        reg_layout.addLayout(self.password_input)
        reg_layout.addLayout(self.confirm_password_input)
        reg_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.reg_frame.setLayout(reg_layout)

    def create_input_field(self, placeholder, icon_path, is_password=False):
        layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        icon_label.setFixedSize(25, 25)

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(30)
        input_field.setStyleSheet("""
            padding-left: 10px;
            background-color: rgba(255, 255, 255, 0.5);
            color: rgb(33,113,53);
            border: 0.5px solid rgb(33,113,53);
            border-radius: 5px;
        """)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(icon_label)
        layout.addWidget(input_field)
        return layout

    def register(self):
        # Lấy thông tin từ các trường nhập
        name = self.name_input.itemAt(1).widget().text()
        email = self.email_input.itemAt(1).widget().text()
        address = self.address_input.itemAt(1).widget().text()  
        password = self.password_input.itemAt(1).widget().text()
        confirm_password = self.confirm_password_input.itemAt(1).widget().text()

        # Kiểm tra tính hợp lệ của thông tin đăng ký
        if not name or not email or not address or not password or not confirm_password:
            QMessageBox.critical(self, "Error", "Vui lòng điền tất cả các trường.")
        elif password != confirm_password:
            QMessageBox.critical(self, "Error", "Mật khẩu không khớp.")
        else:
            QMessageBox.information(self, "Success", "Đăng ký thành công!")
            self.open_login_form()

    def open_login_form(self):
        try:
            subprocess.Popen(["python", "login.py"]) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể mở giao diện đăng nhập: {e}")

# Chạy ứng dụng
app = QApplication(sys.argv)
form = RegisterForm()
form.show()
sys.exit(app.exec())
