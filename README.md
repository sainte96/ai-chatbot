# Telnyx AI Chatbot

This repository contains the code for a Telnyx AI Chatbot, which provides answers to questions related to SMS guidelines in different countries. The chatbot provides answers to questions related to Telnyx SMS guidelines i.e it won't answer who is the president of United States. The chatbot was built entirely on python using the LangChain framework, OpenAI API and OpenAI Embeddings. The embeddings are saved in DeepLake vector database. For demonstration, the chatbot has been deployed on Streamlit. Please click [here](https://telnyxaichatbot.streamlit.app/) for demo

## Setup

Follow these steps to set up and run the project locally:

1. Clone the repository:

```bash
git clone https://github.com/sainte96/ai-chatbot.git
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv env
source env/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. The `documentation.json` file is already included in the repository. It is located in the data/ directory of the project.

5. Run the Streamlit app from terminal by following the instructions provided in the [documentation.](https://docs.streamlit.io/library/get-started/installation) or
```bash
pip install streamlit
streamlit run telnyx_chatbot.py
```

6. Access the app in your web browser at http://localhost:8501.

## Challenges and Solutions

During the development process, I encountered a few challenges and implemented the following solutions:

- Building with LangChain framework: Working with Langchain framework for the first time proved challenging, but with dedication to studying the documentations, other online resources and zeal to learn, I was able to navigate this challenge successfully and glad to have added one more skill to the belt!

- Selecting the Vector Database: Choosing the right vector database posed a challenge during development. Integrating Pinecone with LangChain was time-consuming, and Pinecone's limitations on the free plan made it less suitable. DeepLake emerged as a more flexible alternative, offering various embedded data representations and the ability to create multiple datasets.. I referred to the DeepLake documentation and examples to implement the integration successfully.

- Deploying on Streamlit: Initially, I planned to run the project on the command line, but after discovering the various deployment options offered by LangChain, I decided to learn more about each of them. Streamlit, appears to be faster and its adoption by prominent companies like Uber and IBM made me consider it more. It proved to be an excellent choice that greatly benefited my project.

- Code Organization: As the project grew, maintaining code organization became important especially for readability and easy debugging. I structured the code into functions to separate concerns and improve readability. Additionally, I adhered to best practices, such as adding comments and following PEP 8 style guidelines.

By addressing these challenges, I was able to create a functional and organized Telnyx AI Chatbot that continuously accepts user input and provides relevant answers based on the SMS guidelines dataset.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

