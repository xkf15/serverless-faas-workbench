# import boto3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import pandas as pd
from time import time
import re
# import io

import ctypes
import mmap

cleanup_re = re.compile('[^a-z]+')
tmp = '/tmp/dataset/'
# tmp = "/home/kaifengx/serverless-faas-workbench/dataset/"

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

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def main(event):
    f_s(0)
    latencies = {}
    timestamps = {}
    
    timestamps["starting_time"] = time()
    
    # dataset_bucket = event['dataset_bucket'] #input_bucket
    dataset_object_key = event['dataset_object_key'] #object_key
    # model_bucket = event['model_bucket'] #output_bucket
    model_object_key = event['model_object_key']  # example : lr_model.pk
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

    # start = time()
    # obj = s3_client.get_object(Bucket=dataset_bucket, Key=dataset_object_key)
    # download_data = time() - start
    # latencies["download_data"] = download_data
    # df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    df = pd.read_csv(tmp + "amzn_fine_food_reviews/" + dataset_object_key)

    start = time()
    df['train'] = df['Text'].apply(cleanup)

    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])

    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression()
    model.fit(train, df['Score'])
    function_execution = time() - start
    latencies["function_execution"] = function_execution

    model_file_path = tmp + "model/" + model_object_key
    joblib.dump(model, model_file_path)

    # start = time()
    # s3_client.upload_file(model_file_path, model_bucket, model_object_key)
    # upload_data = time() - start
    # latencies["upload_data"] = upload_data
    # timestamps["finishing_time"] = time()

    # return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}
    f_e(0)
    return {"latencies": latencies}

# if __name__ == '__main__':
#     main("")
