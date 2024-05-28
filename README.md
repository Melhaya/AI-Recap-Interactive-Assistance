
# ARIA (AI Recap Interactive Assistant)

ARIA is an interactive AI-powered assistant designed to enhance learning experiences by generating relevant questions from uploaded learning materials. The assistant uses OpenAI's models to provide feedback on answers, allowing users to engage deeply with their study content.

## Features

- **AI-Powered Question Generation**: Generates insightful questions based on the provided text.
- **Interactive Feedback**: Offers real-time feedback on user answers to foster learning.
- **Progress Tracking**: Visually tracks and displays user progress through a progress bar.
- **Adaptive Questioning**: Allows users to skip questions or proceed to new ones as desired.
- **Customizable Question Count**: Users can choose how many questions they want to answer in a session.

## Installation

To set up ARIA, you'll need Python and pip installed on your machine. Follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Melhaya/AI-Recap-Interactive-Assistance.git
   cd AI-Recap-Interactive-Assistance
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running ARIA, you must configure the application by setting up the necessary API keys in a `.env` file, and model parameters in `config.py`.

- **OpenAI Key**: Set your OpenAI API key in `.env`.
- **AI Models**: Configure the AI models in `config.py` with their corresponding keys as required.

## Usage

To start ARIA, run the main script:

```bash
python main.py
```

or run the streamlit app directly from your terminal:

```bash
streamlit run main.py 
```

The application interface will open in your default web browser where you can upload your learning materials and start your interactive recap session.

## Contributing

Contributions to ARIA are welcome!

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

For support, open an issue on the GitHub repository.

## Reference

The structure and template of this repository were inspired by and adapted from [AI-Microapp-Template-Assistant](https://github.com/jswope00/AI-Microapp-Template-Assistant)
