# import boto3
# from botocore.client import Config
import uuid
from time import time
import cv2                                                                                                                                                                                                                                                                                                                            
import ctypes
import mmap

# tmp = "/home/kaifengx/serverless-faas-workbench/dataset/video/"
tmp = "/tmp/dataset/video/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2

buf_s = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
fpointer_s = ctypes.c_void_p.from_buffer(buf_s)
f_s = ftype(ctypes.addressof(fpointer_s))

buf_s.write(
    b'\x8b\xc7'  # mov eax, edi
    b'\x83\xc0\x01'  # add eax, 1
    b'\x0f\x1f\x84\xbe\x00\x00\x01\x01' # nop
    b'\xc3' #ret
)

buf_e = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
fpointer_e = ctypes.c_void_p.from_buffer(buf_e)
f_e = ftype(ctypes.addressof(fpointer_e))

buf_e.write(
    b'\x8b\xc7'  # mov eax, edi
    b'\x83\xc0\x01'  # add eax, 1
    b'\x0f\x1f\x84\xed\x00\x00\x01\x01' # nop
    b'\xc3' #ret
)

def video_processing(object_key, video_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+'-output.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    if not video.isOpened():
        return 0, 0
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path

def main(event):
    f_s(0)
    latencies = {}
    timestamps = {}
    
    # timestamps["starting_time"] = time()
    # input_bucket = event['input_bucket']
    # object_key = event['object_key']
    # output_bucket = event['output_bucket']
    # endpoint_url = event['endpoint_url']
    # aws_access_key_id = event['aws_access_key_id']
    # aws_secret_access_key = event['aws_secret_access_key']
    # metadata = event['metadata']

    # s3_client = boto3.client('s3',
    #                 endpoint_url=endpoint_url,
    #                 aws_access_key_id=aws_access_key_id,
    #                 aws_secret_access_key=aws_secret_access_key)#,                                                                                                                                                                                                                                                                                                            
    #                 #config=Config(signature_version='s3v4'),                                                                                                                                                                                                                                                                                                                 
    #                 #region_name='us-east-1')                                                                                                                                                                                                                                                                                                                                 

    object_key = 'SampleVideo_1280x720_10mb.mp4'
    # path = tmp + object_key
    # download_path = tmp + '{}'.format(object_key)
    download_path = tmp + object_key
    # download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)

    # start = time()
    # s3_client.download_file(input_bucket, object_key, download_path)
    # get file from host port 1450
    # os.system("curl 'http://0.0.0.0:1450/video/" + object_key + "' -o " + download_path)
    # download_latency = time() - start
    # latencies["download_data"] = download_latency

    video_processing_latency, upload_path = video_processing(object_key, download_path)
    latencies["function_execution"] = video_processing_latency

    # start = time()
    # s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])
    # upload_latency = time() - start
    # latencies["upload_data"] = upload_latency
    # timestamps["finishing_time"] = time()

    # return {"path": upload_path, "latencies": latencies, "timestamps": timestamps, "metadata": metadata}
    # return
    f_e(0)
    return {"latencies": latencies, "path": download_path}
    # return {"path": download_path}

# if __name__ == '__main__':
#     main("")
