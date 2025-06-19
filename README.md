Ứng dụng Truyền File Trực Tiếp
Ứng dụng này cho phép truyền file trực tiếp giữa Người Gửi (Sender) và Người Nhận (Receiver) thông qua WebSocket với tính năng ký số RSA để đảm bảo tính toàn vẹn. File được gửi trực tiếp mà không lưu trữ trên server, sử dụng giao diện tách biệt cho hai vai trò.
Mô tả

Người Gửi: Tạo cặp khóa RSA, chọn file và gửi trực tiếp qua WebSocket.
Người Nhận: Nhận file tự động, tải xuống và xác minh chữ ký.
Công nghệ: Flask, SocketIO, PyCryptoDome, HTML, Tailwind CSS.

Yêu cầu hệ thống

Python 3.7 hoặc cao hơn.
Thư viện cần thiết:
flask
flask-socketio
pycryptodome
uuid



Cài đặt

Clone kho lưu trữ (nếu có):git clone <repository-url>
cd <repository-folder>


Tạo thư mục cần thiết:mkdir keys


Cài đặt các thư viện:pip install flask flask-socketio pycryptodome uuid


Chạy ứng dụng:python app.py


Mở trình duyệt và truy cập:
http://localhost:5000/sender cho Người Gửi.
http://localhost:5000/receiver cho Người Nhận.





Hướng dẫn sử dụng
Người Gửi

Truy cập http://localhost:5000/sender.
Nhấn "Tạo Khóa RSA" để tạo cặp khóa (khóa riêng và khóa công khai).
Chọn file muốn gửi.
Nhấn "Gửi File Trực Tiếp" để gửi qua WebSocket.
Kiểm tra kết quả trong phần "Kết quả".

Người Nhận

Truy cập http://localhost:5000/receiver.
Đợi file được gửi từ Người Gửi (tự động tải xuống khi nhận).
Chọn file đã tải từ máy tính.
Nhấn "Xác Minh Chữ Ký" để kiểm tra tính toàn vẹn.
Kết quả hiển thị trong phần "Kết quả".

Cấu trúc dự án

app.py: Backend xử lý WebSocket và API.
sender.html: Giao diện Người Gửi (tông màu xanh dương).
receiver.html: Giao diện Người Nhận (tông màu xanh lá).
keys/: Thư mục lưu trữ khóa công khai tạm thời.
history.json: Lưu lịch sử gửi file (chỉ metadata).

Lưu ý

Giới hạn file: Ứng dụng phù hợp với file nhỏ (dưới 10MB) do giới hạn WebSocket. File lớn hơn có thể gây chậm hoặc lỗi.
Bảo mật: Khóa công khai và chữ ký được gửi cùng file để Receiver xác minh.
Lỗi: Kiểm tra Console (F12) hoặc terminal để debug.

Phát triển và đóng góp

Fork kho lưu trữ và tạo Pull Request nếu muốn đóng góp.
Báo cáo lỗi qua issue tracker (nếu có).

Giấy phép
[Thêm thông tin giấy phép nếu cần, ví dụ: MIT License]
Liên hệ
Hỗ trợ: [Thêm email hoặc liên hệ nếu cần].
![image](https://github.com/user-attachments/assets/6f877485-0b37-4dd0-936c-bebd8ad6ebb1)

