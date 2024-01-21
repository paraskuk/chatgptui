
#
# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
#     """
#     Endpoint to receive a query and return a response using OpenAI's Chat Completions API
#     :param query_params: User input
#     :return: JSONResponse containing the response and user level estimation
#     """
#     try:
#         # Using the Chat Completions API for the user's input
#         completion_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": query_params.user_input}
#             ]
#         )
#
#         moderation_result = client.moderations.create(
#                     input=query_params.user_input)
#
#         # Check if the completion response is valid
#         if not completion_response.choices or len(completion_response.choices) == 0 or not completion_response.choices[
#             0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for code completion.")
#
#         # Extracting the code completion response
#         code_completion = completion_response.choices[0].message.content
#
#         # Revised prompt for user's expertise level estimation
#         user_level_prompt = "Please evaluate and categorize the user's programming expertise level based on their previous query. Is the user a beginner, intermediate, or advanced programmer?"
#         level_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": user_level_prompt},
#                 {"role": "user", "content": query_params.user_input}  # Repeating the user's input for context
#             ]
#         )
#
#         # Extracting the user level estimation response
#         if not level_response.choices or len(level_response.choices) == 0 or not level_response.choices[0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for user level estimation.")
#
#         user_level_estimation = level_response.choices[0].message.content
#
#         # Sentiment analysis prompt
#         sentiment_analysis_prompt = "Analyze the sentiment of the user's previous query. Is the sentiment positive, negative, or neutral?"
#         sentiment_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": sentiment_analysis_prompt},
#                 {"role": "user", "content": query_params.user_input}  # Repeating the user's input for context
#             ]
#         )
#
#         # Extracting the sentiment analysis response
#         if not sentiment_response.choices or len(sentiment_response.choices) == 0 or not sentiment_response.choices[
#             0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for sentiment analysis.")
#
#         sentiment_estimation = sentiment_response.choices[0].message.content
#
#         # Return the code completion response with user level estimation and sentiment analysis appended
#         return JSONResponse(content={
#             "response": code_completion + "\n\nUser Level Estimation: " + user_level_estimation +
#                         "\n\nSentiment Analysis: " + sentiment_estimation
#         })
#
#         # # Return the code completion response and user level estimation
#         # return JSONResponse(content={
#         #     "response": code_completion + "\n\nUser Level Estimation: " + user_level_estimation
#         # })
#
#     except Exception as e:
#         log.error(f"Exception occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# ###this works also for user level estimation
# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
#     """
#     Endpoint to receive a query and return a response using OpenAI's Chat Completions API
#     :param query_params: User input
#     :return: JSONResponse containing the response and user level estimation
#     """
#     try:
#         # Using the Chat Completions API for the user's input
#         completion_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": query_params.user_input}
#             ]
#         )
#
#         # Check if the completion response is valid
#         if not completion_response.choices or len(completion_response.choices) == 0 or not completion_response.choices[
#             0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for code completion.")
#
#         # Extracting the code completion response
#         code_completion = completion_response.choices[0].message.content
#
#         # Revised prompt for user's expertise level estimation
#         user_level_prompt = "Please evaluate and categorize the user's programming expertise level based on their previous query. Is the user a beginner, intermediate, or advanced programmer?"
#         level_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": user_level_prompt},
#                 {"role": "user", "content": query_params.user_input}  # Repeating the user's input for context
#             ]
#         )
#
#         # Extracting the user level estimation response
#         if not level_response.choices or len(level_response.choices) == 0 or not level_response.choices[0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for user level estimation.")
#
#         user_level_estimation = level_response.choices[0].message.content
#
#         # Return the code completion response and user level estimation
#         return JSONResponse(content={
#             "response": code_completion + "\n\nUser Level Estimation: " + user_level_estimation
#         })
#
#     except Exception as e:
#         log.error(f"Exception occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# this route doesnt have user level estimation
# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
#     """
#     Endpoint to receive a query and return a response using OpenAI's Chat Completions API
#     :param query_params: User input
#     :return: JSONResponse containing the response, user level estimation, and moderation result
#     """
#     try:
#         # Adding Moderation API tracking
#
#
#         # Using the Chat Completions API for the user's input
#         completion_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for coding completions in Python using version of at least 3.11."},
#                 {"role": "user", "content": query_params.user_input}
#             ]
#         )
#
#         moderation_result = client.moderations.create(
#             input=query_params.user_input
#         )
#
#         # Check if the completion response is valid
#         if not completion_response.choices or len(completion_response.choices) == 0 or not completion_response.choices[0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for code completion.")
#
#         # Extracting the code completion response
#         code_completion = completion_response.choices[0].message.content
#
#         # Estimating the user's expertise level with the same GPT-4 call
#         user_level_prompt = f"How would you describe the programming expertise level of a user based on this query: '{query_params.user_input}'?"
#         level_response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": user_level_prompt}
#
#             ]
#         )
#
#         # Extracting the user level estimation response
#         if not level_response.choices or len(level_response.choices) == 0 or not level_response.choices[0].message:
#             raise HTTPException(status_code=500, detail="No response from the model for user level estimation.")
#
#         user_level_estimation = level_response.choices[0].message.content
#
#         # Return the code completion response, user level estimation, and moderation result
#         return JSONResponse(content={
#             "response": code_completion,
#             "user_level_estimation": user_level_estimation
#
#         })
#
#     except Exception as e:
#         log.error(f"Exception occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
#


