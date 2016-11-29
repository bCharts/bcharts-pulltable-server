from googleapiclient import discovery
import base64
import json
import cv2

def analyze_image(bImage):
    ret, buf = cv2.imencode('.PNG', bImage)

    service = discovery.build('vision', 'v1', developerKey='AIzaSyDMgrNdPdZQCWHA4V-9qhPyGUVVqb2DcaA')
    image_content = base64.b64encode(buf)
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': 1
            }]
        }]
    })

    response = service_request.execute()

    return response['responses'][0]