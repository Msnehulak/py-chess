import customtkinter as ctk

# --- POMOCNÉ FUNKCE (LOGIKA FEN) ---

def pice_text_to_image(piece):
    """Převede písmeno z FEN na Unicode symbol."""
    mapping = {
        'P': "♙", 'R': "♖", 'N': "♘", 'B': "♗", 'Q': "♕", 'K': "♔",
        'p': "♟", 'r': "♜", 'n': "♞", 'b': "♝", 'q': "♛", 'k': "♚"  
    }
    return mapping.get(piece, "")

def fen_to_board(fen):
    """Převede FEN řetězec na 2D pole (list of lists)."""
    position = fen.split(' ')[0]
    rows = position.split('/')
    board = []
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend([None] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    return board

# --- HLAVNÍ TŘÍDA APLIKACE ---

class Board:
    def __init__(self):
        # Šachová data
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.color_w = "#eeeed2"
        self.color_b = "#769656"
        self.highlight_color = "#f2f28a"  # Jemná žlutá pro tahy
        self.toplay = "w"
        self.show_moves = []

        # Nastavení GUI
        self.size = 600
        self.square_size = self.size // 8
        self.size_offset = 10 

        self.root = ctk.CTk()
        self.root.title("Python Chess GUI")
        self.root.geometry(f"{self.size + self.size_offset * 2}x{self.size + self.size_offset * 2}")
        self.root.resizable(False, False)

        self.board_frame = ctk.CTkFrame(self.root, width=self.size, height=self.size)
        self.board_frame.pack(pady=self.size_offset, padx=self.size_offset)

        # Inicializace mřížky tlačítek (vytvoří se jen jednou)
        self.squares = []
        self._create_ui_grid()
        
        # První vykreslení figur
        self.update_display()

    def _create_ui_grid(self):
        """Vytvoří 64 tlačítek a uloží je do 2D pole self.squares."""
        for row in range(8):
            row_list = []
            for col in range(8):
                # Určení základní barvy pole
                base_color = self.color_w if (row + col) % 2 == 0 else self.color_b
                
                btn = ctk.CTkButton(
                    self.board_frame,
                    text="",
                    width=self.square_size,
                    height=self.square_size,
                    fg_color=base_color,
                    text_color="black",
                    font=("Arial", 45, "bold"),
                    corner_radius=0,
                    hover_color="#baca44",
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=row, column=col)
                row_list.append(btn)
            self.squares.append(row_list)

    def get_legal_moves(self, row, col):
        """Vypočítá možné tahy pro vybranou figuru."""
        board = fen_to_board(self.fen)
        pos = board[row][col]
        
        if pos is None:
            return []
            
        color = "w" if pos.isupper() else "b"
        char = pos.lower()
        
        if self.toplay != color:
            print(f"Teď hraje: {'bílá' if self.toplay == 'w' else 'černá'}!")
            return []

        move_list = []

        # logic for night
        if char == "n":
            knight_offsets = [
                (-2, -1), (-2, 1), (2, -1), (2, 1),
                (-1, -2), (-1, 2), (1, -2), (1, 2)
            ]
            for dr, dc in knight_offsets:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board[r][c]
                    if target is None:
                        move_list.append((r, c))
                    else:
                        target_color = "w" if target.isupper() else "b"
                        if target_color != color:
                            move_list.append((r, c))
                            
        return move_list

    def update_display(self):
        """Aktualizuje pouze vzhled existujících tlačítek (text a barvu)."""
        board_data = fen_to_board(self.fen)
        
        for r in range(8):
            for c in range(8):
                # 1. Aktualizace ikony figury
                piece = board_data[r][c]
                self.squares[r][c].configure(text=pice_text_to_image(piece))
                
                # 2. Aktualizace barvy (normální vs zvýrazněná)
                if (r, c) in self.show_moves:
                    self.squares[r][c].configure(fg_color="red") # Nebo self.highlight_color
                else:
                    base_color = self.color_w if (r + c) % 2 == 0 else self.color_b
                    self.squares[r][c].configure(fg_color=base_color)

    def on_square_click(self, row, col):
        """Obsluha kliknutí na políčko."""
        print(f"Klik na: [{row}, {col}]")
        
        # Získáme tahy pro dané políčko
        moves = self.get_legal_moves(row, col)
        
        # Uložíme do stavu a překreslíme
        self.show_moves = moves
        self.update_display()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Board()
    app.run()