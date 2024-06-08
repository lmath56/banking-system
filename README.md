<br>

# Banking System
This repository contains the files for a Banking system for Fontys Semester 2 Programming.

<br>

## The Task
#### ***Individual semester assignment***
Over the course of this semester you are expected to design an application that can be deployed on a modern infrastructure. Your application should be a CRUD-application[^1] consisting of the following parts:

- A database (hosted by a client-server DBMS like MySQL, PostgreSQL, Microsoft SQL Server, etc.)
- The application server (where your “API runs”, also known as “the backend”)
- One or multiple frontends with which the user interacts and that in turn communicates with the application server. Examples of frontends could be a webserver that presents a user interface, a mobile application, a command-line tool, etc.

The purpose of the application is something you can think of yourself. Some of the demo code shows a simple, incomplete student-management system. Other examples could be: a car rental system, a blogging system, a twitter-like (X-like?) application, etc.; the possibilities are endless. 

Your application must implement a few criteria:

- The parts mentioned above should be clearly separated and independently runnable (for example in different containers/on different systems).
- The part of the application running on the application server should be stateless; each request it receives should be processable without knowledge of any preceding requests. 
- The system should be secure, so think about things like SQL-injection attack prevention.
- There should be at least 2 types of frontends. For example, a web frontend for interactive use and a commandline-tool for something like retrieving statistics, batch processing, etc. The frontend should ONLY communicate with the application server through the API.
- There should be logging on at least the application server.

We expect you to follow an API first approach. Before proceeding to a next step in the outline below, make sure to ask for feedback from your teacher and a final agreement from him/her before moving on. The general order in which you go about this assignment is:

1. Define the application. Describe what its purpose is, who will be its target audience, who will be using which parts of the system and what the functionalities will be that it offers. This means defining and documenting the functional requirements.
2. Translate the functional requirements into a technical design. This includes:
   a. creating the API according to the OpenAPI specification – you can do this in either YAML or JSON format, but make sure it is correct and can be interpreted by tools that support this specification;
   a. creating diagrams according to the C4 model breaking down the structure of your application and its components at different levels.
3. Implement the application and create a POC (proof of concept) to demonstrate it running.


**Optional (e.g. for Advanced on developmental scale)**

4. Create background tasks that either run continuously or periodically. For example: backups of the database, generating statistics, database cleanup, log rotation, etc.
5. Implement user-based logins. You can follow different approaches for this:
   a. Store the credentials (username/password) in your own database. Think about the security risks involved with this and implement appropriate ways of doing this (hashing, salting, PBKDF, etc.), or
   b. Use an identity provider like Google Identity, Facebook, Microsoft, etc. to prevent having to store password (hashes) in your own database.
6. Add different user roles. For example “normal” users and administrative users.
7. Create the infrastructure where your application runs and host your application so it is secure, highly available and scalable. Infrastructures you can think of are:
   a. Netlab
   b. Docker swarm
   c. Kubernetes
   d. A cloud platform (like Azure)


[^1]: CRUD refers to the four basic operations a software application should be able to perform – Create, Read, Update, and Delete. In such apps, users must be able to create data, have access to the data in the UI by reading the data, update or edit the data, and delete the data. (<https://www.freecodecamp.org/news/crud-operations-explained/>)

<br>

## Chosen Project
The goal of this project is to design and build a prototype banking system which contains all of the features listed above, including the advanced optional tasks.

The back end / application server will be written in Python. The SQLAlchemy database will run separately. The front ends must access the front end via an API using the OpenAPI 3.0 standard, exposed by Connexion. The system must support logins and have an admin role. There will be a GUI front end built using the TKinker package which is used for online banking. Administration of the system will be via a CLI tool that allows management of the system. 


<br>

## Development Timeline
|**When**|**What**|
| :- | :- |
|**Formative indication 1**|<p>- Application definition</p><p>- Functional requirements</p>|
|**Formative indication 2**|<p>- API specification</p><p>- Skeleton code</p><p>- (Informal) models</p>|
|**Formative indication 3**|<p>- Fully working draft version of application</p><p>- Complete documentation</p><p>- Models adhering to C4 model</p>|
|**Final indication / integral assessment**|Final version of everything mentioned under formative indication 3. In this final version, you have processed all feedback you received over the course of the semester. Also clearly document how you processed the feedback and how this is visible in this final delivery.|

<br>

## Screenshots
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

<br>

## Configuration
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

<br>

### Email Configuration
In order for OTP to work, an SMTP server is needed

```ini
[smtp]
enabled=True
host=
port=
username=
password=
sender_name=Luxbank
sender_email=
```

<br>

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

<br>

## Project status
This project is in the final stages of development before being submitted.
