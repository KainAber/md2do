from src.utils import (
    get_system_prompt,
    get_user_prompt,
    get_openai_config,
    create_openai_client,
    load_function_schemas,
    load_functions_module,
    get_todo_md,
    format_numbered_todo,
    fill_system_prompt,
    fill_user_prompt,
    get_user_input,
    get_model_response,
    has_function_call,
    get_function_details,
    execute_function_call,
    get_clean_git_diff,
    display_model_response_with_tts,
    get_git_diff,
    add_function_call_to_messages,
    commit_todo_changes,
    logger,
)


def app():
    system_prompt_template = get_system_prompt()
    user_prompt_template = get_user_prompt()
    config = get_openai_config()
    client = create_openai_client(config)
    functions = load_function_schemas()
    functions_module = load_functions_module()

    messages = [{"role": "system", "content": ""}]

    while True:
        todo_md = get_todo_md()
        numbered_todo = format_numbered_todo(todo_md)
        system_prompt_filled = fill_system_prompt(system_prompt_template, numbered_todo)

        user_input = get_user_input()
        if not user_input.strip() or user_input.lower() in ["quit", "exit", "q", "stop"]:
            break

        user_prompt_filled = fill_user_prompt(user_prompt_template, user_input)

        messages[0] = {"role": "system", "content": system_prompt_filled}
        messages.append({"role": "user", "content": user_prompt_filled})

        logger.debug(f"Full messages list before LLM call: {messages}")
        response_message = get_model_response(client, messages, functions)
        logger.debug(f"LLM response: {response_message}")

        while has_function_call(response_message):
            function_name, function_args = get_function_details(response_message)
            function_result = execute_function_call(
                functions_module, function_name, function_args, todo_md.splitlines()
            )

            todo_md = get_todo_md()

            git_diff_result = get_git_diff()
            if git_diff_result:
                function_result += f"\n\nChanges made:\n{git_diff_result}"

            messages = add_function_call_to_messages(
                messages, response_message, function_name, function_result
            )

            logger.debug(f"Full messages list before LLM call: {messages}")
            response_message = get_model_response(client, messages, functions)
            logger.debug(f"LLM response: {response_message}")

        change_message = get_clean_git_diff()
        if change_message:
            logger.info(change_message)
            commit_todo_changes(user_input)

        display_model_response_with_tts(client, response_message)
        messages.append({"role": "assistant", "content": response_message.content})


if __name__ == "__main__":
    app()
