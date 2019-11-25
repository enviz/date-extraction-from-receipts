import requests
image_path = 'receipt.jpeg'
data = {'file': open(image_path, 'rb')}
response = requests.post('https://extract-date-receipt.herokuapp.com/extract_date', files=data)
print(response.json())
