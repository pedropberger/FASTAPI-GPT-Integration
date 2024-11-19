# FastAPI GPT Integration

This project is a Python API built with FastAPI that integrates with a language model to process messages, store results in a database, and return the processed response. The API accepts a JSON payload, sends the data to an external endpoint, saves the results in a SQLite database, and returns the generated content.

---

## 📋 Prerequisites

1. **Python 3.11 or higher**
2. **Docker (optional for containerized execution)**
3. **Environment variables**:
   - `API_KEY`: Your external API key.
   - `ENDPOINT`: The external API endpoint URL.

Make sure to create a `.env` file in the project root with the following format:

```env
API_KEY=your_api_key
ENDPOINT=https://your-api-endpoint.com
```

---

## 🚀 How to Run

### 1. Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pedropberger/FASTAPI-GPT-Integration.git
   cd your-repo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the application:
   - Visit [http://localhost:8000](http://localhost:8000) to view the endpoints.
   - The interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

### 2. Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t fastapi-gpt-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env fastapi-gpt-app
   ```

3. The API will be available at [http://localhost:8000](http://localhost:8000).

---

## 📂 Project Structure

```
.
├── Dockerfile           # Docker configuration
├── main.py              # Main FastAPI application code
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (do not commit this file!)
└── README.md            # Project documentation
```

---

## 🛠️ Features

- Accepts structured messages as a payload.
- Sends data to a language model via an external API.
- Stores responses in a local SQLite database.
- Returns only the generated content from the model.

---

## 📦 Database

The project uses SQLite to store the following information:

- Sent message (`message`)
- Response ID (`completion_id`)
- Model used (`model_used`)
- Timestamp of creation (`created_timestamp`)
- Generated content (`content`)
- Token usage:
  - Prompt tokens (`prompt_tokens`)
  - Completion tokens (`completion_tokens`)
  - Total tokens (`total_tokens`)

The database is automatically initialized on the first run.

---

## 📝 Usage Examples

### Example Payload:

```json
{
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant helping people find information."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate an example text block for a prompt."
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}
```

### API Response:

```json
{
  "content": "This is an example of a generated text block for a prompt."
}
```

### Python request exemple:

```python
import requests

url = "http://127.0.0.1:8000/process-payload/"
headers = {"Content-Type": "application/json"}

payload = {
    "messages": [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant helping people find information."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate an example text block for a prompt."
                }
            ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    print("Content:", response.json()["content"])
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

---

## ⚠️ Important Notes

1. **.env Security**: Never commit your `.env` file with sensitive API keys to GitHub.
2. **SQLite for Testing**: For production, consider using a more robust database like PostgreSQL or MySQL.
3. **Token Limits**: Ensure that `max_tokens` values are within your model's limits.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the project.
2. Create a new branch:
   ```bash
   git checkout -b my-feature
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add my new feature"
   ```
4. Push your branch to your fork:
   ```bash
   git push origin my-feature
   ```
5. Open a Pull Request on the main repository.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

### Author

Developed with ❤️ by [Pedro](https://github.com/pedropberger).
