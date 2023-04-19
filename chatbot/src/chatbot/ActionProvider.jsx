import { lebronSays } from '../lebronSays.js';
import React, { useEffect, useState } from 'react';
import { ChatOpenAI } from "langchain/chat_models/openai";
import { OpenAI } from "langchain/llms/openai";
import { genAudio } from "../voicetrialsrandom.js";
import { ConversationChain, SqlDatabaseChain } from 'langchain/chains';
import { initializeAgentExecutor, Tool } from "langchain/agents";
import { DynamicTool } from "langchain/tools";
import sound from "./sample.mp4";

import { Calculator } from "langchain/tools/calculator";
import { BufferMemory } from "langchain/memory";

async function createExecutor() {
    const chatModel = new ChatOpenAI({
        openAIApiKey: "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",
        temperature: 0.6
    });

    const tools = [
        new Calculator(),
    ]
    const executor = await initializeAgentExecutor(
        tools,
        chatModel,
        "chat-conversational-react-description",
        true
    );
    executor.memory = new BufferMemory({
        returnMessages: true,
        memoryKey: "chat_history",
        inputKey: "input",
    });
    return executor;
 }

// Create a new const called "executor" and assign it to the result of calling createExecutor()
// This must avoid assigning the object to a promise, instead it must assign "executor" to the result of the promise
// This doesn't work: const executor = createExecutor();
const executor = await createExecutor();

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
    const [userMessage, setUserMessage] = useState('');

    // https://js.langchain.com/docs/modules/chains/llmchain/
    // https://js.langchain.com/docs/getting-started/guide-chat#memory-add-state-to-chains-and-agents

    async function getResponse(message) {
        if (!message) {
            return;
        }
        const newResponse = await executor.call({
            input: message,
        });
        const newResponseText = newResponse.output;
        console.log("User Message: " + message);
        console.log("Response: " + newResponseText);
        const botMessage = createChatBotMessage(newResponseText);
        lebronSays(newResponseText);
        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, botMessage],
        }));
    }

    useEffect(() => {
        getResponse(userMessage);
    }, [userMessage]); 

    const gptResponse = (message) => {
        setUserMessage(message);
    };
    
    return (
        <div>
        {React.Children.map(children, (child) => {
            return React.cloneElement(child, {
            actions: {
                gptResponse,
            },
            });
        })}
        </div>
    );
};

export default ActionProvider;