class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text: str, key: int) -> str:
        if key <= 1:
            return plain_text
            
        # Tạo ma trận trống để xếp chữ
        rail = [['\n' for i in range(len(plain_text))] for j in range(key)]
        
        dir_down = False
        row, col = 0, 0
        
        for i in range(len(plain_text)):
            # Đảo hướng khi chạm rầy trên cùng hoặc dưới cùng
            if (row == 0) or (row == key - 1):
                dir_down = not dir_down
            
            rail[row][col] = plain_text[i]
            col += 1
            
            # Tìm hàng tiếp theo
            if dir_down:
                row += 1
            else:
                row -= 1
                
        # Đọc kết quả theo từng hàng ngang từ trên xuống dưới
        result = []
        for i in range(key):
            for j in range(len(plain_text)):
                if rail[i][j] != '\n':
                    result.append(rail[i][j])
        return "".join(result)

    def rail_fence_decrypt(self, cipher_text: str, key: int) -> str:
        if key <= 1:
            return cipher_text
            
        # Tạo ma trận trống
        rail = [['\n' for i in range(len(cipher_text))] for j in range(key)]
        
        # Đánh dấu các vị trí zigzag bằng ký tự '*'
        dir_down = None
        row, col = 0, 0
        
        for i in range(len(cipher_text)):
            if row == 0:
                dir_down = True
            if row == key - 1:
                dir_down = False
            
            rail[row][col] = '*'
            col += 1
            
            if dir_down:
                row += 1
            else:
                row -= 1
        
        # Điền các ký tự của chuỗi mã hóa vào các vị trí đã đánh dấu '*'
        index = 0
        for i in range(key):
            for j in range(len(cipher_text)):
                if (rail[i][j] == '*') and (index < len(cipher_text)):
                    rail[i][j] = cipher_text[index]
                    index += 1
        
        # Đọc lại ma trận theo đường zigzag để lấy chuỗi gốc ban đầu
        result = []
        row, col = 0, 0
        for i in range(len(cipher_text)):
            if row == 0:
                dir_down = True
            if row == key - 1:
                dir_down = False
            
            if rail[row][col] != '*':
                result.append(rail[row][col])
                col += 1
            
            if dir_down:
                row += 1
            else:
                row -= 1
        return "".join(result)