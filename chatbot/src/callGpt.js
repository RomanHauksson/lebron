import { OpenAI } from "langchain/llms/openai";

async function callGpt (userMessage) {
    const model = new OpenAI({ openAIApiKey: "OPEN_AI_API_KEY", temperature: 0.9 });
    const response = await model.call(userMessage);
    return(response);
};

export { callGpt };