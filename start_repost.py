import json
import subprocess

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        config_data = json.load(file)
        print(config_data)

    processes = []

    for camera_config in config_data:
        cam_name = config_data[camera_config]["name"]
        channel = config_data[camera_config]["channel"]
        status = config_data[camera_config]["status"] == "本地"
        rtsp_addr = config_data[camera_config]["rtsp_addr"]
        rtsp_post_addr = config_data[camera_config]["rtsp_post_addr"]
        local_file = config_data[camera_config]["local_file"]
        show_time = config_data[camera_config]["show_time"] == "True"
        time_color = config_data[camera_config]["time_color"]

        print("启动摄像头" + cam_name)

        if status:
            # If status is "本地", use local_file for processing
            process = subprocess.Popen(
                ["python", "process_local.py", cam_name, channel, local_file, rtsp_post_addr, str(show_time), time_color]
            )
        else:
            # If status is "网络", use rtsp_addr for processing
            process = subprocess.Popen(
                ["python", "process_network.py", cam_name, channel, rtsp_addr, rtsp_post_addr, str(show_time), time_color]
            )

        processes.append(process)

    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
