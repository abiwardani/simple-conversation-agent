# Conversation Agent Web App

This is the web app implementation of a conversational agent or chatbot. The user asks the chatbot a question, and the chatbot searches its knowledge base for the matching answer. Searching is done by comparing the sentence similarity between the user prompt and the questions from the Question-Answer pairs in the knowledge base.

## How to Run
### Build and run from repository
1. Clone the repo
2. Set repo as working directory
3. Set .env file in [/webapp](./webapp)
4. Sample API key is contained in [.env.example](./webapp/.env.example)
5. Build webapp docker image ```docker build -t <webapp-image-tag> ./webapp```
6. Build similarity API docker image ```docker build -r <api-image-tag> ./api```
7. Run webapp docker image ```docker run -d -p 5000:5000 <webapp-image-tag>```
8. Run similarity API docker image ```docker run -d -p <port-number>:5000 <api-image-tag>```
9. The port number of the similarity API should be the same as the port number specified in the .env file.
10. On a browser, open `localhost:5000`

### Alternative: pull from Docker Hub
1. Pull the webapp image ```docker pull abiwardani85/conversation-agent-web-app```
2. Run the webapp image ```docker run -d -p 5000:5000 abiwardani85/conversation-agent-web-app```
3. Pull the similarity API image ```docker pull abiwardani85/conversation-agent-similarity-api```
4. Run the similarity API image ```docker run -d -p <port-number>:5000 abiwardani85/conversation-agent-similarity-api```
5. On a browser, open `localhost:5000`

## How to Use
1. Once the web app is open, users can send a message to the chatbot
2. The chatbot will respond with the suitable answer, or if it is not found, an error message
3. After 5 minutes of inactivity, the chatbot is disconnected

## Contributors
Muhammad Rifat Abiwardani (13519205@std.stei.itb.ac.id)

## Project Status
Complete