#
# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
#     """
#     Endpoint to receive a query and return a response using OpenAI's Chat Completions API
#     :param query_params: User input
#     :return: JSONResponse containing the response
#     """
#     try:
#
#         # Using the Chat Completions API
#         response = client.chat.completions.create(
#             model=query_params.model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant for coding completions in Python using version of at least 3.11."},
#                 {"role": "user", "content": query_params.user_input}
#             ]
#         )
#
#         # Adding Moderation API tracking
#         moderation_input = client.moderations.create(
#             input=query_params.user_input
#         )
#
#         # Extracting the response
#         if response.choices and len(response.choices) > 0 and response.choices[0].message:
#             return JSONResponse(content={"response": response.choices[0].message.content})
#         else:
#             raise HTTPException(status_code=500, detail="No response from the model.")
#     except Exception as e:
#         log.error(f"Exception occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))



# @app.get("/login/github")
# async def login_via_github(request: Request):
#     # Check if the user is already authenticated
#     if 'auth_token' in request.state.session:
#         return RedirectResponse(url='/')
#
#     # Generate the OAuth state
#     state = secrets.token_urlsafe(32)
#     request.state.session['oauth_state'] = state
#     log.debug(f"Generated OAuth state: {state}")
#
#     # Retrieve or create a new session ID
#     session_id = request.cookies.get('session_id') or str(uuid.uuid4())
#     redis_client.set(session_id, json.dumps(request.state.session))
#     log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")
#
#     # Redirect to GitHub for authentication
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     auth_url = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
#
#     # Set the session ID cookie in the response
#     response = RedirectResponse(url=auth_url)
#     response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, max_age=3600)
#     return response

#
# @app.get("/login/github")
# async def login_via_github(request: Request):
#     # Check if the user is already authenticated
#     if 'auth_token' in request.state.session:
#         log.debug("User already authenticated, redirecting to home.")
#         return RedirectResponse(url='/')
#
#     # Generate the OAuth state
#     state = secrets.token_urlsafe(32)
#     request.state.session['oauth_state'] = state
#     log.debug(f"Generated OAuth state: {state}")
#
#     # Retrieve or create a new session ID
#     session_id = request.cookies.get('session_id') or str(uuid.uuid4())
#     redis_client.set(session_id, json.dumps(request.state.session))
#     log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")
#
#     # Generate the authorization URL for GitHub OAuth
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     try:
#         auth_url = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
#     except Exception as e:
#         log.error(f"Error generating authorization URL: {e}")
#         raise HTTPException(status_code=500, detail="Error generating authorization URL")
#
#     # Set the session ID cookie in the response
#     response = RedirectResponse(url=auth_url)
#     response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, max_age=3600)
#     log.debug(f"Redirecting to GitHub for authentication with session_id: {session_id}")
#
#     return response

