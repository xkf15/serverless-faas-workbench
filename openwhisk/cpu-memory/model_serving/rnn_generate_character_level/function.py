# import boto3
import os
import pickle
import numpy as np
import torch
import rnn
import ctypes
import mmap

from time import time

# tmp = "/home/kaifengx/serverless-faas-workbench/dataset/model/"
tmp = "/tmp/dataset/model/"

"""
Language
 - Italian, German, Portuguese, Chinese, Greek, Polish, French
 - English, Spanish, Arabic, Crech, Russian, Irish, Dutch
 - Scottish, Vietnamese, Korean, Japanese
"""

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

def main(event):
    f_s(0)
    latencies = {}
    timestamps = {}
    
    timestamps["starting_time"] = time()

    language = "English" # event['language']
    start_letters = "ABCDEfghijk" # event['start_letters']
    model_parameter_object_key = "rnn_params.pkl" # event['model_parameter_object_key']  # example : rnn_params.pkl
    model_object_key = "rnn_model.pth" # event['model_object_key']  # example : rnn_model.pth
    # model_bucket = event['model_bucket'] #input_bucket
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

    # Check if models are available
    # Download model from S3 if model is not already present
    parameter_path = tmp + model_parameter_object_key
    model_path = tmp + model_object_key

    # start = time()

    # if not os.path.isfile(parameter_path):
    #     s3_client.download_file(model_bucket, model_parameter_object_key, parameter_path)

    # if not os.path.isfile(model_path):
    #     s3_client.download_file(model_bucket, model_object_key, model_path)

    # download_data = time() - start
    # latencies["download_data"] = download_data

    start = time()

    with open(parameter_path, 'rb') as pkl:
        params = pickle.load(pkl)

    all_categories = params['all_categories']
    n_categories = params['n_categories']
    all_letters = params['all_letters']
    n_letters = params['n_letters']

    rnn_model = rnn.RNN(n_letters, 128, n_letters, all_categories, n_categories, all_letters, n_letters)
    rnn_model.load_state_dict(torch.load(model_path))
    rnn_model.eval()

    output_names = list(rnn_model.samples(language, start_letters))

    latency = time() - start
    latencies["function_execution"] = latency
    # timestamps["finishing_time"] = time()

    # return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}
    f_e(0)
    print({"latencies": latencies, "ouput_names": output_names})
    return {"latencies": latencies, "ouput_names": output_names}

if __name__ == "__main__":
    main("")
