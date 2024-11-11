import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QStackedWidget, QSpacerItem, QSizePolicy, QMessageBox, QTableWidget, QTableWidgetItem,
                             QLineEdit, QDialog, QFormLayout)
from PyQt6.QtWidgets import QHeaderView

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize

import subprocess

import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lí thư viện")
        self.setFixedSize(1024, 600)

        # Tạo widget chính và layout chính
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Thanh điều hướng phía trên
        top_nav_widget = QWidget()
        top_nav_layout = QHBoxLayout()
        top_nav_widget.setLayout(top_nav_layout)
        top_nav_widget.setFixedHeight(40)
        top_nav_widget.setStyleSheet("background-color: rgba(255,255,255,0.7); color: white; border-radius: 5px; padding: 2px")

        admin_label = QLabel("Admin")
        admin_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        admin_label.setStyleSheet("background-color: rgba(0,0,0,0); color: darkgreen")

        top_nav_layout.addWidget(admin_label)

        # Thêm khoảng trống để đẩy nút đăng xuất sang bên phải
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        top_nav_layout.addItem(spacer)

        # Nút đăng xuất
        logout_button = QPushButton("Đăng xuất")
        logout_button.setFixedWidth(70)
        logout_button.setFixedHeight(25)
        logout_button.setStyleSheet("background-color: rgba(207, 6, 26,0.8); color: white; padding: 2px; border-radius: 5px")
        top_nav_layout.addWidget(logout_button)

        # Kết nối nút đăng xuất với hàm logout
        logout_button.clicked.connect(self.logout)

        # Thanh điều hướng bên trái
        nav_widget = QWidget()
        nav_layout = QVBoxLayout()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedWidth(170)
        nav_widget.setStyleSheet("background-color: rgba(255,255,255,0.7); color: white; border-radius: 5px")

        # StackedWidget để chứa các trang
        self.stacked_widget = QStackedWidget()

        # Thêm các trang vào stacked widget
        self.add_pages_to_stacked_widget()
        self.card_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        # Danh sách các mục điều hướng
        nav_items = [
            ("Nhân viên","images/nhanvien.png",0),
            ("Sách", "images/books.png", 1),
            ("Tác giả","images/tacgia.png",2),
            ("Nhà xuất bản","images/nxb.png",3),
            ("Đọc giả","images/reader.png",4),
            ("Thẻ thư viện", "images/the.png", 5),
            ("Mượn trả sách", "images/muontra.png", 6),
            ("Chi tiết mượn trả","images/muontra.png",7),
            ("Thống kê", "images/sta.png", 8),
        ]
        
        # Tạo các nút điều hướng và kết nối sự kiện cho từng nút
        for text, icon, index in nav_items:
            button = QPushButton(text)
            button.setIcon(QIcon(icon))  # Đặt biểu tượng cho nút
            button.setIconSize(QSize(20, 20))  # Điều chỉnh kích thước icon
            button.setStyleSheet("background-color: rgba(33,113,53,0.8); color: white; text-align: left; padding: 10px; border-radius: 5px")
            button.setFont(QFont("Arial", 10))
            button.clicked.connect(lambda checked, idx=index: self.stacked_widget.setCurrentIndex(idx))
            nav_layout.addWidget(button)

        # Thêm khoảng trống vào cuối để đẩy các nút lên trên
        nav_layout.addStretch()

        # Layout chính
        content_layout = QHBoxLayout()
        content_layout.addWidget(nav_widget)
        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(top_nav_widget)
        main_layout.addLayout(content_layout)


    def add_pages_to_stacked_widget(self):
        #Nhân viên
        staff_page = QWidget()
        staff_layout = QVBoxLayout()
        staff_layout.addWidget(QLabel("Nhân viên"))
        staff_page.setLayout(staff_layout)
        self.stacked_widget.addWidget(staff_page)

        # Sách 
        book_management_page_1 = QWidget()
        book_management_layout_1 = QVBoxLayout()
        book_management_layout_1.addWidget(QLabel("Sách"))
        book_management_page_1.setLayout(book_management_layout_1)
        self.stacked_widget.addWidget(book_management_page_1)


        # Tác giả
        author_page = QWidget()
        author_layout = QVBoxLayout()
        author_layout.addWidget(QLabel("Tác giả"))
        author_page.setLayout(author_layout)
        self.stacked_widget.addWidget(author_page)

        #Nhà xuất bản
        publisher_page = QWidget()
        publisher_layout = QVBoxLayout()
        publisher_layout.addWidget(QLabel("Nhà xuất bản"))
        publisher_page.setLayout(publisher_layout)
        self.stacked_widget.addWidget(publisher_page)

        # Độc giả
        reader_page = QWidget()
        reader_layout = QVBoxLayout()
        reader_layout.addWidget(QLabel("Độc giả"))
        reader_page.setLayout(reader_layout)
        self.stacked_widget.addWidget(reader_page)

        # Thẻ thư viện
        card_management_page = QWidget()
        card_management_layout = QVBoxLayout()
        card_management_layout.addWidget(QLabel("Thẻ thư viện"))
        card_management_page.setLayout(card_management_layout)
        self.stacked_widget.addWidget(card_management_page)

        search_layout = QHBoxLayout()
        centered_search_layout = QHBoxLayout()

        search_label = QLabel("Tìm kiếm thẻ thư viện:")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍Nhập số thẻ...")
        self.search_box.textChanged.connect(self.filter_card_table)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)

        centered_search_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        centered_search_layout.addLayout(search_layout)
        centered_search_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        card_management_layout.addLayout(centered_search_layout)

        # Tạo bảng QTableWidget
        self.card_table = QTableWidget()
        self.card_table.setColumnCount(4)  # 4 cột: Số Thẻ, Ngày Bắt đầu, Ngày Kết thúc, Ghi chú
        self.card_table.setHorizontalHeaderLabels(["Số Thẻ", "Ngày Bắt đầu", "Ngày Kết thúc", "Ghi chú"])

        # Lấy dữ liệu từ cơ sở dữ liệu và thêm vào bảng
        rows = self.get_card_data_from_db()
        self.card_table.setRowCount(len(rows))
        for row, data in enumerate(rows):
            for column, value in enumerate(data):
                # Chuyển đổi datetime.date thành chuỗi để tránh lỗi TypeError
                if isinstance(value, datetime.date):
                    value = value.strftime("%Y-%m-%d")  # Định dạng ngày theo ý muốn, ví dụ: YYYY-MM-DD
                self.card_table.setItem(row, column, QTableWidgetItem(str(value)))

        # Thêm bảng vào layout
        card_management_layout.addWidget(self.card_table)

        # Các nút Thêm, Sửa, Xóa
        button_layout = QHBoxLayout()
        add_button = QPushButton("Thêm")
        edit_button = QPushButton("Sửa")
        delete_button = QPushButton("Xóa")

        add_button.clicked.connect(self.add_card)
        edit_button.clicked.connect(self.edit_card)
        delete_button.clicked.connect(self.delete_card)

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        # Thêm các nút vào layout
        card_management_layout.addLayout(button_layout)

        # Thêm trang quản lý thẻ vào stacked widget
        card_management_page.setLayout(card_management_layout)
        self.stacked_widget.addWidget(card_management_page)


        # Quản lý mượn trả
        borrow_return_page = QWidget()
        borrow_return_layout = QVBoxLayout()
        borrow_return_layout.addWidget(QLabel("Quản lý mượn trả"))
        borrow_return_page.setLayout(borrow_return_layout)
        self.stacked_widget.addWidget(borrow_return_page)

        # Quản lý mượn trả
        detail_page = QWidget()
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(QLabel("Quản lý mượn trả"))
        detail_page.setLayout(detail_layout)
        self.stacked_widget.addWidget(detail_page)

        # Thống kê
        statistics_page = QWidget()
        statistics_layout = QVBoxLayout()
        statistics_layout.addWidget(QLabel("Thống kê"))
        statistics_page.setLayout(statistics_layout)
        self.stacked_widget.addWidget(statistics_page)

    def filter_card_table(self):
        search_text = self.search_box.text().strip().lower()
        for row in range(self.card_table.rowCount()):
            item = self.card_table.item(row, 0)  # Column 0 is 'Số Thẻ'
            self.card_table.setRowHidden(row, search_text not in item.text().lower())

    def add_card(self):
        # Mở cửa sổ thêm thẻ mới
        self.card_dialog = CardDialog(self, "Thêm thẻ")
        self.card_dialog.exec()

    def edit_card(self):
        # Mở cửa sổ sửa thẻ
        selected_row = self.card_table.currentRow()
        if selected_row != -1:
            card_data = [self.card_table.item(selected_row, i).text() for i in range(4)]
            self.card_dialog = CardDialog(self, "Sửa thẻ", card_data)
            self.card_dialog.exec()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thẻ để sửa")

    def delete_card(self):
        # Xóa thẻ đã chọn
        selected_row = self.card_table.currentRow()
        if selected_row != -1:
            reply = QMessageBox.question(self, 'Xác nhận', "Bạn có chắc muốn xóa thẻ này?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                card_number = self.card_table.item(selected_row, 0).text()
                self.delete_card_from_db(card_number)
                self.card_table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thẻ để xóa")

    def get_card_data_from_db(self):
        db = connect_to_db()
        if db:
            cursor = db.cursor()
            query = "SELECT soThe, ngayBatDau, ngayHetHan, ghiChu FROM the_thu_vien"
            cursor.execute(query)
            rows = cursor.fetchall()
            db.close()
            return rows
        return []

    def add_card_to_db(self, number, start_date, end_date, note):
        # Kiểm tra xem số thẻ đã tồn tại trong cơ sở dữ liệu chưa
        if self.check_card_exists(number):
            QMessageBox.warning(self, "Lỗi", "Số thẻ này đã tồn tại. Vui lòng nhập số thẻ khác.")
            return

        db = connect_to_db()  # Kết nối tới cơ sở dữ liệu
        if db:
            cursor = db.cursor()
            query = "INSERT INTO the_thu_vien (soThe, ngayBatDau, ngayHetHan, ghiChu) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (number, start_date, end_date, note))  # Thực thi truy vấn
            db.commit()  # Xác nhận thay đổi vào cơ sở dữ liệu
            db.close()  # Đóng kết nối cơ sở dữ liệu

            # Cập nhật bảng giao diện với thông tin thẻ mới
            self.card_table.insertRow(self.card_table.rowCount())  # Thêm một hàng mới vào cuối bảng
            self.card_table.setItem(self.card_table.rowCount() - 1, 0, QTableWidgetItem(number))
            self.card_table.setItem(self.card_table.rowCount() - 1, 1, QTableWidgetItem(start_date))
            self.card_table.setItem(self.card_table.rowCount() - 1, 2, QTableWidgetItem(end_date))
            self.card_table.setItem(self.card_table.rowCount() - 1, 3, QTableWidgetItem(note))

            self.refresh_and_sort_card_table()

    def check_card_exists(self, number):
        db = connect_to_db()
        if db:
            cursor = db.cursor()
            query = "SELECT COUNT(*) FROM the_thu_vien WHERE soThe = %s"
            cursor.execute(query, (number,))
            result = cursor.fetchone()
            db.close()
            return result[0] > 0  # Trả về True nếu số thẻ đã tồn tại
        return False



    def update_card_in_db(self, number, start_date, end_date, note, original_number):
        # Kiểm tra xem số thẻ mới có tồn tại không (và không phải là số thẻ cũ đang sửa)
        if number != original_number and self.check_card_exists(number):
            QMessageBox.warning(self, "Lỗi", "Số thẻ này đã tồn tại. Vui lòng nhập số thẻ khác.")
            return

        db = connect_to_db()
        if db:
            cursor = db.cursor()
            query = """UPDATE the_thu_vien 
                        SET soThe = %s, ngayBatDau = %s, ngayHetHan = %s, ghiChu = %s 
                        WHERE soThe = %s"""
            cursor.execute(query, (number, start_date, end_date, note, original_number))  # Cập nhật thẻ
            db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            db.close()  # Đóng kết nối cơ sở dữ liệu

            # Làm mới bảng và sắp xếp lại theo 'Số Thẻ'
            self.refresh_and_sort_card_table()


    def refresh_and_sort_card_table(self):
        rows = self.get_card_data_from_db()  # Lấy lại toàn bộ dữ liệu thẻ từ cơ sở dữ liệu
        rows.sort(key=lambda x: x[0])  # Sắp xếp các dòng theo số thẻ 
        # Xóa toàn bộ dữ liệu trong bảng
        self.card_table.setRowCount(0)

        # Thêm các dòng đã được sắp xếp vào bảng
        for row, data in enumerate(rows):
            self.card_table.insertRow(row)  # Thêm dòng mới vào bảng
            for column, value in enumerate(data):
                if isinstance(value, datetime.date):
                    value = value.strftime("%Y-%m-%d")  
                self.card_table.setItem(row, column, QTableWidgetItem(str(value)))  

    def delete_card_from_db(self, number):
        db = connect_to_db()
        if db:
            cursor = db.cursor()
            query = "DELETE FROM the_thu_vien WHERE soThe = %s"
            cursor.execute(query, (number,))
            db.commit()
            db.close()

    def logout(self):
       # Xác nhận đăng xuất
        reply = QMessageBox.question(self, 'Xác nhận', "Bạn có chắc muốn đăng xuất?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                subprocess.Popen(["python", "login.py"])  
                self.close()  
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Không thể mở giao diện đăng nhập: {e}")


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


class CardDialog(QDialog):
    def __init__(self, parent, title, card_data=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(300, 200)

        # Layout và form
        layout = QFormLayout(self)

        self.soThe = QLineEdit(self)
        self.ngayBatDau = QLineEdit(self)
        self.ngayHetHan = QLineEdit(self)
        self.ghiChu = QLineEdit(self)

        layout.addRow("Số thẻ:", self.soThe)
        layout.addRow("Ngày bắt đầu:", self.ngayBatDau)
        layout.addRow("Ngày hết hạn:", self.ngayHetHan)
        layout.addRow("Ghi chú:", self.ghiChu)

        # Nếu có dữ liệu thẻ, điền vào các trường
        if card_data:
            self.soThe.setText(card_data[0])
            self.ngayBatDau.setText(card_data[1])
            self.ngayHetHan.setText(card_data[2])
            self.ghiChu.setText(card_data[3])

        # Thêm nút xác nhận
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("Xác nhận", self)
        confirm_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Hủy", self)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        layout.addRow(button_layout)

    def accept(self):
        # Lấy dữ liệu từ các ô nhập liệu
        number = self.soThe.text()  
        start_date = self.ngayBatDau.text()  
        end_date = self.ngayHetHan.text()  
        note = self.ghiChu.text() 

        # Kiểm tra xem là thêm thẻ mới hay sửa thẻ cũ
        if self.windowTitle() == "Thêm thẻ":
            self.parent().add_card_to_db(number, start_date, end_date, note)  # Gọi hàm thêm thẻ mới
        elif self.windowTitle() == "Sửa thẻ":
            # Lấy số thẻ gốc để xác định hàng cần cập nhật trong cơ sở dữ liệu
            original_number = self.parent().card_table.item(self.parent().card_table.currentRow(), 0).text()
            # Gọi hàm cập nhật thẻ với số thẻ gốc và các thông tin đã chỉnh sửa
            self.parent().update_card_in_db(number, start_date, end_date, note, original_number)

            # Cập nhật bảng giao diện
            self.parent().card_table.setItem(self.parent().card_table.currentRow(), 0, QTableWidgetItem(number))
            self.parent().card_table.setItem(self.parent().card_table.currentRow(), 1, QTableWidgetItem(start_date))
            self.parent().card_table.setItem(self.parent().card_table.currentRow(), 2, QTableWidgetItem(end_date))
            self.parent().card_table.setItem(self.parent().card_table.currentRow(), 3, QTableWidgetItem(note))

        super().accept()  # Đóng hộp thoại sau khi hoàn thành


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
