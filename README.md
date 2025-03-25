# docker-with-postgres (andalsoFastAPI...)

What started as a testing repo has started to evolve... The initial idea for this repo was just to knock the rust off of my Docker/Postgres knowledge. The project now has FastAPI with a number of functioning endpoints (including passwordless authentication!).

## First time Spinning Everything Up (Mac... I don't know Windows)

Here’s how to get everything running. If something isn’t working, try checking the container logs or verifying that Docker is running properly.

### Spinning Up Docker

I believe that you need to have both Docker and Docker Compose installed on your machine, as well as the **Docker Desktop app**. If installed, open the Docker Desktop app and then run the following command in a terminal window:

```
docker compose up --build
```

This will start all necessary services.

#### Troubleshooting

- Check running containers:  
  `docker ps`
- View logs for a specific service (e.g., Postgres):  
  `docker logs postgres_db`
- Restart everything if needed:  
  `docker compose down && docker compose up --build`
- Use Docker Desktop if you like GUI's

---

## Authentication Flow and Requirements

### (Requires All Docker Containers are Running)

#### Step-By-Step

(It is easiest to handle most of this testing through the Swagger UI)

1. Register new user with a POST to **/users/register**
2. Request an auth code with the newly registered email using a POST to **/auth/request-code**
   - As of 3/24/25, I have disabled the function that sends the auth code via email. I added a print function that displays the code in the terminal. Copy the code from there.
3. To verify the copied auth code, use a POST to **/auth/verify-code** and send both the email associated with the code, and the code itself
   - If successfull, copy the JWT token that is returned.
4. In a terminal window, send a curl request with the following structure:

```
curl -X GET "http://localhost:8000/offices/protected-route"
```

This should spit out a unauthorized related error. Now, try adding an **'Authorization: bearer <token>** header to the curl request:

```
curl -X GET "http://localhost:8000/offices/protected-route" -H "Authorization: Bearer <your.token.here.should.look.like.string.of.random.characters>"
```

**/offices/protected-route** is, well, a protected route. If everything worked well, you should get a message showing you're authenticated and successfully ran a GET on the protected route!

---

## Adding New Data Tables

Add a new file to the **app/models/sqlalchemy** directory. Match the naming convention. Reference existing files for structure. If you need something specific, check out [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/).

---

## Writing New Endpoints

### Endpoints for New Data Table

If you're writing endpoints for a newly created table, create a new router.

1. Create a new routers file in **app/routers** and match the naming convention. Follow structure of existing router files.
2. Include the router in main.py by:
   - Importing the router from **app/routers** (currenly main.py line 4...)
   - Calling a new **app.include** function:
     - Arg 1: the new and imported router
     - Arg 2: your chosen endpoint prefix
     - Arg 3: tags are the title seen for the section in Swagger UI
3. Write Pydantic Models in **app/models/pydantic** (see details below).
4. Write routes in **app/routers/<new-data>\_routers.py**
5. Separate route specific functionality to a **<new-data>\_queries.py** file in the **app/queries** directory.

---

## Write Pydantic Models

Coming soon...

---

## Writing new routes

Coming soon...

---

## Logging Into pgAdmin

Once all Docker containers are running, open your browser and go to:

[http://localhost:5050](http://localhost:5050)

### Login Credentials

- **Email**: `admin@admin.com`
- **Password**: `admin`

### Registering the Database

1. Right-click on **"Servers"**, then click **"Register" → "Server"**.
2. Go to the **General** tab:
   - **Name**: `Postgres DB`
3. Go to the **Connection** tab:
   - **Host name/address**: `db`
   - **Username**: `myuser`
   - **Password**: `mypassword`
4. Click **Save**, and you should be connected!

---

# Markdown syntax guide for future README additions...

## Headers

# This is a Heading h1

## This is a Heading h2

###### This is a Heading h6

## Emphasis

_This text will be italic_

**This text will be bold**

## Lists

### Unordered

- Item 1
- Item 2
- Item 2a
- Item 2b
  - Item 3a
  - Item 3b

### Ordered

1. Item 1
2. Item 2
3. Item 3
   1. Item 3a
   2. Item 3b

## Images

![This is an alt text.](/image/sample.webp "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
> > Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Tables

| Left columns | Right columns |
| ------------ | :-----------: |
| left foo     |   right foo   |
| left bar     |   right bar   |
| left baz     |   right baz   |

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
