import pygame
import os

pygame.font.init()

class FontManager:
    def __init__(self) -> None:
        """
        Font manager
        :return:
        """
        self.font_paths = []
        self.font_folder_path = os.path.join("Resources", "fonts")
        self.find_font_paths()

    def find_font_paths(self):
        """
        Get the font paths
        :return:
        """
        # get all the font directories in the fonts folder
        font_directories = os.listdir(os.path.join(os.getcwd(), self.font_folder_path))

        for font_dir in font_directories:
            if font_dir.endswith(".ttf"):
                # get the font name
                self.font_paths.append(os.path.join(os.getcwd(), self.font_folder_path, font_dir))


    def create_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        """
        Create a font object from a font name and size
        :param font_name: The name of the font file
        :param font_size: The size of the font
        :return: pygame.font.Font object
        """


        for font_path in self.font_paths:
            if font_path.endswith((font_name + ".ttf").lower()):
                return pygame.font.Font(font_path, font_size)


        try:
            font = pygame.font.SysFont(font_name, font_size)
            return font
        except pygame.error:
            raise Exception(f"Font '{font_name}' not found in the fonts file or in system fonts.")



font_manager = FontManager()
