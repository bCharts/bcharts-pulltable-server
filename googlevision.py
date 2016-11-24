from googleapiclient import discovery
import base64
from PIL import Image, ImageDraw
from io import BytesIO
import json

def analyze_image(bImage):
    service = discovery.build('vision', 'v1', developerKey='AIzaSyCTnZcKIkOQkuYyiACDmnmcJU1zoEJ69Zs')
    image_content = base64.b64encode(bImage)
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': 1
            }, {
                'type': 'LOGO_DETECTION',
                'maxResults': 1
            }, {
                'type': 'IMAGE_PROPERTIES',
                'maxResults': 1
            }]
        }]
    })

    response = service_request.execute()

    trg_image = Image.open(BytesIO(bImage)).convert('RGB')
    draw = ImageDraw.Draw(trg_image)

    textAnnotations = response['responses'][0].get('textAnnotations')
    if textAnnotations is not None:
        for i in range(1, len(textAnnotations)):
            vertices = textAnnotations[i]['boundingPoly']['vertices']
            for p1 in range(len(vertices)):
                if p1 == len(vertices) - 1:
                    p2 = 0
                else:
                    p2 = p1 + 1
                p1_x = vertices[p1].get('x', 0)
                p1_y = vertices[p1].get('y', 0)
                p2_x = vertices[p2].get('x', 0)
                p2_y = vertices[p2].get('y', 0)
                draw.line((p1_x, p1_y, p2_x, p2_y), fill=(0, 255, 0), width=3)

    logoAnnotations = response['responses'][0].get('logoAnnotations')
    if logoAnnotations is not None:
        for i in range(0, len(logoAnnotations)):
            vertices = logoAnnotations[i]['boundingPoly']['vertices']
            for p1 in range(len(vertices)):
                if p1 == len(vertices) - 1:
                    p2 = 0
                else:
                    p2 = p1 + 1
                p1_x = vertices[p1].get('x', 0)
                p1_y = vertices[p1].get('y', 0)
                p2_x = vertices[p2].get('x', 0)
                p2_y = vertices[p2].get('y', 0)
                draw.line((p1_x, p1_y, p2_x, p2_y), fill=(255, 0, 0), width=3)

    return json.dumps(response['responses'][0]), trg_image