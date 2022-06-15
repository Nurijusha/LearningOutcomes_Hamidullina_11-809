from flask import Flask, request, jsonify, Response

import logger_utils
from check_solution import SolutionTests
from testing.schemas import LearningOutcomeSchema

# Set logging
logger = logger_utils.setup_applevel_logger()

app = Flask(__name__)


@app.route('/do-static-tests/', methods=['GET'])
@app.route('/do-static-tests', methods=['GET'])
def static_testing():
    data = request.get_json()

    if not data:
        return Response(status=404)

    url: str = data.get('github_url')
    if not url:
        return Response(status=404)
    if not url.startswith('https://github.com/'):
        return jsonify({
            'github_url': url,
            'result': 'error'
        })

    logger.info(f'New url: {url}')

    solution = SolutionTests(url)
    try:
        result = solution.run_tests()
    except Exception:
        return jsonify({'github_url': url, 'result': 'error', })

    if isinstance(result, bool):
        return jsonify({
            'github_url': url,
            'result': 'error'
        })

    lo_schema = LearningOutcomeSchema(many=True)
    serialized_data = lo_schema.dump(result)

    return jsonify({
        'github_url': url,
        'result': serialized_data
    })


if __name__ == '__main__':
    app.run(port=6001, debug=True)
