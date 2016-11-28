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
    '''
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
                p2_y = vertices[p2].get('y', 0)'''

    return response['responses'][0]