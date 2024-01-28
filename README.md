# jarvis-2024
Local terminal interface for chatgpt AI. Provides a "stateful" experience. Unlike regular chatgpt, jarvis-2024 remembers previous conversations, and uses every conversation to update itself to be more personalized for its user.

## Configure

Create `.env` file with an [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) in the same directory, using the following format:

`OPENAI_API_KEY=copy_api_key_here`

## Run AI

`./run_jarvis.sh`

If you get a 'permission denied' error, run: `chmod +x run_jarvis.sh`

Type `bye` to exit the program.
