import click
from manager.player import VideoPlayer


@click.command()
@click.option("--play_mode", default="video",
              help='option for play mode in video or image. if want to play image, set to "image".')
@click.option("--in_path", default="./data/video",
              help='path to video(or image) to play. if want to play image, set to "./data/image".')
@click.option("--resizing", default=False,
              help='flag for resizing video(or image) resolution. if want to resize video(or image), set to True')
@click.option("--resizing_ratio", default=None, type=click.FLOAT,
              help='resizing ratio for video(or image) resolution. '
                   'if want to downsampling, set to 0.x, upsampling set to 1.x.')
@click.option("--delay_time", default=None, type=click.INT,
              help='delay time for playing next frame. '
                   'None means delay time calculated automatically using fps of video.' 
                   'if want to set delay time manually, set to desired number(e.g: 24).')
@click.option("--save", default=False,
              help='flag for save video as image sequence. if want to save, set to True.')
@click.option("--save_interval", default=5,
              help='interval of image sequence to saving. if set to 10, it will be saved as one image per 10 frames.')
@click.option("--save_path", default="./data/video_to_image",
              help='path to saving image sequence. '
                   'sub-folder is created same as video file name in the folder and then image sequence will be saved.')
@click.option("--save_file_extension", default="PNG",
              help='file extension name for saving image sequence(e.g: "PNG", "bmp" ... etc).')
def main(play_mode, in_path, resizing, resizing_ratio, delay_time, save, save_interval, save_path, save_file_extension):

    # video play mode
    if play_mode == "video":
        vp = VideoPlayer(in_path, resizing, resizing_ratio)
        vp.play(play_mode, delay_time, save, save_interval, save_path, save_file_extension)

    # image play mode
    elif play_mode == "image":
        vp = VideoPlayer(in_path, resizing, resizing_ratio)
        vp.play(play_mode)


if __name__ == "__main__":

    main()


"""
* script usage: 
1. when play video using fps: 
python main.py --play_mode="video" 
    
1.1 when play resized video using delay time:
python main.py --play_mode="video" --delay_time=24 --resizing=True --resizing_ratio=0.5
    
1.2 when play resized video using delay time and save image sequence:
python main.py --play_mode="video" --delay_time=1 --resizing=True --resizing_ratio=0.5 --save=True --save_interval=10
               --save_file_extension="PNG"

2. when play image:
python main.py --play_mode="image" --in_path="./data/image" 
    
2.1 when play resized image: 
python main.py --play_mode="image" --in_path="./data/image" --resizing=True --resizing_ratio=0.5
    
* keyboard use:
1. space bar: stop video play 
2. any key: continue video(or image) play   
3. d: play for next video file(only when playing video)
4. q: exit
"""

