# Agentic Chat with PostgreSQL Memory

![image](https://github.com/user-attachments/assets/6fdb0107-72ed-45ab-bebd-b37e8bc11f01)

This project demonstrates how to integrate PostgreSQL for persistent memory in a FastAPI-based chatbot application. It uses OpenAI's GPT model and provides a modular architecture for extending functionality with tools.

## Features

- **FastAPI**: A modern web framework for building APIs.
- **PostgreSQL**: Persistent storage for chat memory.
- **OpenAI GPT Integration**: Uses OpenAI's GPT model for generating responses.
- **Tool Integration**: Extendable with custom tools for additional functionality.
- **Dockerized**: Easily deployable with Docker Compose.

## Prerequisites

- Docker and Docker Compose installed.
- OpenAI API key.
- Python 3.10+ (for local development).

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ThanAid/Agentic-Chat-PostgreSQL-Memory.git
cd Agentic-Chat-PostgreSQL-Memory
```

### 2. Create a `.env` File

Create a `.env` file in the root directory with the following variables:

```env
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
GEMINI_API_KEY=your_gemini_api_key
MODEL_NAME=gpt-4o-mini (for example)
```

### 3. Start the Application

Run the following command to start the application using Docker Compose:

```bash
docker-compose up --build
```

This will start the PostgreSQL database and the FastAPI application.

### 4. Access the Application

- API Documentation: [http://localhost/docs](http://localhost/docs)
- Application runs on port `80`.

## Project Structure

```
agentchat
├── __init__.py
├── __pycache__
├── agents
│   ├── __init__.py
│   ├── chain.py
│   └── chatbot.py
├── api
│   ├── __init__.py
│   ├── endpoints.py
│   ├── file_handler
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── file_processor.py
│   │   ├── response_serializer.py
│   │   └── validators.py
│   └── schema.py
├── app.py
└── core
    └── settings.py
```

## Key Components

### 1. **Database Integration**

The application uses PostgreSQL for persistent memory. The database schema is set up automatically when the application starts.

### 2. **Chatbot**

The chatbot is implemented using a state graph (`StateGraph`) and integrates Google Gemini model for generating responses.

It is set to function as AI personal trainer.

### 4. **API Endpoints**

- **POST /message**: Accepts a user message and returns a chatbot response.
- **POST /upload**: Accepts a user uploaded txt file and inserts it into the chat context.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
