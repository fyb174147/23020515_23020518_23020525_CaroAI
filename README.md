# Caro AI

Chương trình chơi cờ Caro 15x15 bằng Python/Pygame. Luật thắng theo đề bài: người chơi có 4 quân liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo sẽ thắng; không xét luật chặn hai đầu.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy game

```bash
python play.py
```

Màn hình bắt đầu cho phép chọn:

- `Human vs AI`: người chơi cầm đen, AI cầm trắng.
- `AI vs Human`: AI cầm đen, người chơi cầm trắng.
- `AI vs AI`: hai bên đều do AI điều khiển.
- `Human vs Human`: hai người chơi luân phiên trên cùng máy.
- Thuật toán AI: `Minimax` hoặc `Alpha-Beta`.

Quân đen luôn đi trước. Khi AI đi, terminal sẽ in nước đi được chọn, giá trị đánh giá, độ sâu, số trạng thái đã xét và thời gian chạy.

## Chạy thực nghiệm

```bash
python performance_eval.py
```

Script tạo file `ket_qua_thuc_nghiem.csv`, gồm 5 trạng thái kiểm thử, các độ sâu 1, 2, 3 và kết quả so sánh Minimax với Alpha-Beta trên cùng trạng thái, cùng hàm đánh giá.

## Cấu trúc chính

- `play.py`: vòng lặp game và xử lý bốn chế độ chơi.
- `source/AI.py`: Minimax, Alpha-Beta pruning, hàm đánh giá, kiểm tra thắng/hòa.
- `source/gomoku.py`: áp dụng nước đi, gọi AI và ghi nhận thông số tìm kiếm.
- `source/utils.py`: chuyển tọa độ, sinh pattern heuristic và Zobrist table.
- `gui/`: giao diện Pygame.
- `performance_eval.py`: benchmark phục vụ báo cáo.
- `BAO_CAO.md`: báo cáo theo yêu cầu đề bài.
