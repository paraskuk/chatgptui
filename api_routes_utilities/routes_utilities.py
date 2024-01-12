
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
