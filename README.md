1. Create mysql database named shop

	`create database shop`

2. Edit line 17 in app.py specifying database details

3. Create a migration repository with the init subcommand

	`python app.py db init`

4. Create an automatic migration script using db migrate command

	`python app.py db migrate -m "initial migrate"`

5. Apply migration script to the database using the db upgrade command 

	`python app.py db upgrade`

6. Run the server.

	`python app.py runserver`

Access app at http://127.0.0.1:5000/
