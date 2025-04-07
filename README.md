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
OPENAI_API_KEY=your_openai_api_key
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
.
├── agentchat/
│   ├── __init__.py
│   ├── api/
│   │   ├── endpoints.py       # API endpoints
│   │   ├── schema.py          # Pydantic models for request/response
│   ├── agents/
│   │   ├── agent.py           # Agent setup with OpenAI GPT
│   │   ├── chatbot.py         # Chatbot state graph
│   │   ├── tools.py           # Custom tools for the agent
│   ├── core/
│   │   ├── settings.py        # Configuration and logging
│   ├── app.py                 # FastAPI application entry point
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for the API
├── README.md                  # Project documentation
```

## Key Components

### 1. **Database Integration**

The application uses PostgreSQL for persistent memory. The database schema is set up automatically when the application starts.

### 2. **Chatbot**

The chatbot is implemented using a state graph (`StateGraph`) and integrates OpenAI's GPT model for generating responses.

### 3. **Tools**

Custom tools can be added to extend the chatbot's functionality. For example, a `multiply_numbers` tool is included as a demonstration.

### 4. **API Endpoints**

- **POST /message**: Accepts a user message and returns a chatbot response.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
