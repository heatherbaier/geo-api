rm lambda_function.zip
cd package                                                       
zip -r ../lambda_function.zip .
cd ..
zip lambda_function.zip lambda_function.py
aws s3 cp lambda_function.zip s3://geo-wm               