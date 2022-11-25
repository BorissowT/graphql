to get auth token:

mutation {
  tokenAuth(username:"tim",password:"1234"){
    token
  }
}

request header to make requests:
{
  "AUTHORIZATION": "JWT <token>"
}


create a link:

mutation{
  createLink(url:"https://en.wikipedia.org/wiki/README", description:"how to create readme"){
    id
    url
    description
    postedBy{
      id
      username
      email
    }
    
  }
}

vote for a link:

mutation{
  createVote(linkId: 2) {
    user{
      id
      username
      email
    }
    link{
      id
      description
      url
    }
  }
}

see all links:

query{
  links {
    id
    url
    votes {
      id
      user {
        id
        username
      }
    }
  }
}

search query:

query {
  links(search:"jonatas"){
    id
    url
    description
  }
}

query with pagination: 

query {
  links(first:2, skip:1){
    id
    url
    description
  }
}