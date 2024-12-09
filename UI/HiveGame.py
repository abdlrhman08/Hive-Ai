import pygame

from .hex_utils import (
    calculate_hex_dimensions,
    hexagon_vertices, point_in_hexagon
)

from utils.board import Board
from utils.location import Location
from utils.pieces import Ant, Beetle, Grasshopper, Queen, Spider

# Screen
WIDTH, HEIGHT = 800, 600

# Colors
BACKGROUND = (255, 255, 255)  # Background
BLACK = (0, 0, 0)  # Black for Lines
HOVER_COLOR = (220, 220, 220)  # Light Grey When Hovered
CLICK_COLOR = (255, 0, 0)  # Red when clicked

# Hexagon attributes
HEX_GRID = 10  # Grid size
HEX_RADIUS = 30
MIN_HEX_RADIUS = 10
MAX_HEX_RADIUS = 80

HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(
    HEX_RADIUS)

# Draw honeycomb pattern
def draw_hex_grid(rows, cols, hex_radius, offset_x=0, offset_y=0):
    hexagons = []
    for row in range(rows):
        for col in range(cols):
            # Horizontal offset
            x_offset = col * HORIZONTAL_SPACING + \
                (row % 2) * (HORIZONTAL_SPACING / 2) + offset_x
            # Vertical offset
            y_offset = row * VERTICAL_SPACING + offset_y
            hexagon = hexagon_vertices(x_offset, y_offset, hex_radius)
            # Store row and col instead of position
            hexagons.append((hexagon, (row, col)))
    return hexagons


class HiveGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.hexagons = draw_hex_grid(HEX_GRID, HEX_GRID, HEX_RADIUS)
        self.offset_x = 0
        self.offset_y = 0
        self.selected_piece = None

        self.init_piece_holder()
        # create a board
        self.board = Board()

        pygame.display.set_caption("Hive Game")

    def check_game_events(self):
        global HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update the offset to drag the grid
                if event.buttons[0]:
                    self.offset_x += event.rel[0]
                    self.offset_y += event.rel[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in/out with mouse wheel
                if event.button == 4:  # Scroll Up
                    if HEX_RADIUS < MAX_HEX_RADIUS:
                        HEX_RADIUS += 5  # Increase radius
                elif event.button == 5:  # Scroll Down
                    if HEX_RADIUS > MIN_HEX_RADIUS:
                        HEX_RADIUS -= 5  # Decrease radius

                self.check_piece_selection()

    def start_game_loop(self):
        global HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING

        self.running = True
        hex_states = {}

        clicked_this_frame = False  # Flag to track if click is processed yet
        while self.running:
            self.screen.fill(BACKGROUND)
            # Mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Hovering and clicking
            for hexagon, (row, col) in self.hexagons:
                hex_key = (row, col)  # Use grid indices
                if point_in_hexagon(mouse_pos[0], mouse_pos[1], hexagon):
                    # Highlight on hovering
                    pygame.draw.polygon(self.screen, HOVER_COLOR, hexagon)
                    pygame.draw.polygon(self.screen, BLACK, hexagon, 2)  # Black outline
                    # Left mouse click and not processed yet
                    if mouse_pressed[0] and not clicked_this_frame:
                        # If it was not clicked before, color it and store the state
                        if hex_key not in hex_states:
                            hex_states[hex_key] = CLICK_COLOR  # red
                        # Fill with stored color in state
                        pygame.draw.polygon(self.screen, hex_states[hex_key], hexagon)
                        pygame.draw.polygon(self.screen, BLACK, hexagon, 2)  # Black outline
                        print(f"Hexagon clicked at ({row}, {col})")
                        clicked_this_frame = True  # processed
                else:
                    # Draw the hexagon with its current state (color)
                    if hex_key in hex_states:
                        # Use the stored colors
                        pygame.draw.polygon(self.screen, hex_states[hex_key], hexagon)
                    else:
                        # Default white color
                        pygame.draw.polygon(self.screen, BACKGROUND, hexagon)
                    pygame.draw.polygon(self.screen, BLACK, hexagon, 2)  # Black outline

            if not mouse_pressed[0]:
                clicked_this_frame = False        # Recalculate hexagon dimensions

            self.draw_hand()
            self.check_game_events()

            HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(
                HEX_RADIUS
            )

            # Redraw grid with new offset
            self.hexagons = draw_hex_grid(
                HEX_GRID, HEX_GRID, HEX_RADIUS, self.offset_x, self.offset_y
            )
            pygame.display.flip()

    def init_piece_holder(self):
        self.hand = [
            Ant, Ant, Ant,
            Beetle, Beetle,
            Grasshopper, Grasshopper, Grasshopper,
            Queen, Spider, Spider
        ]
        self.piece_rects = []
        # I got them by trial and error so don't ask me
        self.holder_width = WIDTH * 3/4 + 20
        self.holder_height = HEIGHT * 1/4 + 10
        self.pieces_holder_border = pygame.rect.Rect((WIDTH * 3/4, HEIGHT * 1/4), (WIDTH * 1/4 + 5, 125))
        self.pieces_holder = pygame.rect.Rect((WIDTH * 3/4 + 5, HEIGHT * 1/4 + 5), (WIDTH * 1/4, 125 - 10))

        for index, piece in enumerate(self.hand):
            x = self.holder_width + (index % 4 * 40)
            y = self.holder_height + (index // 4) * 35
            self.piece_rects.append(piece.sprite.get_rect().move(x, y))


    def draw_hand(self):
        weird_brown_color = (210, 189, 150)
        pygame.draw.rect(self.screen, (10, 10, 10), self.pieces_holder_border, border_radius = 5)
        pygame.draw.rect(self.screen, weird_brown_color, self.pieces_holder, border_radius = 5)

        for index, piece in enumerate(self.hand):
            x = self.holder_width + (index % 4 * 40)
            y = self.holder_height + (index // 4) * 35
            self.screen.blit(piece.sprite, (x, y))

    def check_piece_selection(self):
        mouse_pos = pygame.mouse.get_pos()

        for piece_rect, piece in zip(self.piece_rects, self.hand):
            if piece_rect.collidepoint(mouse_pos):
                self.selected_piece = piece
