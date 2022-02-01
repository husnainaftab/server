from flask import Flask, request, jsonify
from main import get_results
import boto3
import uuid


app = Flask(__name__)

@app.route("/signed-upload-path", methods=["GET"])
def signed_upload_path():
    name = str(uuid.uuid4()) + ".jpeg"
    url = boto3.client('s3').generate_presigned_url(
    ClientMethod='put_object', 
    Params={'Bucket': 'drbd-upload-images', 'Key': name , "ContentType" : "image/jpeg"},
    ExpiresIn=3600)

    return jsonify(
        url= url,
        name=name
    )

@app.route("/", methods=["POST"])
def verify_image():
    req = request.get_json()
    image_path = req["image_path"]
    x = get_results(image_path=image_path)
    return x



if __name__ == '__main__':
    app.run()




