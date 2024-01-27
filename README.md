# STUDENT MANAGEMENT API

This API is responsible for managing the registration of students and their guardians to the system, validating the registration of students to unique groups.

## 🛠 Used technology

- **Programming language:** Python
- **Web framework:** FastAPI
- **Database:** PostgreSQL
- **Testing:** Unittest.
- **Web server:** Uvicorn
- **Data validation:** Pydantic

## 📚 Project Organization

The development of the project follows a layer-based architecture. The code is organized as follows:

- `src/`: Where the main source code of the project is stored.
  - `controllers/`: Directory where input requests are processed.
  - `crud/`: Organize, store, and execute database operations.
  - `database/`: Directory where database connections are controlled.
  - `enums/`: Define the limited sets of options or states that can be used.
  - `models/`: The data structures that represent entities in the application are defined.
  - `schemas/`: Directory used to define the structure, validation and serialization of the data.
  - `services/`: Directory where the business logic is grouped and processed.
  - `main.py`: Main entry point.
  - `settings.py`: File where the microservice configurations are managed.
- `test/`:Where the project tests are executed.
- `.gitignore/`: Specify which files should be ignored by Git.
- `README.md/`: Provides information and documentation about the project.
- `requirements.txt/`: Used to specify project dependencies.

## 🏁 Endpoints

This Notion describes the processes and analyses carried out, as well as the respective technical documentation.

https://romantic-ghoul-576.notion.site/Caso-te-cnico-Backend-Developer-Crack-The-Code-234ffe0261474b59b18ddf272a873260

## ▶️ Fast configuration and execution.

1. Clone this repository
   ```bash
   https://github.com/Walbert29/student-management.git
   ```
2. Create and activate a virtual environment

   **Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server

   **Using the main entry point:**

   ```bash
   cd src/
   python main.py
   ```

5. Download the template designed for student enrollment

   ```bash
    GET
    /template/list/templates
   ```

6. There are 2 templates.
   Template for student enrollment.
   Template for updating student and guardian data.

7. Select the template with the Endpoint:
   ```bash
    GET
    /template/template/{template_id}
   ```

## ▶️ Run test

### Enrollemt

```bash
cd test/
python -m unittest ./enrollment.py
```

### Course

```bash
cd test/
python -m unittest ./course.py
```

### Group

```bash
cd test/
python -m unittest ./group.py
```

### Room

```bash
cd test/
python -m unittest ./room.py
```

### Student

```bash
cd test/
python -m unittest ./student.py
```

### Teacher

```bash
cd test/
python -m unittest ./teacher.py
```

## 📃Versions

### v0.1.0

#### New Features

- Creation of the main function (Enrollment of students).
- Creation of data update system for students and guardians.
- Creation of users (Students, tutors, teachers).
- Creation of groups, classrooms and courses.

### v0.2.0

#### New Features

- Creation of deletion flows for groups, courses and rooms.
- Docker implementation.

#### Enhancements

- Added more unit tests to validate correct execution of the code.
- Improvements in the validation of errors in student enrollment.
