# Android APK Explorer

![android](https://baswijdenes.com/wp-content/uploads/2016/05/android-banner.png)

An API to explore Android applications uploaded by Creators.

## Informations

### Installation (Docker)  
In the `apk_explorer` folder run the following command :  
`docker-compose up`  


The application runs at `http://127.0.0.1:8000`.  

### Browse the API
- A Postman collection `apk-explorer.postman_collection.json` with all the API endpoints is available in the root folder.
- The database already contains 2 test users, each of them having uploaded one application.
- The API has a token based authentication. Except for GET endpoints, a token must be provided for all the others. This token can be retrieved with the `/api-token-auth/` endpoint, providing the user's username and password.

### Running tests
Run the following command:  
`python manage.py test`

### Known limitations
- The API runs on a SQLite database which is the default database for Django. As SQLite has sizes limits (maximum number of database, columns, length of string, ...), the number of creators and applications might be limited.
  

## Explanation
- For this project I tried to keep things clean and simple, by using Django's built-in features as possible.
- I used Androguard to extract APK files' content, as it is quite simple to use and the documentation is comprehensive.
- For the views, as it is my first use of Django (I have experience with Laravel), I found the more verbose APIView class easier to use over the ViewSet class. It gaves me a better understanding of the application flow.
- I choosed to use a token based authentication for non-GET endpoints because of its simplicity and efficiency.
- As mentioned before, the application runs on a SQLite database. I choosed to keep the Django's default engine as it is sufficient for a project of this size.
- I struggled a bit to have the right representation of models. When applications were displayed, the creator field also contained the list of its applications, because the creator model should be represented with its applications' list. I finally created separated serilaizers to display applications and creators differently depending on their nested representation or not.
- For testing, I tried to find a way to generate a fake APK file to test the upload endpoint. I didn't find a solution in the end, so I managed to include a real APK file (in `explorer/apk_examples`).
- A `docker-compose` file was not needed here, as the SQLite database in embedded in the project. But I still included one to keep the installation simple by running only the `docker-compose up` command to build image, create and run a container.