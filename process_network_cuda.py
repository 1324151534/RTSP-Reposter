import sys
import cv2
import time
import subprocess
from video_processing import VideoProcessor

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python process_network.py <cam_name> <channel> <rtsp_addr> <rtsp_post_addr> <show_time> <time_color>")
        sys.exit(1)

    cam_name = sys.argv[1]
    channel = sys.argv[2]
    rtsp_addr = sys.argv[3]
    rtsp_post_addr = sys.argv[4]
    show_time = sys.argv[5] == "True"
    time_color = sys.argv[6]

    cv2.cuda.setDevice(0) 

    try:
        # Open network camera stream
        cap = cv2.cudacodec.createVideoReader(rtsp_addr)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)[1]
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)[1]

        frame_width = str(width).split(".")[0]
        frame_height = str(height).split(".")[0]

        fps = str(int(cap.get(cv2.CAP_PROP_FPS)[1])).split(".")[0]

        print("DEBUG: FPS = " + fps)
        print("DEBUG: RES = " + str(frame_width) + "x" + str(frame_height))

        video_processor = VideoProcessor()

        # Prepare ffmpeg command for streaming with H.265 encoding
        ffmpeg_command = [
            "ffmpeg",
            '-y',  # 覆盖输出文件（如果已存在）
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', frame_width + "x" + frame_height,  # 设置视频分辨率
            '-r', fps,  # 设置帧率
            "-pix_fmt", "yuv420p",  # 设置颜色空间
            "-i", "-",  # Read from stdin
            "-c:v", "hevc_nvenc",  # 使用 H.265 编码器
            "-b:v", "500k",  # 设置比特率
            '-r', fps,  # 设置帧率
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
            ret, frame = cap.nextFrame()
            if not ret:
                print("End of video stream.")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Add timestamp and camera ID to each frame
            if show_time:
                frame = video_processor.add_timestamp_to_frame(frame, cam_name, time_color, frame_width, frame_height)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
            # Write frame to stdin for ffmpeg to read
            ffmpeg_process.stdin.write(frame.tobytes())

            # time.sleep(1 / 30)

        ffmpeg_process.communicate()
        # Close the network stream
        cap.release()

        # Close stdin to signal the end
        ffmpeg_process.stdin.close()

        # Wait for ffmpeg process to finish
        ffmpeg_process.wait()

    except KeyboardInterrupt:
        sys.exit(0)
