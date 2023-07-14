from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QLineEdit, QVBoxLayout, QWidget, \
    QLabel, QHBoxLayout, QCheckBox, QPushButton
from PySide6.QtGui import QPainter, QImage, QPixmap
from minimax import find_best_move
import chess
import chess.svg
import cairosvg
import time
import sys


class ChessGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Chess GUI")
        self.setGeometry(100, 100, 640, 480)

        # Initialize the chessboard
        self.board = chess.Board()

        # minmax depth
        self.depth = 3

        # evaluation weights
        self.values_param_white = 1
        self.position_param_white = 0.03
        self.values_param_black = 1
        self.position_param_black = 0.06

        # Load the initial chessboard SVG image
        self.update_board_image()

        # Convert SVG to QPixmap
        self.board_pixmap = self.convert_svg_to_pixmap(self.board_image)

        # Create the QGraphicsScene and QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.view.setSceneRect(0, 0, self.board_pixmap.width(), self.board_pixmap.height())
        self.view.setStyleSheet("border: none;")

        # Add the chessboard image to the scene
        self.chessboard_item = self.scene.addPixmap(self.board_pixmap)

        # Create the text boxes
        # self.move_input_white = QLineEdit()
        # self.move_input_black = QLineEdit()

        # Create the checkboxes
        #self.checkbox_white = QCheckBox("White")
        #self.checkbox_black = QCheckBox("Black")

        # Create the buttons
        self.start_button = QPushButton("Start")
        # self.pause_button = QPushButton("Pause")

        # Create the layout and central widget
        layout = QVBoxLayout()
        layout.addWidget(self.view)

        # Create the input boxes layout
        # input_layout = QHBoxLayout()
        # input_layout.addWidget(QLabel("White Move:"))
        # input_layout.addWidget(self.move_input_white)
        # input_layout.addWidget(self.checkbox_white)
        # input_layout.addWidget(QLabel("Black Move:"))
        # input_layout.addWidget(self.move_input_black)
        # input_layout.addWidget(self.checkbox_black)

        # layout.addLayout(input_layout)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        # button_layout.addWidget(self.pause_button)

        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)

        # Connect the text boxes' returnPressed signals to handle_move_input
        # self.move_input_white.returnPressed.connect(self.handle_move_input)
        # self.move_input_black.returnPressed.connect(self.handle_move_input)

        # Connect the checkboxes' stateChanged signals to handle_checkbox_state
        # self.checkbox_white.stateChanged.connect(self.handle_checkbox_state)
        # self.checkbox_black.stateChanged.connect(self.handle_checkbox_state)

        # Connect the button clicked signals to handle_button_click
        self.start_button.clicked.connect(self.handle_button_click)
        # self.pause_button.clicked.connect(self.handle_button_click)

        # Initialize the player turn and checkbox states
        self.current_player = chess.WHITE
        # self.checkbox_white.setChecked(True)
        # self.checkbox_black.setChecked(True)

        # Disable the input field for the player who is not on turn
        # self.move_input_white.setEnabled(False)
        # self.move_input_black.setEnabled(False)

        # disable pause btn on start up
        # self.pause_button.setEnabled(False)

    def convert_svg_to_pixmap(self, svg_data):
        image = QImage.fromData(svg_data)
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def update_board_image(self):
        self.board_svg = chess.svg.board(board=self.board).encode("UTF-8")
        self.board_image = cairosvg.svg2png(bytestring=self.board_svg)

    def handle_move_input(self):
        if self.current_player == chess.WHITE:
            move = self.move_input_white.text()
            self.move_input_white.clear()
            self.move_input_black.setEnabled(True)
            self.move_input_white.setEnabled(False)
            self.move_input_black.setFocus()
        else:
            move = self.move_input_black.text()
            self.move_input_black.clear()
            self.move_input_white.setEnabled(True)
            self.move_input_black.setEnabled(False)
            self.move_input_white.setFocus()

        # Apply the move to the chessboard if it is valid
        if self.is_valid_move(move):
            self.board.push_san(move)
            self.update_board_image()
            self.board_pixmap = self.convert_svg_to_pixmap(self.board_image)
            self.chessboard_item.setPixmap(self.board_pixmap)

            # Switch the player turn
            self.current_player = not self.current_player

            print("Move:", move)
            print("Current Player:", "White" if self.current_player == chess.WHITE else "Black")

        else:
            print("Invalid move!")

    def is_valid_move(self, move):
        legal_moves = self.board.legal_moves
        return chess.Move.from_uci(move) in legal_moves

    def handle_checkbox_state(self):
        white_active = self.checkbox_white.isChecked()
        black_active = self.checkbox_black.isChecked()

        self.move_input_white.setEnabled(white_active)
        self.move_input_black.setEnabled(black_active)

    def handle_button_click(self):
        sender = self.sender()
        if sender == self.start_button:
            print("Game started")
            # if not self.checkbox_white.isChecked() and not self.checkbox_black.isChecked():
            self.bot_game()
            # elif self.checkbox_black.isChecked() and self.checkbox_white.isChecked():
            #     self.move_input_white.setEnabled(True)
            # else:
            #     pass
        # elif sender == self.pause_button:
        #     print("Pause button clicked")

    def bot_game(self):
        self.start_button.setEnabled(False)
        while not self.board.is_game_over():
            QApplication.processEvents()
            self.bot_move()

            # draw new board
            self.update_board_image()
            self.board_pixmap = self.convert_svg_to_pixmap(self.board_image)
            self.chessboard_item.setPixmap(self.board_pixmap)

            self.current_player = not self.current_player

            time.sleep(0.5)
        result = self.board.outcome()
        print(f"Game over! Result: {result.result()}")
        self.start_button.setEnabled(True)

    def bot_move(self, alone=False):
        if alone:
            QApplication.processEvents()

        if self.current_player:
            move = find_best_move(self.board, self.depth, self.current_player, self.values_param_white, self.position_param_white)
        else:
            move = find_best_move(self.board, self.depth, self.current_player, self.values_param_black, self.position_param_black)
        self.board.push(move)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the chessboard pixmap
        painter.drawPixmap(0, 0, self.board_pixmap)

        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessGUI()
    window.show()
    sys.exit(app.exec())
