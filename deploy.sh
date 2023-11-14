~/openwhisk/bin/wsk action delete chameleon -i
~/openwhisk/bin/wsk action delete videoprocessing -i
~/openwhisk/bin/wsk action delete imageprocessing -i
~/openwhisk/bin/wsk action delete floatoperation -i
~/openwhisk/bin/wsk action delete matmul -i
~/openwhisk/bin/wsk action delete linpack -i
~/openwhisk/bin/wsk action delete pyaes -i
~/openwhisk/bin/wsk action delete modelserving -i
~/openwhisk/bin/wsk action delete modeltraining -i
~/openwhisk/bin/wsk action delete rnnserving -i

~/openwhisk/bin/wsk action create chameleon --docker andersonandrei/python3action:chameleon ~/serverless-faas-workbench/openwhisk/cpu-memory/chameleon/function.py -m 512 -t 300000 -i
# ./bin/wsk action invoke chameleon -p num_of_rows 2000 -p num_of_cols 200 -p metadata deadbeef  --result -iv
# 
~/openwhisk/bin/wsk action create videoprocessing --docker kaifengx/kaifengx-functionbench:video_processing ~/serverless-faas-workbench/openwhisk/cpu-memory/video_processing/function.py -t 300000 -i 
# ./bin/wsk action invoke videoprocessing -i --result
# 
~/openwhisk/bin/wsk action create imageprocessing --docker kaifengx/kaifengx-functionbench:image_processing ~/serverless-faas-workbench/openwhisk/cpu-memory/image_processing/function.py -t 300000 -i
# ./bin/wsk action invoke imageprocessing -iv --result
# 
~/openwhisk/bin/wsk action create floatoperation ~/serverless-faas-workbench/openwhisk/cpu-memory/float_operation/function.py -t 300000 -i
# ./bin/wsk action invoke floatoperation -p n 10000000 -p metadata deadbeef -iv --result
# 
# 
~/openwhisk/bin/wsk action create matmul --docker andersonandrei/python3action:matmul ~/serverless-faas-workbench/openwhisk/cpu-memory/matmul/function.py -m 512 -t 300000 -i
# ./bin/wsk action invoke matmul -p n 1000 -p metadata deadbeef -iv --result
# 
~/openwhisk/bin/wsk action create linpack --docker andersonandrei/python3action:linpack ~/serverless-faas-workbench/openwhisk/cpu-memory/linpack/function.py -m 512 -t 300000 -i
# ./bin/wsk action invoke linpack -p n 1000 -p metadata deadbeef -iv --result
# 
~/openwhisk/bin/wsk action create pyaes --docker andersonandrei/python3action:pyaes ~/serverless-faas-workbench/openwhisk/cpu-memory/pyaes/function.py -m 512 -t 300000 -i
# ./bin/wsk action invoke pyaes -p length_of_message 1000 -p num_of_iterations 1000 -p metadata deadbeef -iv --result
# 
~/openwhisk/bin/wsk action create modelserving --docker kaifengx/kaifengx-functionbench:video_processing ~/serverless-faas-workbench/openwhisk/cpu-memory/model_serving/ml_video_face_detection/function.py -t 300000 -i
# ./bin/wsk action invoke modelserving -iv --result
# 
~/openwhisk/bin/wsk action create modeltraining --docker kaifengx/kaifengx-functionbench:video_processing ~/serverless-faas-workbench/openwhisk/cpu-memory/model_training/function.py -t 300000 -i
# ./bin/wsk action invoke modeltraining -p dataset_object_key reviews10mb.csv -p model_object_key lr_model.pk -iv --result
# 
~/openwhisk/bin/wsk action create rnnserving --docker kaifengx/kaifengx-functionbench:rnn_generate_character_level ~/serverless-faas-workbench/openwhisk/cpu-memory/model_serving/rnn_generate_character_level/function.py -t 300000 -i
# ./bin/wsk action invoke rnnserving -iv --result
