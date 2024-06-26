import sys
import cv2
import subprocess
from video_processing import VideoProcessor

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python process_network.py <cam_name> <channel> <rtsp_addr> <rtsp_post_addr> <show_time> <time_color> <gpu_encoder>")
        sys.exit(1)

    cam_name = sys.argv[1]
    channel = sys.argv[2]
    rtsp_addr = sys.argv[3]
    rtsp_post_addr = sys.argv[4]
    show_time = sys.argv[5] == "True"
    time_color = sys.argv[6]
    gpu_encoder = sys.argv[7]

    try:
        cap = cv2.VideoCapture(rtsp_addr)
        if not cap.isOpened():
            print(f"Error opening network stream: {rtsp_addr}")
            sys.exit(1)

        frame_width = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        frame_height = str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        target_fps = fps

        print("DEBUG: FPS = " + str(fps))
        print("DEBUG: RES = " + str(frame_width) + "x" + str(frame_height))

        video_processor = VideoProcessor()

        ffmpeg_command = [
            "ffmpeg",
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', frame_width + "x" + frame_height,
            '-r', str(fps),
            "-pix_fmt", "yuv420p",
            "-i", "-",
            "-c:v", gpu_encoder,
            "-b:v", "1000k",
            '-r', str(target_fps),
            "-pix_fmt", "yuv420p",
            '-s', frame_width + "x" + frame_height, 
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            f"{rtsp_post_addr}"
        ]

        print(ffmpeg_command)

        buffer_size = 1024 * 1024 * 4
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, bufsize=buffer_size)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream.")
                break
            
            if show_time:
                frame = video_processor.add_timestamp_to_frame(frame, cam_name, time_color, frame_width, frame_height)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
            ffmpeg_process.stdin.write(frame.tobytes())

            cv2.waitKey(1)

            # time.sleep(1 / 30)

        ffmpeg_process.communicate()
        cap.release()

        ffmpeg_process.stdin.close()

        ffmpeg_process.wait()

    except KeyboardInterrupt:
        sys.exit(0)
