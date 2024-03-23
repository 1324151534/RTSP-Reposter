import json
import subprocess

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        config_data = json.load(file)
        # print(config_data)

    with open('control_config.json', 'r') as file:
        control_config = json.load(file)

    version = control_config["version"]
    cuda = control_config["cuda"] == 1
    use_gpu = control_config["use_gpu"] == 1

    gpu_encoder_enum = {
        "QSV 编码（Intel核显）" : "h264_qsv",
        "NVENC 编码（NVIDIA显卡）" : "h264_nvenc",
        "AMF 编码（AMD显卡）" : "h264_amf"
    }

    if use_gpu:
        gpu_encoder = gpu_encoder_enum[control_config["hardware_decoding_option"]]
    else:
        gpu_encoder = "libx264"

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
        activation = config_data[camera_config]["activate"] == "True" or "1"

        local_filename = "process_local.py"
        network_filename = "process_network.py"

        '''
        if cuda:
            local_filename = "process_local_cuda.py"
            network_filename = "process_network_cuda.py"

        '''
        
        if activation:

            print("启动摄像头" + cam_name)
            
            if status:
                # If status is "本地", use local_file for processing
                process = subprocess.Popen(
                    ["python", local_filename, cam_name, channel, local_file, rtsp_post_addr, str(show_time), time_color, gpu_encoder]
                )
            else:
                # If status is "网络", use rtsp_addr for processing
                process = subprocess.Popen(
                    ["python", network_filename, cam_name, channel, rtsp_addr, rtsp_post_addr, str(show_time), time_color, gpu_encoder]
                )

            processes.append(process)

    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