#
# @app.get("/login/github")
# async def login_via_github(request: Request):
#     # Check if the user is already authenticated
#     if 'auth_token' in request.state.session:
#         log.debug("User already authenticated, redirecting to home.")
#         return RedirectResponse(url='/')
#
#     # Generate the OAuth state
#     state = secrets.token_urlsafe(32)
#     request.state.session['oauth_state'] = state
#     log.debug(f"Generated OAuth state: {state}")
#
#     # Retrieve or create a new session ID
#     session_id = request.cookies.get('session_id') or str(uuid.uuid4())
#     redis_client.set(session_id, json.dumps(request.state.session))
#     log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")
#
#     # Generate the authorization URL for GitHub OAuth
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     response = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
#
#     # Ensure the response is a RedirectResponse and set the session_id cookie
#     if isinstance(response, RedirectResponse):
#         response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, max_age=3600)
#         log.debug(f"Redirecting to GitHub for authentication with session_id: {session_id}")
#         return response
#     else:
#         log.error(f"Expected a RedirectResponse, but got: {type(response)}")
#         raise HTTPException(status_code=500, detail="Error during redirection to GitHub")

# @app.get("/login/github")
# async def login_via_github(request: Request):
#     # Check if the user is already authenticated
#     if 'auth_token' in request.state.session:
#         log.debug("User already authenticated, redirecting to home.")
#         return RedirectResponse(url='/')
#
#     # Generate the OAuth state
#     state = secrets.token_urlsafe(32)
#     request.state.session['oauth_state'] = state
#     log.debug(f"Generated OAuth state: {state}")
#
#     # Retrieve or create a new session ID
#     session_id = request.cookies.get('session_id') or str(uuid.uuid4())
#     redis_client.set(session_id, json.dumps(request.state.session))
#     log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")
#
#     # Generate the authorization URL for GitHub OAuth
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     try:
#         auth_url = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
#     except Exception as e:
#         log.error(f"Error generating authorization URL: {e}")
#         raise HTTPException(status_code=500, detail="Error generating authorization URL")
#
#     # Set the session ID cookie in the response
#     response = RedirectResponse(url=auth_url)
#     response.set_cookie(key="session_id", value=session_id, httponly=True, samesite='Lax', max_age=3600) # Removed `secure=True` for local testing
#     log.debug(f"Redirecting to GitHub for authentication with session_id: {session_id}")
#
#     return response


#
# #thuis sets session and outh state correctly but does not redirect to github
# @app.get("/login/github")
# async def login_via_github(request: Request):
#     # Check if the user is already authenticated
#     if 'auth_token' in request.state.session:
#         log.debug("User already authenticated, redirecting to home.")
#         return RedirectResponse(url='/')
#
#     # Generate the OAuth state
#     state = secrets.token_urlsafe(32)
#     request.state.session['oauth_state'] = state
#     log.debug(f"Generated OAuth state: {state}")
#
#     # Retrieve or create a new session ID
#     session_id = request.cookies.get('session_id') or str(uuid.uuid4())
#     redis_client.set(session_id, json.dumps(request.state.session))
#     log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")
#
#     # Generate the authorization URL for GitHub OAuth
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     try:
#         auth_url = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
#     except Exception as e:
#         log.error(f"Error generating authorization URL: {e}")
#         raise HTTPException(status_code=500, detail="Error generating authorization URL")
#
#     # Set the session ID cookie in the response
#     response = RedirectResponse(url=auth_url)
#     response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, max_age=3600)
#     log.debug(f"Redirecting to GitHub for authentication with session_id: {session_id}")
#
#     return response
#
#
# @app.route('/auth/github/callback')
# async def authorize(request: Request):
#     # Retrieve the session ID from the cookie
#     session_id = request.cookies.get('session_id')
#     log.debug(f"Callback received with session_id: {session_id}")
#
#     if not session_id:
#         log.error("Session ID is None. Possible cookie issue.")
#         # Redirect to an error page or handle as needed
#         return RedirectResponse(url='/login-error?message=Session ID not found')
#
#     # Retrieve the session data from Redis
#     session_data_json = redis_client.get(session_id)
#     if not session_data_json:
#         log.error("Session data not found in Redis.")
#         # Redirect to an error page or handle as needed
#         return RedirectResponse(url='/login-error?message=Session data not found')
#
#     request.state.session = json.loads(session_data_json)
#     log.debug(f"Retrieved session data from Redis: {session_data_json}")
#
#     # Compare the OAuth state
#     session_state = request.state.session.get('oauth_state')
#     callback_state = request.query_params.get('state')
#     log.debug(f"Session State: {session_state}, Callback State: {callback_state}")
#
#     if session_state != callback_state:
#         log.error("State mismatch error.")
#         # Redirect to an error page or handle as needed
#         return RedirectResponse(url='/login-error?message=State mismatch')
#
#     try:
#         # Exchange the code for a token
#         token = await oauth.github.authorize_access_token(request)
#         request.state.session['auth_token'] = token['access_token']
#
#         # Update the session data in Redis
#         redis_client.set(session_id, json.dumps(request.state.session))
#         log.debug("Authorization successful, redirecting to authenticated page.")
#         return RedirectResponse(url='/authenticated')
#     except Exception as e:
#         log.error(f"Error during authorization: {e}")
#         # Redirect to an error page or handle as needed
#         return RedirectResponse(url='/login-error?message=Authorization failure')


