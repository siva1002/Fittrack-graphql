function friends() {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNpdmFzdXJ1bGkiLCJleHAiOjE2OTc0NDI4NTMsIm9yaWdJYXQiOjE2OTc0NDI1NTN9.0BH3Pspj97ns_5zhoNXmMnMEe6QjSHEe-yinn_19zuE"
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const graphqlQuery = `
{
    friends {
      userfriend {
        email
        username
      }
    }
  }
`;

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            Authorization: "JWT " + token
        },
        body: JSON.stringify({ query: graphqlQuery }),
    };

    fetch(`${graphqlEndpoint}/fit/graphql/`, options)
        .then(response => response.json())
        .then(data => {
            // Handle the GraphQL response data
            console.log('GraphQL response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    console.log(graphqlEndpoint)
}


friends()
