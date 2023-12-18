curl -v -u "username@email.com:pword" -X PUT http://localhost:8080/api/content/my_command/1 -F 'json={
   "identifier":"c6646f03-588d-479f-96db-33b85bc20bad",
   "stName":"CourseSession",
   "contentHost":"www.mywebsite.com",

}; type=application/json'


curl -v http://localhost:8080/api/launch_battle/150/25/