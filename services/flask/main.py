from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from prompt import prompt
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from typing import Any
from model import db, Response


app = Flask(__name__)

CORS(app, origins="*")

# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# Load environment variables from .env file
load_dotenv()


@tool
def query_database(message):
    """
    Tool to query the database for predefined responses matching the client's criteria,
    using enhanced keyword matching and response ranking.
    """
    try:
        lower_message = message.lower()
        user_keywords = set(lower_message.split())

        # Ensure db.session is used in a Flask app context if needed
        all_responses = Response.query.all()

        best_response = None
        highest_match_count = 0

        for response in all_responses:
            response_keywords = set(response.keyword.lower().split())
            match_count = len(user_keywords.intersection(response_keywords))

            if match_count > highest_match_count:
                highest_match_count = match_count
                best_response = response.response_text
                
        if best_response:
            return best_response
        else:
            return "I'm not sure how to answer that. Could you please provide more details or ask a different question?"
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"Error querying database: {e}")
        return "I encountered an error while processing your request."
    

# Main Agent Function
def execute_agent(message_text):

    # Define tools
    tools = [query_database]
    
    llm_chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Bind tools to chat model
    llm_with_tools = llm_chat.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    # Define agent
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])
            
        }
        | prompt_template
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    try:
        
        response = agent_executor.invoke({"input": message_text})
        

        return response["output"]
    
    except AttributeError as ae:
        error_message = str(ae)
        print(f"AttributeError in execute_agent: {error_message}")
        return error_message
    

    

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})
    
# Updated message endpoint to utilize the update_query_frequency function
@app.route('/message', methods=['POST'])
def message():
    try:
        data = request.get_json()
        message_text = data.get('message')
        response_text = execute_agent(message_text)
        return jsonify({'message': response_text})

    except AttributeError as ae:
        error_message = str(ae)
        return jsonify({'error': 'An unexpected error occurred.', 'details': error_message}), 500
    
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': 'An error occurred while processing your request.', 'details': error_message}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=8080)