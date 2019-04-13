import sys
import cv2
import os
import numpy as np
import random
import copy


sys.path.append("..")

from file_handler import FileHandler

FH = FileHandler()

class VideoMaker(object):
    """docstring for VideoMaker."""

    def __init__(self):
        self.fps = 24
        self.font_picker = {
            "Hershey Simplex" : cv2.FONT_HERSHEY_SIMPLEX,
            "Hershey Plain" : cv2.FONT_HERSHEY_PLAIN,
            "Hershey Duplex" : cv2.FONT_HERSHEY_DUPLEX,
            "Hershey Complex" : cv2.FONT_HERSHEY_COMPLEX,
            "Hershey Triplex" : cv2.FONT_HERSHEY_TRIPLEX,
            "Hershey Complex Small" : cv2.FONT_HERSHEY_COMPLEX_SMALL,
            "Hershey Script Simplex" : cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "Hershey Script Complex" : cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
            "Italic" : cv2.FONT_ITALIC
        }

    # pos = (rows, cols)
    def generate_sticker_pos(self,pos):
        rnd = random.choice(range(0,3))
        # 1/8 pre width
        # 1/6 pre height

        # Vlavo hore
        if rnd == 0:
            pos_width = self.resolution[0] // 8
            pos_height = self.resolution[1] // 6
            return [pos_width,pos_height]
        # Vpravo hore
        else:
            pos_width =  self.resolution[0] - self.resolution[0] // 8 - pos[1]
            pos_height = self.resolution[1] // 6
            return [pos_width,pos_height]

    def generate_text_pos(self):
        rnd = random.choice(range(0,3))
        # 1/8 pre width
        # 1/6 pre height

        # Stred
        if rnd == 0:
            pos_width = self.resolution[0] // 2
            pos_height = self.resolution[1] - self.resolution[1] // 6
            return [pos_width,pos_height]
        # Vlavo
        else:
            pos_width = self.resolution[0] // 8
            pos_height = self.resolution[1] - self.resolution[1] // 6
            return [pos_width,pos_height]

    def generate_video(self,settings):
        self.path = os.getcwd()
        self.title = settings["name"]
        self.video_id = settings["video_id"]
        self.extension = settings["format"]

        if settings["font"] in self.font_picker.keys():
            self.font = self.font_picker[settings["font"]]
        else:
            self.font = cv2.FONT_ITALIC

        self.texts = []

        if not settings["gender"].upper() == "NONE":
            if settings["gender"].upper() == "FEMALE":
                self.texts.append("For women.")
            else:
                self.texts.append("For men.")

        if not settings["brand"].upper() == "":
            self.texts.append("Created by " + settings["brand"])

        if not settings["price"].upper() == "":
            self.texts.append("Only " + settings["price"])

        if not settings["age"].upper() == "NONE":
            if settings["gender"].upper() == "YOUNG":
                self.texts.append("Good for young people.")
            elif settings["gender"].upper() == "ELDERLY":
                self.texts.append("Feel young again.")
            else:
                self.texts.append("For all categories.")

        if not settings["sale"].upper() == "":
            self.texts.append(settings["sale"])

        if not settings["product"].upper() == "":
            self.texts.append(settings["product"])

        if settings["resolution"].upper() == "HD":
            self.resolution = (1280, 720)
        else:
            self.resolution = (1920, 1080)

        self.background = FH.get_user_files_in_dir(self.video_id ,"/Background")
        self.product = FH.get_user_files_in_dir(self.video_id ,"/Products")
        self.stickers = FH.get_user_files_in_dir(self.video_id ,"/Stickers")

        # Nacitaj images
        self.product = self.load_images(self.product)
        self.stickers = self.load_images(self.stickers)

        # Je background nastaveny ?
        if self.background is None:
            self.gen_vid_bg_none()
        # Je BG video ?
        elif self.is_bg_video():
            self.gen_vid_bg_vid()
        # BG su obrazky
        else:
            self.gen_vid_bg_pic()

    def make_alpha(self,file):
        if file.shape[2] > 3:
            return file

        # Add an ALPHA channel to the loaded image
        b_channel, g_channel, r_channel = cv2.split(file)
        alpha_channel = np.zeros(b_channel.shape, dtype=b_channel.dtype) #creating a dummy alpha channel image.
        file = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        return file

    def load_images(self,links):
        if links is None:
            return []

        images = []
        for link in links:
            img = cv2.imread(link,-1)

            # JPG ?
            if img.shape[2] == 3:
                img = self.make_alpha(img)

            images.append(img)
        return images

    # Je background video alebo su to obrazky
    def is_bg_video(self):
        # Ak je viacero obrazkov
        if len(self.background) > 1:
            return False


        # Kontrola ci je to video
        if self.background[0][-4:].upper() == ".MP4":
            return True
        return False

    # Funkcia na resizovanie
    def resize_image(self,image,size,edging = True):
        tmp_img = self.image_resize(image,size[0],None)

        if tmp_img.shape[0] <= self.resolution[1] and tmp_img.shape[1] <= self.resolution[0]:
            return self.add_edges(tmp_img,edging)

        tmp_img = self.image_resize(image,None,size[1])

        if tmp_img.shape[0] <= self.resolution[1] and tmp_img.shape[1] <= self.resolution[0]:
            return self.add_edges(tmp_img,edging)

        print("Neda sa resiznut image !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None

    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def add_edges(self,image,edging):
        if not edging:
            return image

        edge_y = self.resolution[1] - image.shape[0]
        edge_x = self.resolution[0] - image.shape[1]

        if not edge_y == 0:
            height = int(edge_y / 2)
            size = (height,self.resolution[0],4)
            black_width = np.zeros(size,np.uint8)
            tmp_img = np.concatenate((black_width,image),axis=0)

            height = int(self.resolution[0] - tmp_img.shape[0])
            size = (height,self.resolution[1],4)
            black_width = np.zeros(size,np.uint8)
            tmp_img = np.concatenate((tmp_img,black_width),axis=0)

        if not edge_x == 0:
            width = int(edge_x / 2)
            size = (self.resolution[1],width,4)
            black_height = np.zeros(size,np.uint8)
            tmp_img = np.concatenate((black_height,image),axis=1)

            width = int(self.resolution[0] - tmp_img.shape[1])
            size = (self.resolution[1],width,4)
            black_height = np.zeros(size,np.uint8)
            tmp_img = np.concatenate((tmp_img,black_height),axis=1)

        return tmp_img

    # Generacia videa z background videom
    def gen_vid_bg_vid(self):
        self.background = self.load_images(self.background)
        pass

    # Generacia videa z bacground obrazkami
    def gen_vid_bg_pic(self):
        self.background = self.load_images(self.background)
        pass

    # Generacia videa bez backgroundu
    def gen_vid_bg_none(self):

        self.text_pos = self.generate_text_pos()

        filename = self.title + "." + self.extension
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        video = cv2.VideoWriter(self.path + "/" + filename, fourcc, self.fps, self.resolution)

        sticker = None
        txt = None

        # Loop through all product images
        for img in self.product:
            # Resize each image
            resized = self.resize_image(img,self.resolution)

            # Check if there are some
            if len(self.stickers) != 0:
                sticker = self.stickers.pop()
                res_sticker = self.resize_image(sticker,(self.resolution[0] // 6, self.resolution[1] // 4),False)

                stick_pos = self.generate_sticker_pos(res_sticker.shape)

            if len(self.texts) > 0:
                txt = self.texts.pop()
                length = random.choice(range(72,120))
            else:
                length = random.choice(range(54,84))


            if sticker is not None:
                resized = self.overlay_sticker(resized,res_sticker,stick_pos)


            # Ak je text poziciovany vlavo dole
            if self.text_pos[0] <= self.resolution[0] // 3:
                # Posun z prava do lava
                text_animation = [(self.resolution[0] - self.text_pos[0]) // length,0]
            else:
                # Posun zo stredu na kraj
                text_animation = [-(self.text_pos[0] // length),0]

            # Remove alpha channel
            b_channel, g_channel, r_channel = cv2.split(resized)[:3]
            resized = cv2.merge((b_channel,g_channel,r_channel))

            # Uloz si dolnu cast obrazka
            cropped_img = copy.deepcopy(resized[self.resolution[1] // 2: self.resolution[1] , 0 : self.resolution[0]])

            for i in range(0,length):

                # Ak je text tak mozme urobit posun
                if txt is not None:

                    # Prepisat dolnu cast obrazka
                    resized[self.resolution[1] // 2: self.resolution[1] , 0 : self.resolution[0]] = cropped_img

                    self.text_pos = [self.text_pos[0] + text_animation[0],self.text_pos[1] + text_animation[1]]

                    resized = self.overlay_text(resized,txt,self.text_pos)

                video.write(resized)

            sticker = None
            txt = None
        video.release()


    def overlay_sticker(self,image1,image2, pos):
        background = image1
        overlay = image2

        rows, cols, channels = overlay.shape

        # Make alpha channel
        background = self.make_alpha(background)
        overlay = self.make_alpha(overlay)

        alpha = copy.deepcopy(overlay)

        if pos is not None and overlay is not None and alpha is not None:

            rows, cols, color = alpha.shape

            for y in range(rows):
                for x in range(cols):
                    if alpha[y, x][3] == 0:
                        alpha[y, x][0] = 0
                        alpha[y, x][1] = 0
                        alpha[y, x][2] = 0
                        alpha[y, x][3] = 0
                    else:
                        alpha[y, x][0] = 255
                        alpha[y, x][1] = 255
                        alpha[y, x][2] = 255
                        alpha[y, x][3] = 255

            overlay = overlay.astype(float)
            background = background.astype(float)

            alpha = alpha.astype(float) / 255

            overlay = cv2.multiply(alpha, overlay)

            background_tmp = cv2.multiply(1.0 - alpha, background[50:50 + rows, 250: 250+cols])
            background_tmp = cv2.add(overlay,background_tmp)

            background[50:50+rows,250: 250+cols] = background_tmp

            background = np.uint8(background)

            #if pos[0] > (self.resolution[0] // 2):
            #   background[pos[1]:pos[1]+rows, pos[0]:pos[0]+cols ] = overlay
            #else:
            #    background[pos[0]:pos[0]+rows, pos[1]:pos[1]+cols ] = overlay

        return background

    def overlay_text(self,background,text,pos_text):
        pos_text = self.text_pos

        cv2.putText(background, text, (pos_text[0],pos_text[1]), self.font , 4, (255,255,255,255), 2,cv2.LINE_AA)

        return background