##this worked but did not call the callback
# @app.route('/auth/github/callback')
# async def authorize(request: Request):
#     # Retrieve the session ID from the cookie
#     session_id = request.cookies.get('session_id')
#     log.debug(f"Callback received with session_id: {session_id}")
#
#     # Retrieve the session data from Redis
#     session_data_json = redis_client.get(session_id)
#     if session_data_json:
#         request.state.session = json.loads(session_data_json)
#     else:
#         request.state.session = {}
#     log.debug(f"Retrieved session data from Redis: {session_data_json}")
#
#     # Compare the OAuth state
#     session_state = request.state.session.get('oauth_state')
#     callback_state = request.query_params.get('state')
#     log.debug(f"Session State: {session_state}, Callback State: {callback_state}")
#     if session_state != callback_state:
#         raise HTTPException(status_code=400, detail="State mismatch")
#
#     # Exchange the code for a token
#     token = await oauth.github.authorize_access_token(request)
#
#     # Here, you might want to use the token to fetch user information from GitHub,
#     # create a user session, or perform other application-specific actions
#     request.state.session['auth_token'] = token['access_token']
#
#     # Update the session data in Redis
#     redis_client.set(session_id, json.dumps(request.state.session))
#
#     # Redirect the user to a specific page after successful authentication
#     return RedirectResponse(url='/authenticated')
#

#
# @app.route('/auth/github/callback')
# async def authorize(request: Request):
#     session_state = request.state.session.get('oauth_state')
#     callback_state = request.query_params.get('state')
#     log.info(f"Session State: {session_state}, Callback State: {callback_state}")
#     if session_state != callback_state:
#         raise HTTPException(status_code=400, detail="State mismatch")
#
#     code = request.query_params.get('code')
#     token = await oauth.github.authorize_access_token(request, code=code)
#     request.state.session['auth_token'] = token['access_token']
#     log.debug(f"GitHub access token retrieved: {token['access_token']}")
#     return RedirectResponse(url='/authenticated')



#
# @app.route('/auth/github/callback')
# async def authorize(request: Request):
#     log.debug("Received GitHub callback")
#     session_state = request.session.get('oauth_state')
#     callback_state = request.query_params.get('state')
#     log.info(f"Session State: {session_state}, Callback State: {callback_state}")
#
#     if session_state != callback_state:
#         log.error("State mismatch error")
#         raise HTTPException(status_code=400, detail="State mismatch")
#
#     token = await oauth.github.authorize_access_token(request)
#     request.session['auth_token'] = token['access_token']
#     log.debug(f"GitHub access token retrieved: {token['access_token']}")
#     return RedirectResponse(url='/authenticated')



# @app.route('/login/github')
# async def login_via_github(request: Request):
#     if 'auth_token' in request.session:
#         # Redirect to a page for authenticated users
#         return RedirectResponse(url='/')
#     redirect_uri = 'http://localhost:8000/auth/github/callback'
#     return await oauth.github.authorize_redirect(request, redirect_uri)
#
# @app.route('/auth/github/callback')
# # @app.route('/authorize')
# async def authorize(request: Request):
#     token = await oauth.github.authorize_access_token(request)
#     request.session['auth_token'] = token['access_token']
#     # Redirect to a frontend route
#     return RedirectResponse(url='/authenticated')




# @app.get("/logout")
# async def logout(request: Request):
#     session_id = request.cookies.get('session_id')
#     if session_id:
#         redis_client.delete(session_id)
#     return RedirectResponse(url='/')


# @app.get("/logout")
# async def logout(request: Request):
#     request.session.clear()
#     # Redirect to the home page or login page after logout
#     return RedirectResponse(url='/')


