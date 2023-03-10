#Change directory to api folder (rest_api)
#Run on VS Code with venv environment. Or install the below given python modules
pip install fastapi
pip install "uvicorn[standard]"
pip install pyrebase4

#Run your api file
uvicorn api:app --host 0.0.0.0 --port 8000

#Install node js. Open a new terminal and change directory to nuxt app folder (quiz_builder)
#Deploy the nuxt app
npm run dev