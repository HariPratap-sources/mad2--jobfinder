## jobfinder-mad2
# How to run project
### Create virtual environment
```terminal
python -m venv .venv
```
### open venv in terminal
```
.\.venv\Scripts\activate
```
### install all requirements
```
pip install -r requirements.tx
```
### install vite
### go to frontend folder
```
cd frontend
```
### then run code
```
npm install
```
### then run code
```
npm run dev
```
### open new terminal, go to virtual environment if automatic open, OK if not, run code (.\.venv\Scripts\activate) after that run code
```
cd backend
```
### then run app.py after that server run
```
pyhton app.py
```

### for background tasks
open new terminal and go backend folder using (cd backend) command after that run command for ### celery beat
```
celery -A app.celery beat --loglevel=info
```

###for celery worker
```
celery -A app.celery worker --pool=solo --loglevel=info
```

# and run Redis server on docker

