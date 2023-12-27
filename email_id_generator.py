def generate_emails_helper(username, index, current_username, output_usernames):
    if index == len(username):
        output_usernames.append(current_username+"@gmail.com")
        return

    # Do not insert a period at the current index
    generate_emails_helper(
        username, index + 1, current_username + username[index], output_usernames)

    # Insert a period at the current index, but not at the beginning
    if current_username:
        generate_emails_helper(
            username, index + 1, current_username + '.' + username[index], output_usernames)


def generate_emails(username):
    output_usernames = []
    generate_emails_helper(username, 0, "", output_usernames)
    return [email for email in output_usernames]


# Example usage
input_username = "helloworld"
result = generate_emails(input_username)

# Print the result
print(len(result))
for email in result:
    print(email)
