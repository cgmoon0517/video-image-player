import os
import cv2


class VideoPlayer(object):

    def __init__(self, in_path=None, resizing=False, resizing_ratio=None):
        """
        Initialization for VideoPlayer class
        Args:
        :param in_path: path to video(or image) to play (e.g: ./data/video or ./data/image)
        :param resizing: flag for resizing video(or image) resolution
        :param resizing_ratio: resizing ratio for video(or image) resolution (e.g: 0.x: downsampling, 1.x: upsampling)
        """

        super(VideoPlayer, self).__init__()

        if not os.path.isdir(in_path) or len(os.listdir(in_path)) == 0:
            raise Exception("Check directory and files in data`s directory!")

        if resizing:
            assert resizing_ratio > 0, "resizing_ratio must be greater than 0"

        self._in_path = os.walk(in_path)
        self._resizing = resizing
        self._resizing_ratio = resizing_ratio
        self._frame_counter = 1  # frame counter of video

        # video(or image) display setting
        self._font = cv2.FONT_HERSHEY_DUPLEX
        self._thickness = 0.5
        self._color = (0, 0, 255)
        self._video_win_name = "Video"
        self._image_win_name = "Image"

        # key control setting
        self._key_space = 32
        self._key_d = 100
        self._key_q = 113

    def __resize_image(self, image):
        """
        Resize input video(or image) resolution using bilinear interpolation and return resized video(or image).
        Args:
        :param image: input video(or image)
        :return: resized video(or image)
        """

        image_height, image_width = image.shape[0:2]
        resized_image_width = int(image_width*self._resizing_ratio)
        resized_image_height = int(image_height*self._resizing_ratio)
        resized_image = cv2.resize(image, (resized_image_width, resized_image_height), cv2.INTER_LINEAR)

        return resized_image

    def __get_video(self, file_path, file_name, delay_time, save, save_interval, made_save_path, save_file_extension):
        """
        Play input video and save it as image sequence according to the parameter settings.
        Args:
        :param file_path: path to input video (e.g: './data/video/xxx.avi')
        :param file_name: file name of video without extension (e.g: 'xxx')
        :param delay_time: delay time for playing next frame
        :param save: flag for save video as image sequence using save_interval
        :param save_interval: interval of image sequence to saving(unit: frame count)
        :param made_save_path: path to saving image sequence (e.g: './data/video_to_image/xxx')
        :param save_file_extension: file extension name for saving image sequence (e.g: "PNG", "bmp" ... etc)
        :return: None
        """
        # capture video
        video = cv2.VideoCapture(file_path)

        if not delay_time:  # set delay time using fps
            fps = video.get(cv2.CAP_PROP_FPS)
            delay_time = int((1/int(fps))*1000)

        while video.isOpened():

            # read video
            captured, frame = video.read()

            if not captured:
                break

            # resize input video resolution
            if self._resizing:
                frame = self.__resize_image(frame)

            # save image sequence according to save_interval
            if save and self._frame_counter % save_interval == 0:
                save_filename = file_name + "_" + str(self._frame_counter).zfill(5) + "." + save_file_extension
                cv2.imwrite(os.path.join(made_save_path, save_filename), frame)

            # display file name, frame number and frame
            cv2.putText(frame, file_path, (0, 15), self._font, self._thickness, self._color)
            cv2.putText(frame, "#: "+str(self._frame_counter), (frame.shape[1]-80, 15),
                        self._font, self._thickness, self._color)
            cv2.imshow(self._video_win_name, frame)

            self._frame_counter += 1

            key = cv2.waitKey(delay_time)

            # press space bar for play waiting
            if key == self._key_space:
                cv2.waitKey(0)

            # press d for playing next video
            elif key == self._key_d:
                self._frame_counter = 1
                cv2.destroyAllWindows()
                break

            # press q for exit
            elif key == self._key_q:
                video.release()
                cv2.destroyAllWindows()
                exit()

        video.release()

    def __get_image(self, file_path):
        """
        Display input image.
        Args:
        :param file_path: path to input image(e.g: './data/image/xxx.jpg')
        :return: None
        """

        # load image from file path
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        # resize input image resolution
        if self._resizing:
            image = self.__resize_image(image)

        # display file name and image
        cv2.putText(image, file_path, (0, 15), self._font, self._thickness, self._color)
        cv2.imshow(self._image_win_name, image)

    @staticmethod
    def __make_save_folder(save_path, filename):
        """
        Make new folder for saving image sequence.
        Args:
        :param save_path: path to saving image sequence (e.g: './data/video_to_image')
        :param filename: file name of video without extension (e.g: 'xxx')
        :return: made new folder (e.g: './data/video_to_image/xxx')
        """

        made_save_path = save_path + "/" + filename
        if not os.path.isdir(made_save_path):
            os.mkdir(made_save_path)

        return made_save_path

    def play(self, play_mode, delay_time=None, save=False, save_interval=5, save_path=None, save_file_extension=None):
        """
        Play input video or image according to the parameter settings.
        Args:
        :param play_mode: option for play mode in video or image (e.g: "video" or "image")
        :param delay_time: delay time for playing next frame (None means delay time calculated automatically using fps)
        :param save: flag for save video as image sequence using save_interval
        :param save_interval: interval of image sequence to saving(unit: frame count)
        :param save_path: path to saving image sequence (e.g: './data/video_to_image')
        :param save_file_extension: file extension name for saving image sequence (e.g: "PNG", "bmp" ... etc)
        :return: None
        """

        # get root path and files list from input path
        for root_, dirs_, files_ in self._in_path:
            files_.sort()  # sort files list
            for filename_ in files_:
                path = os.path.join(root_, filename_)
                filename, ext = os.path.splitext(filename_)

                # play video
                if play_mode == "video":
                    if save:  # make folder same as file name
                        made_save_path = self.__make_save_folder(save_path, filename)

                    else:  # only play video
                        made_save_path = save_path
                    self.__get_video(path, filename, delay_time, save,
                                     save_interval, made_save_path, save_file_extension)

                # play image
                elif play_mode == "image":
                    self.__get_image(path)

                    key = cv2.waitKey(0)

                    # press q for exit
                    if key == self._key_q:
                        break

                cv2.destroyAllWindows()
