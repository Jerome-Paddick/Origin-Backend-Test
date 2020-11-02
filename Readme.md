To RUN:

1. docker-compose up -d
2. docker exec -it api sh
3. cd api
4. flask db upgrade
5. Head over to -> http://localhost:5000/api/api_documentation.html
3. Click on api_documentation
6. Create User ( /api/register )
5. Login User ( /api/login ) -> get jwt
6. use jwt to create bond ( POST /api/bonds )
7. use jwt to get bond for user ( GET /api/bonds )

 ---
 Tests
 
 - (after docker image is live and db populated)
 1. docker exec -it api sh
 2. pytest
 
---
Improvements

Obviously this is pretty barebones by design, Im happy with the containerisation, 
the database and test_databse setup, If i had more time I would have liked to add :
 - A central logging system instead of returning errors from api endpoints, 
 - A reverse Proxy such as NGINX
 - auto-scaling, high availability, and a custom url on AWS for example
 - more tests
 
