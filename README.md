# 🖊️ Handwriting Extraction AI

A full-stack web application for extracting text from handwritten images using AI vision technology.

## 🎯 Features

- **AI-Powered OCR**: Uses local vision models served by Ollama (default: `llava`)
- **Edge-Friendly Setup**: Run multimodal inference without external API keys
- **Langfuse Observability**: Complete tracing and analytics for AI operations
- **Dynamic JSON Output**: Extracts structured data without predefined schemas
- **No Hallucinations**: Only extracts what's actually visible in the image
- **React Frontend**: Beautiful, user-friendly interface with drag-and-drop upload
- **FastAPI Backend**: High-performance async API

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Ollama** - Local multimodal inference server (default model: `llava`)
- **Langfuse** - AI observability and tracing
- **Python 3.11** - Programming language

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Styling

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- [Ollama](https://ollama.com/) installed and running (`ollama serve`)
- Vision model pulled locally (recommended: `ollama pull llava`)
- Langfuse API Keys (optional, for observability)

## 🚀 Quick Start

### 1. Install & Prepare Ollama

```bash
# Install Ollama from https://ollama.com/download
ollama serve            # starts the local daemon (runs automatically on most systems)
ollama pull llava       # download the multimodal model used by this app
```

Keep the Ollama service running while you use the app.

### 2. Set Optional Environment Variables

Create a `.env` file if you need to override defaults:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llava
LANGFUSE_PUBLIC_KEY=pk-your-langfuse-public-key (optional)
LANGFUSE_SECRET_KEY=sk-your-langfuse-secret-key (optional)
LANGFUSE_HOST=https://cloud.langfuse.com
OLLAMA_TIMEOUT_SECONDS=60
```

### 2. Install Dependencies

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### 3. Run the Application

#### Start Backend (Terminal 1)
```bash
cd backend
python main.py
```
The backend will run on http://localhost:8000

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
The frontend will run on http://localhost:5000

### 4. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 How to Use

1. **Upload Image**: Click "Browse Files" or drag and drop a handwritten image
2. **Supported Formats**: JPG, PNG (PDF support coming soon)
3. **Extract**: Click "Extract Text" button
4. **View Results**: See beautifully formatted JSON output
5. **Copy JSON**: Click the copy button to copy extracted data

## 🔑 API Endpoints

### POST /upload
Upload a handwritten image for text extraction.

**Request**:
- Content-Type: `multipart/form-data`
- Body: File upload

**Response**:
```json
{
  "success": true,
  "filename": "example.jpg",
  "extracted_data": {
    "field1": "value1",
    "field2": "value2"
  },
  "message": "Handwriting extracted successfully"
}
```

### GET /health
Check API health status.

**Response**:
```json
{
  "status": "healthy",
  "agent_initialized": true,
  "ollama_host": "http://localhost:11434",
  "ollama_model": "llava",
  "langfuse_configured": true
}
```

### GET /
API information and available endpoints.

## 🎨 Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── agent.py          # Ollama-powered agent with Langfuse tracing
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.jsx       # Main app component
│   │   └── main.jsx      # Entry point
│   ├── index.html
│   ├── vite.config.js    # Vite configuration
│   └── package.json      # Node dependencies
├── uploads/              # Temporary file storage
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🧠 How It Works

1. **Upload**: User uploads a handwritten image through the React frontend
2. **Backend Receives**: FastAPI receives the file and validates format/size
3. **AI Processing**: Ollama serves the multimodal model (default `llava`)
4. **Text Extraction**: AI reads handwriting and structures data as JSON
5. **Langfuse Tracing**: All operations are traced for observability
6. **Return Results**: Structured JSON is sent back to frontend
7. **Display**: React displays formatted JSON results

## 🔒 Security Features

- File type validation (JPG, PNG only)
- File size limits (10MB max)
- Temporary file cleanup
- Environment variable protection
- CORS configuration

## 🐛 Error Handling

The application handles:
- Unreadable handwriting (marked as null or "unreadable")
- Invalid file formats
- File size violations
- Ollama service not running / model missing
- Network failures
- Langfuse connection issues (graceful degradation)

## 📊 Langfuse Integration

Langfuse provides:
- Complete trace of AI operations
- Performance metrics
- Cost tracking
- Error monitoring
- Analytics dashboard

Access your traces at: https://cloud.langfuse.com

## 🔧 Configuration

### Backend Port
Default: 8000
Change in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)
```

### Frontend Port
Default: 5000
Change in `frontend/vite.config.js`:
```javascript
server: {
  port: YOUR_PORT
}
```

## 🎯 Key Principles

1. **No Hallucinations**: Only extracts visible information
2. **Dynamic Schema**: Adapts to any handwritten form
3. **Generalizable**: Works with any handwriting style
4. **Observable**: Full tracing with Langfuse
5. **User-Friendly**: Simple, beautiful interface

## 🚨 Common Issues

### Agent not initialized
- Verify the Ollama daemon is running (`ollama serve`)
- Pull the configured model (default `ollama pull llava`)
- Restart the backend server after Ollama is ready

### CORS errors
- Ensure backend is running on port 8000
- Check CORS configuration in `main.py`

### Langfuse errors
- Langfuse is optional, the app works without it
- Check your API keys if you want tracing

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using Ollama (llava), Langfuse, and FastAPI**
