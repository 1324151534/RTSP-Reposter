import sys
import cv2
import subprocess
from video_processing import VideoProcessor

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python process_local.py <cam_name> <channel> <input_file> <rtsp_post_addr> <show_time> <time_color>")
        sys.exit(1)

    cam_name = sys.argv[1]
    channel = sys.argv[2]
    input_file = sys.argv[3]
    rtsp_post_addr = sys.argv[4]
    show_time = sys.argv[5] == "True"
    time_color = sys.argv[6]

    try:
        cap = cv2.VideoCapture(input_file)
        # print("DEBUG: Format is " + str(cap.get(cv2.CAP_PROP_FORMAT)))

        frame_width = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        frame_height = str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        target_fps = fps - 5

        print("DEBUG: FPS = " + str(fps))
        print("DEBUG: RES = " + str(frame_width) + "x" + str(frame_height))

        if not cap.isOpened():
            print(f"Error opening video file: {input_file}")
            sys.exit(1)

        video_processor = VideoProcessor()

        # Prepare ffmpeg command for streaming with H.264 encoding
        ffmpeg_command = [
            "ffmpeg",
            '-y',  # 覆盖输出文件（如果已存在）
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', frame_width + "x" + frame_height,  # 设置视频分辨率
            '-r', str(fps),  # 设置帧率
            "-pix_fmt", "yuv420p",  # 设置颜色空间
            "-i", "-",  # Read from stdin
            "-c:v", "hevc_nvenc",  # 使用 H.265 编码器
            "-b:v", "500k",  # 设置比特率
            '-r', str(target_fps),  # 设置帧率
            "-pix_fmt", "yuv420p",  # 设置颜色空间
            '-s', frame_width + "x" + frame_height, 
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            f"{rtsp_post_addr}"
        ]

        print(ffmpeg_command)

        buffer_size = 1024 * 1024 * 4
        # Start ffmpeg process with a pipe for stdin
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, bufsize=buffer_size)

        while True:
            ret, frame = cap.read()
            if not ret:
                # 视频文件结束，重新开始
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Add timestamp and camera ID to each frame
            if show_time:
                frame = video_processor.add_timestamp_to_frame(frame, cam_name, time_color, frame_width, frame_height)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
            # Write frame to stdin for ffmpeg to read
            ffmpeg_process.stdin.write(frame.tobytes())

            cv2.waitKey(int((1000/fps) / 2))
            # time.sleep(1 / (fps * 2))

    except KeyboardInterrupt:
        sys.exit(0)
