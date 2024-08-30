## Back-End Plan (FastAPI)

### 1. User Authentication (Sign Up, Login, Logout)

- **Sign Up**:
  - **Endpoint**: `POST /signup`
  - **Functionality**: Create new user records in the PostgreSQL database with hashed passwords.
  - **Future Consideration**: Extend the system to support OAuth (Google, Firebase).

- **Login**:
  - **Endpoint**: `POST /login`
  - **Functionality**: Validate user credentials, return JWT for session management.

- **Logout**:
  - **Endpoint**: Can be handled on the client-side by simply clearing the JWT token.

### 2. Student Dashboard

- **Endpoint**: `GET /student/{id}`
  - **Functionality**: Retrieve and display student’s profile details.
  - **Profile Photo Upload**:
    - **Endpoint**: `POST /student/{id}/upload-photo`
    - **Functionality**: Handle image uploads, save them on the server, and store the file path in the database.

### 3. Student Course Page

- **Course Information**:
  - **Endpoint**: `GET /student/{id}/courses`
  - **Functionality**: Return a list of courses the student is enrolled in.

- **Music File Upload**:
  - **Endpoint**: `POST /student/{id}/courses/{course_id}/upload`
  - **Functionality**: Handle music file uploads, store the files on the server or cloud storage, and store the file metadata in the database.

- **File Management**:
  - **Endpoint for re-upload**: `PUT /student/{id}/courses/{course_id}/upload/{file_id}`
  - **Endpoint for deletion**: `DELETE /student/{id}/courses/{course_id}/upload/{file_id}`

### 4. Teacher Dashboard

- **Assigned Courses**:
  - **Endpoint**: `GET /teacher/{id}/courses`
  - **Functionality**: List all courses assigned to the teacher with associated student information.

- **Student Submissions**:
  - **Endpoint**: `GET /teacher/{id}/courses/{course_id}/students`
  - **Functionality**: Retrieve and display all student submissions for a particular course.

---

## Database Considerations

**PostgreSQL** is recommended because it’s a powerful, open-source relational database that can handle the structured data required for user profiles, course details, and file metadata. PostgreSQL’s extensibility, such as support for JSON fields, offers flexibility if unstructured data needs to be handled in the future.

- **User Table**: Store user details (name, email, password hash, role, etc.).
- **Course Table**: Store course-related information (name, schedule, instrument, teacher, etc.).
- **File Metadata Table**: Store references to uploaded music files (file path, uplo