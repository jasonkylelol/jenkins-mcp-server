# jenkins-mcp-server
mcp server for jenkins build tasks

# usage
1. config environment
```
vim .env # config jenkins url, user and token and openai api model and api key.
```
and edit server_config.json for your own mcp server port  

2. launch server
```
python3 mcp_server.py
```
3. run a jenkins build task
```
python3 mcp_client.py
```
then you will see the build task is running in jenkins, when the task is done, the client will show the result.
