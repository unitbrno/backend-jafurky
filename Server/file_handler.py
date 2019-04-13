#!/usr/bin/python3

import os
import shutil
import glob

class FileHandler(object):
    """Handles files"""

    def __init__(self):
        self.users = {}
        # Change into directory for users
        os.chdir("../Users/")
        self.path = os.getcwd()

    # Vytvor link k suboru
    def create_path(self,string):
        return self.path + "/" + string

    # Vytvori zlozku pre uzivatela
    # @return boolean True ak sa podarilo False ak nie
    def create_user_folder(self,user_string):
        # Skontrolujeme ci uz neexistuje direcotry
        if self.check_existence_user_folder(user_string):
            return False
        # Pokus sa vytvorit zlozku
        try:
            os.mkdir(self.create_path(user_string))
        # Failo return false
        except Exception as e:
            return False
        return True

    # Vytvor Products, Stickers, Background
    def create_subdir_in_user(self, user_string):
        # Skontroluj ci existuje parent dir
        if not self.check_existence_user_folder(user_string):
            return False

        # Vojdi donho

        os.chdir(self.path + "/" + user_string)

        dir_path = os.getcwd()

        # Pokus sa vytvorit podadresare
        try:
            os.mkdir(dir_path + "/" + "Products")
            os.mkdir(dir_path + "/" + "Stickers")
            os.mkdir(dir_path + "/" + "Background")
        except Exception as e:
            return False
        return True

    # Skontroluj ci zlozka uz existuje
    def check_existence_user_folder(self,user_string):
        return os.path.isdir(self.create_path(user_string))

    # Vymaze folder uzivatela aj z celym jeho obsahom
    def remove_user_folder(self,user_string):
        # Ak neexistuje nie je co mazat
        if not self.check_existence_user_folder(user_string):
            return True

        # Mozme sa pokusit vymazat zlozku
        try:
            shutil.rmtree(self.create_path(user_string))
        except Exception as e:
            return False
        return True

    # Vrati obsah folderu a vsetko co obsahuje ako list stringov
    def get_user_files(self,user_string):
        # Directory z ktorej treba prehladavat
        root_dir = self.create_path(user_string)
        files_to_return = []

        # Zacneme prechadzat kazdu zlozku a pridavat do files subory
        for dir_, _, files in os.walk(root_dir):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, root_dir)
                rel_file = os.path.join(rel_dir, file_name)
                files_to_return.append(rel_file)
        return files_to_return

    def get_user_files_in_dir(self,user_string,path):
        root_dir = self.create_path(user_string + path)
        files_to_return = []

        # Zacneme prechadzat kazdu zlozku a pridavat do files subory
        for dir_, _, files in os.walk(root_dir):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, root_dir)
                rel_file = os.path.join("." + path, file_name)
                files_to_return.append(rel_file)

        if len(files_to_return) == 0:
            return None
        return files_to_return

    def exist_user_file(self,user_string):
        return os.path.isfile(self.create_path(user_string))

    # Vymaze specificky subor
    def remove_user_file(self,user_string,file_link):
        file_link = self.create_path(user_string) + "/" + file_link
        # Existuje subor na zmazanie ?
        if self.exist_user_file(file_link):
            return True

        # Pokusime sa vymazat subor
        try:
            os.remove(file_link)
        # Mazanie neuspelo
        except Exception as e:
            return False
        return True

    def get_user_dir_products(self, user_string):
        return self.path + "/" + user_string + "/Products"

    def get_user_dir_stickers(self, user_string):
        return self.path + "/" + user_string + "/Stickers"

    def get_user_dir_background(self, user_string):
        return self.path + "/" + user_string + "/Background"

    def get_video_path(self, user_string):
        return self.path + "/" + user_string
