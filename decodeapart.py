import base64
import array

testb64 = '"MTQ0IDAyMgA='
decodage = base64.b64decode(testb64)
test = decodage.decode("utf-8")
print(test)
