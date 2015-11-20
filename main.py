#!/usr/bin/env python3

import boto
import config
import hashlib
import random
import string
from boto.s3.key import Key
from flask import Flask, abort, jsonify, request, send_file
from wand.image import Color, Image

app = Flask(__name__)
app.config.from_object(config)


def upload(image):
    s3 = boto.connect_s3()
    bucket = s3.get_bucket(app.config['AWS_BUCKET_NAME'])
    blob = image.make_blob()

    # generate filename from 8 random letters
    filename = ''.join(random.sample(string.ascii_letters, 8))

    # generate filename from image md5
    # h = hashlib.md5()
    # h.update(blob)
    # filename = h.hexdigest()

    key = Key(bucket)

    # key key is image filename, data is blob and headers
    key.key = '%s.%s' % (filename, image.format.lower())
    key.set_contents_from_string(blob, headers={
        'Content-Type': image.mimetype
        })
    key.make_public()
    return key


@app.route('/blend', methods=['POST', 'OPTIONS'])
def blend():
    picture, flag = request.files['picture'], request.files['flag']

    # don't be foolish. please send stuff.
    if not picture or not flag:
        abort(400)

    with Image(file=flag) as foreground:
        with Image(height=foreground.height, width=foreground.width,
                   background=Color('gray80')) as alpha:
            # this will copy the opacity of a 60% opacity image to foreground
            foreground.composite_channel('default_channels', alpha,
                                         'copy_opacity', left=0, top=0)

        with Image(file=picture) as background:
            # rescale flag to be the same size as background
            foreground.resize(height=background.height,
                              width=background.width)

            # blend both images into one
            background.composite_channel('default_channels', foreground,
                                         'blend', left=0, top=0)

            # upload to S3 converted to PNG
            key = upload(background.convert('png'))

    # return json object with url to newly uploaded file
    response = jsonify(url=key.generate_url(app.config['AWS_EXPIRES_IN']))
    response.headers.add('Access-Control-Allow-Origin',
                         app.config['ALLOWED_ORIGIN'])
    response.headers.add('Access-Control-Allow-Credentials',
                         'true')
    return response


if __name__ == '__main__':
    app.run()
