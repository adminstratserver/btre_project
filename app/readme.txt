GammaTrades Project (V31)
================================

1. Django project - btre
2. Example using Movies app for testing REST API - Login to generate token, and Post to send trade alerts

-> http http://gammatrades.com/rest-auth/login/ username="tangpd" password="Romans12:1"
<- returns back the token

-> http POST http://127.0.0.1:8000/api/v1/movies/ "Authorization: Token 54923669390a287c9267ace9efc7570f175f5ec2" title="Hello-123" genre="World-123" year=2018
<- send the trade order to IB account

