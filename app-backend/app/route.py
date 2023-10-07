from flask import (
    Flask, request, make_response, Blueprint, flash
)
app = Flask()

@app.route('/capture_images', methods=['GET'])
def capture_images():

    images = []
    return make_response("Not implemented", 501)