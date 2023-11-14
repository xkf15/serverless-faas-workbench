# import boto3
# import uuid
from time import time
import cv2

tmp = "/tmp/dataset/"
# tmp = "/home/kaifengx/serverless-faas-workbench/dataset/"

FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2

import ctypes
import mmap

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

def video_processing(object_key, video_path, model_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+'-detection.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    face_cascade = cv2.CascadeClassifier(model_path)

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            #print("Found {0} faces!".format(len(faces)))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            out.write(frame)
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
    
    timestamps["starting_time"] = time()
    
    # input_bucket = event['input_bucket']
    object_key = "SampleVideo_1280x720_10mb.mp4" # event['object_key']
    # output_bucket = event['output_bucket']
    model_object_key = "haarcascade_frontalface_default.xml" # event['model_object_key'] # example : haarcascade_frontalface_default.xml
    # model_bucket = event['model_bucket'] # input_bucket as well
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

    # download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)
    # model_path = tmp + '{}{}'.format(uuid.uuid4(), model_object_key)
    download_path = tmp + "video/" + object_key
    model_path = tmp + "model/" + model_object_key

    # start = time()
    # s3_client.download_file(input_bucket, object_key, download_path)
    # s3_client.download_file(model_bucket, model_object_key, model_path)    
    # download_data = time() - start
    # latencies["download_data"] = download_data

    function_execution, upload_path = video_processing(object_key, download_path, model_path)
    latencies["function_execution"] = function_execution

    # start = time()
    # s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])
    # upload_data = time() - start
    # latencies["upload_data"] = upload_data
    # timestamps["finishing_time"] = time()

    # return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}
    f_e(0)
    return {"latencies": latencies}

if __name__ == '__main__':
    main("")
