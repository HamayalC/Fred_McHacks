import httplib, urllib, base64, json, ast, cv2


cam = cv2.VideoCapture(0)
frame = cam.read()[1]
cv2.imwrite(filename='img.jpg', img=frame)
cam.release()

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'c5990bc6c575435681a2c288f685fe44',
}

params = urllib.urlencode({
})

# Replace the example URL below with the URL of the image you want to analyze.
req_body = open('img.jpg', 'rb').read()


import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
    #   URL below with "westcentralus".
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body=req_body, headers=headers)
    response = conn.getresponse()
   # data = response.read()
   # parsed = json.loads(data)


    data = response.read()

	
    b = data.decode("utf-8") #bytes to string conversion
    c = ast.literal_eval(b) #string to list conversion
   

    happy = (c[0]['scores']['happiness']) #parsing
    sad = (c[0]['scores']['sadness'])
    angry = (c[0]['scores']['anger']) 

    if happy>sad and happy>angry:
	ser.write("a")
	print("Happy")
    elif sad>angry:
	ser.write("d")
	print("Sad")
    else:
	ser.write("s")
	print("Angry")


    #print (json.data(parsed, sort_keys=True, indent=2))
    #conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
