import requests
image_path = 'your_image.jpeg'
data = {'file': open(image_path, 'rb')}
response = requests.post('https://extract-date-receipt.herokuapp.com/extract_date', files=data)
print(response.json())
