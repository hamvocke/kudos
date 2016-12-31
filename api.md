Kudos REST API
==============

## Feedback
The **feedback** resource represents a thing you collect feedback for. 

### GET /feedback
Retrieve a list of all feedbacks known to the system

#### Request

    curl http://getkudos.com/feedback

#### Response

  * `200 OK` and the list of feedbacks in the body if everything was ok

### GET /feedback/{identifier}
Retrieve information for a single feedback, identified by `identifier`

#### Request

    curl http://getkudos.com/feedback/crazy_banana

#### Response

  * `200 OK` and the feedback information in the body if everything was ok
  * `404 NOT FOUND` for unknown feedback identifiers

### POST /feedback
Create a new feedback.

#### Request

Header: `Content-Type: application/json`
Body:
```javascript
{
    name: 'My Retrospective',
    email: 'youremail@example.test'
}
```

    curl -X POST -H "Content-Type: application/json" -X POST -d '{name: "My Retrospective", email: "youremail@example.test"}' http://getkudos.com/feedback

#### Response

  * `201 CREATED` if the feedback has successfully been created
  * `400 BAD REQUEST` if the request data was malformed

