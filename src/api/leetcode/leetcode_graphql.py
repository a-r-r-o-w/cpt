import json

lcgraphql_objects = {
    "question_data": {
        "operationName": "questionData",
        "variables": {"titleSlug": None},
        "query": """\
      query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
          questionId
          questionFrontendId
          boundTopicId
          title
          titleSlug
          content
          translatedTitle
          translatedContent
          isPaidOnly
          difficulty
          likes
          dislikes
          isLiked
          similarQuestions
          exampleTestcases
          categoryTitle
          contributors {
            username
            profileUrl
            avatarUrl
            __typename
          }
          topicTags {
            name
            slug
            translatedName
            __typename
          }
          companyTagStats
          codeSnippets {
            lang
            langSlug
            code
            __typename
          }
          stats
          hints
          solution {
            id
            canSeeDetail
            paidOnly
            hasVideoSolution
            paidOnlyVideo
            __typename
          }
          status
          sampleTestCase
          metaData
          judgerAvailable
          judgeType
          mysqlSchemas
          enableRunCode
          enableTestMode
          enableDebugger
          envInfo
          libraryUrl
          adminUrl
          challengeQuestion {
            id
            date
            incompleteChallengeCount
            streakCount
            type
            __typename
          }
          __typename
        }
      }""",
    }
}


def get_object(name: str, variables: dict) -> str:
    obj = lcgraphql_objects.get(name)
    if obj is None:
        raise ValueError(f"Object with name {name} does not exist")
    obj["variables"].update(variables)
    return json.dumps(obj)
