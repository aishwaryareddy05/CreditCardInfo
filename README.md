# Credit Card Information Extractor 📊💳

[![Download README](https://img.shields.io/badge/Download-README-blue?style=for-the-badge&logo=markdown)](https://raw.githubusercontent.com/your-repo/credit-card-extractor/main/README.md)

## Flow Chart 📈

```mermaid
flowchart TD
    A[Start] --> B{Input Type}
    B --> |URL| C[Fetch with Serper API]
    B --> |PDF| D[Extract Text]
    C --> E[Analyze with Gemini]
    D --> E
    E --> F{Data Available?}
    F --> |Yes| G[Display Structured Results]
    F --> |No| H[Show Error]
    G --> I[Export Options]
    H --> I
    I --> J[End]
```

## System Architecture 🏗️

```mermaid
graph LR
    UI[Streamlit UI] --> API[Serper API]
    UI --> Gemini[Gemini AI]
    UI --> PDF[PDF Processor]
    API --> Gemini
    PDF --> Gemini
    Gemini --> UI
```

## Complete Setup Guide 🛠️

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/your-repo/credit-card-extractor.git
cd credit-card-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 2. Installation

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create `.env` file:

```ini
GEMINI_API_KEY=your_actual_key_here
SERPER_API_KEY=your_actual_key_here
```

### 4. Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Serper
    participant Gemini
    participant PDF

    User->>UI: Select Input Type
    alt URL Input
        UI->>Serper: Fetch URL Content
        Serper-->>UI: Return Page Data
    else PDF Input
        UI->>PDF: Extract Text
        PDF-->>UI: Return Text Content
    end
    UI->>Gemini: Analyze Content
    Gemini-->>UI: Return Structured Data
    UI->>User: Display Results
```

# To run
```python
streamlit run app.py
```

## Troubleshooting 🔧

| Error | Solution |
|-------|----------|
| API Limits | Upgrade Serper/Gemini plan |
| PDF Errors | Use text-based PDFs |
| Model Not Found | Check available Gemini models |

## License 📜

MIT License - Contains [Mermaid.js](https://mermaid.js.org/) diagrams

---

